from datetime import datetime, timezone
from pathlib import Path
import uuid

import cv2
from ultralytics import YOLO
from sqlalchemy.orm import Session

from app.config import settings
from app.models.detection import Detection

from app.models.evidence import Evidence
from app.models.alert import Alert

import subprocess


class YOLODetector:
    def __init__(self):
        self.model = YOLO(settings.yolo_model_path)

    def process_video(
        self,
        video_path: str,
        analysis_run_id: int,
        db: Session,
    ):
        video_file = Path(video_path)

        if not video_file.exists():
            raise FileNotFoundError(
                f"Video not found: {video_path}"
            )

        video = cv2.VideoCapture(str(video_file))

        if not video.isOpened():
            raise RuntimeError(
                f"Could not open video: {video_path}"
            )

        fps = video.get(cv2.CAP_PROP_FPS)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)

        evidence_dir = Path("evidence")
        evidence_dir.mkdir(exist_ok=True)

        temp_output_path = (
            output_dir / f"{video_file.stem}_detected_temp.mp4"
        )

        output_path = (
            output_dir / f"{video_file.stem}_detected.mp4"
        )

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        writer = cv2.VideoWriter(
            str(temp_output_path),
            fourcc,
            fps,
            (width, height),
        )

        frame_number = 0
        low_confidence_count = 0

        try:
            while True:
                success, frame = video.read()

                if not success:
                    break

                results = self.model(frame, conf=0.5)

                result = results[0]

                annotated_frame = result.plot()

                writer.write(annotated_frame)

                if len(result.boxes) > 0 and frame_number % 30 == 0:
                    evidence_filename = (
                        f"run_{analysis_run_id}_frame_{frame_number}.jpg"
                    )

                    evidence_path = evidence_dir / evidence_filename

                    cv2.imwrite(
                        str(evidence_path),
                        annotated_frame,
                    )

                    evidence = Evidence(
                        detection_id=None,
                        evidence_id=f"evidence_{uuid.uuid4().hex}",
                        kind="frame",
                        uri=str(evidence_path),
                        description=(
                            f"Annotated evidence frame {frame_number} "
                            f"from analysis run {analysis_run_id}"
                        ),
                        created_at=datetime.now(timezone.utc),
                    )

                    db.add(evidence)

                for box in result.boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    if confidence < 0.60:
                        low_confidence_count += 1

                    species = self.model.names[class_id]

                    x1, y1, x2, y2 = (
                        float(value)
                        for value in box.xyxy[0]
                    )

                    detection = Detection(
                        analysis_run_id=analysis_run_id,
                        event_id=f"evt_{uuid.uuid4().hex}",
                        timestamp=datetime.now(timezone.utc),
                        species=species,
                        detection_confidence=confidence,
                        frame_number=frame_number,
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2,
                    )

                    db.add(detection)

                frame_number += 1

            if low_confidence_count > 0:
                alert = Alert(
                    analysis_run_id=analysis_run_id,
                    alert_id=f"alert_{uuid.uuid4().hex}",
                    severity="medium",
                    message=(
                        f"{low_confidence_count} detection(s) had confidence "
                        "below 0.60 and require human review."
                    ),
                    created_at=datetime.now(timezone.utc),
                )
                db.add(alert)

            db.commit()
            
        except Exception:
            db.rollback()
            raise

        finally:
            video.release()
            writer.release()

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(temp_output_path),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(output_path),
            ],
            check=True,
        )

        temp_output_path.unlink()

        return str(output_path)