from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import re

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.analysis_run import AnalysisRun
from app.models.detection import Detection
from app.models.evidence import Evidence
from app.models.alert import Alert


def build_m4_payload(
    db: Session,
    analysis_run: AnalysisRun,
) -> dict:
    generated_at = datetime.now(timezone.utc)

    window_start = analysis_run.started_at
    window_end = analysis_run.ended_at or generated_at

    detections = db.scalars(
        select(Detection)
        .where(
            Detection.analysis_run_id == analysis_run.id
        )
        .order_by(Detection.frame_number)
    ).all()

    alerts = db.scalars(
        select(Alert)
        .where(
            Alert.analysis_run_id == analysis_run.id
        )
    ).all()

    # Evidence files currently contain the run and frame number
    # in their filename, e.g. run_7_frame_1050.jpg.
    evidence_rows = db.scalars(
        select(Evidence)
    ).all()

    evidence_by_frame = {}

    pattern = re.compile(
        rf"run_{analysis_run.id}_frame_(\d+)"
    )

    for evidence in evidence_rows:
        match = pattern.search(Path(evidence.uri).name)

        if not match:
            continue

        frame_number = int(match.group(1))

        evidence_by_frame.setdefault(
            frame_number,
            [],
        ).append(
            {
                "evidence_id": evidence.evidence_id,
                "kind": evidence.kind,
                "uri": evidence.uri,
                "description": evidence.description,
            }
        )

    observations = []

    for detection in detections:
        observation = {
            "event_id": detection.event_id,
            "timestamp": detection.timestamp.isoformat(),
            "species": detection.species,
            "detection_confidence": detection.detection_confidence,
        }

        frame_evidence = evidence_by_frame.get(
            detection.frame_number,
            [],
        )

        if frame_evidence:
            observation["evidence"] = frame_evidence

        observations.append(observation)

    # M3 tracking/Re-ID is not implemented yet.
    # Therefore we must not pretend detection count == unique animals.
    species_counts = Counter(
        detection.species
        for detection in detections
    )

    counts = [
        {
            "species": species,
            "unique_individuals": 0,
        }
        for species in sorted(species_counts)
    ]

    payload = {
        "source_id": f"analysis_run_{analysis_run.id}",
        "generated_at": generated_at.isoformat(),
        "window_start": window_start.isoformat(),
        "window_end": window_end.isoformat(),
        "observations": observations,
        "counts": counts,
        "alerts": [
            {
                "alert_id": alert.alert_id,
                "severity": alert.severity,
                "message": alert.message,
            }
            for alert in alerts
        ],
    }

    if analysis_run.camera_id is not None:
        payload["camera_id"] = str(
            analysis_run.camera_id
        )

    return payload