# VanDrishti

**Privacy-conscious, offline-first wildlife monitoring and forest-threat
analysis.**

VanDrishti is a wildlife-monitoring project designed to help authorized
conservation teams analyze camera footage, identify animal activity,
review evidence, and surface potential threats such as forest fires. It
is intended for deployment on local infrastructure in remote areas where
internet connectivity may be unreliable or unavailable.

> **Security principle:** Wildlife observations and location metadata
> can be sensitive. Production deployments should keep data on
> authorized local infrastructure, restrict access, and avoid publishing
> raw footage, precise locations, credentials, or other operational
> details.

## Project goals

-   Detect wildlife in camera footage using computer vision.
-   Store analysis results and supporting evidence in a local database.
-   Produce structured intelligence summaries using a locally hosted
    language model.
-   Surface potential threats through an alert workflow, including the
    planned forest-fire detection workflow.
-   Support human review of evidence and generated intelligence.
-   Minimize dependence on internet connectivity during field operation.
-   Treat animal re-identification (ReID) as an experimental capability
    until it has been validated on representative field data.

## Current status

VanDrishti is an evolving prototype. The following status labels
distinguish the intended design from verified functionality:

  -----------------------------------------------------------------------
  Capability                          Status
  ----------------------------------- -----------------------------------
  Video-analysis workflow and         Implemented as a prototype;
  wildlife detection                  validate with the target deployment
                                      data

  PostgreSQL storage for analysis     Implemented in the backend
  runs, detections, evidence, and     
  related records                     

  Intelligence processing and         Implemented in the M4 intelligence
  structured outputs                  module; validate model availability
                                      and output quality locally

  Review workflow and dashboard       Under integration; verify
                                      end-to-end behavior before relying
                                      on it

  Forest-fire detection and genuine   Development priority; do not treat
  fire alerts                         as operational until trained,
                                      tested, and validated

  Animal ReID across frames or        Experimental; real-world accuracy
  cameras                             is not yet validated

  Fully offline end-to-end operation  Deployment goal; requires an
                                      offline acceptance test

  Production-grade security           Requires deployment-specific
                                      hardening and verification
  -----------------------------------------------------------------------

This table is deliberately conservative. A component existing in the
codebase does not by itself mean that its complete workflow is reliable
or production-ready.

## System architecture

The project is organized into a computer-vision/backend path and an
intelligence-processing path.

``` text
Camera footage / uploaded video
             |
             v
    M2: Detection / species model
             |
             v
    M3: Tracking / ReID / counting
    (ReID remains experimental)
             |
             v
    M1: Backend API
             |
             v
    PostgreSQL database
    - analysis runs
    - detections
    - evidence
    - alerts
             |
             v
    M4: Intelligence processing
    - contract-based input/output
    - fact packet
    - local LLM generation
    - numeric guard / validation
    - explainability information
    - review queue
             |
             v
    M5: Dashboard / authorized human review
```

The exact modules available in a given branch may differ. The
architecture above describes the intended integration flow, not a claim
that every stage is fully integrated in every branch.

### Main components

-   **Computer vision:** YOLO-based detection and related video-analysis
    components.
-   **M1 backend:** API and database integration for analysis runs,
    detections, evidence, and alerts.
-   **M4 intelligence module:** Processes structured evidence through
    contract-defined inputs and outputs, generates intelligence
    summaries, applies numeric checks, and supports review.
-   **Database:** PostgreSQL for persistent application records.
-   **Frontend:** React with Vite for the monitoring dashboard and
    review experience.
-   **Model inference and language generation:** Intended to run on
    local hardware for offline field deployments.

M4 should communicate through defined contracts and backend APIs rather
than accessing M1's database directly.

## Technology stack

  -----------------------------------------------------------------------
  Area                                Technology
  ----------------------------------- -----------------------------------
  Frontend                            React, Vite, JavaScript

  Backend API                         Python, FastAPI

  Computer vision                     YOLO-based object detection

  Database                            PostgreSQL

  Database migrations                 Alembic

  Intelligence processing             Python, contract/schema validation,
                                      local LLM integration

  API/data contracts                  JSON Schema and Pydantic

  Local development                   Separate frontend, backend, and
                                      intelligence services
  -----------------------------------------------------------------------

Exact package versions and environment-specific requirements should be
taken from the relevant branch's dependency files.

## Privacy and security

Wildlife data can expose endangered species to disturbance, capture, or
poaching when observations are linked to precise locations and times.
VanDrishti should therefore be deployed as a restricted conservation
tool, not as a public wildlife-data portal.

### Data-handling principles

1.  **Keep the repository private.** Do not publish operational
    datasets, sensitive footage, camera coordinates, precise sighting
    locations, or private deployment configuration.
2.  **Keep sensitive data local.** Store footage, evidence, detections,
    and location metadata on authorized infrastructure. Avoid sending
    them to third-party services.
3.  **Run inference locally.** Configure the detection model and LLM to
    use locally available model files and local inference services. Do
    not silently fall back to cloud inference.
4.  **Restrict access.** Require authentication and authorization for
    dashboard and API access. Apply least-privilege permissions to
    database users and filesystem directories.
5.  **Protect secrets.** Keep passwords, API keys, signing keys,
    database URLs, and private configuration out of source control. Use
    environment variables or an appropriately protected local secrets
    mechanism.
6.  **Limit location exposure.** Show precise coordinates only to
    authorized users who need them. Redact or generalize location data
    in exports, screenshots, logs, reports, and demonstrations.
7.  **Validate inputs.** Apply upload size and file-type limits,
    validate API payloads, and avoid trusting uploaded files or
    generated model output.
8.  **Audit sensitive actions.** Record appropriate access and review
    events while avoiding unnecessary logging of exact coordinates,
    secrets, or raw sensitive content.
9.  **Secure local networking.** Bind services to loopback or a
    protected local network where appropriate. Do not expose development
    servers or database ports to untrusted networks.
10. **Back up carefully.** Encrypt and restrict backups where supported,
    control who can restore them, and test recovery procedures.

A private repository is only one layer of protection. It does not
replace authentication, network controls, database permissions, secure
storage, or operational procedures.

## Offline-first deployment

The deployment goal is to operate in remote areas without internet
access during normal use.

For a genuinely offline installation:

-   Install the operating system packages and Python/Node dependencies
    before field deployment.
-   Download and verify all required model weights in advance.
-   Keep the detection model and LLM weights on authorized local
    storage.
-   Configure the LLM runtime to use a local model and local endpoint;
    disable cloud-provider fallbacks.
-   Ensure the application does not depend on remote APIs, hosted
    databases, remote fonts, CDNs, or externally hosted frontend assets
    at runtime.
-   Configure the backend, database, and frontend to communicate over
    local interfaces or a protected local network.
-   Verify that logs, alerts, report generation, and review workflows
    work without external services.
-   Test restart and recovery behavior after a power loss or service
    failure.

**Offline operation is not guaranteed merely because the application is
running on a local computer.** The complete dependency chain must be
tested with internet access disabled. Updates, dependency installation,
model downloads, and security patches may still require a controlled
online preparation process.

### Suggested local service layout

``` text
Local field workstation / server
├── React frontend
├── M1 backend API
├── M4 intelligence service
├── Local detection model weights
├── Local LLM runtime and model weights
└── PostgreSQL database
```

The deployment may use one machine or multiple machines on a secured
local network, depending on available hardware and performance
requirements.

## Local development setup

These instructions are a starting point. Use the dependency files and
environment configuration in the branch you intend to run.

### Prerequisites

-   Git
-   Python version supported by the selected backend and intelligence
    dependencies
-   Node.js version supported by the frontend
-   PostgreSQL
-   Local detection-model weights
-   A compatible local LLM runtime and model weights if running
    intelligence generation

### 1. Clone the private repository

``` bash
git clone <PRIVATE_REPOSITORY_URL>
cd VanDrishti
```

Use the repository URL provided to authorized team members. Do not
replace it with a public URL.

### 2. Start PostgreSQL

Start the local PostgreSQL service and verify that it is accepting
connections:

``` bash
pg_isready
```

Create a database and a least-privilege application user according to
your local configuration. Set the database connection string through the
backend's environment configuration. Do not commit credentials.

### 3. Start the M1 backend

From the backend directory, activate the project's Python virtual
environment, install the dependencies listed by the project, configure
the environment variables, and run the API using the project's
documented entry point.

The current local development setup has used port `8001` for M1:

``` bash
cd backend
# Activate the existing virtual environment.
# Install dependencies from the applicable requirements file.
# Configure the database URL and other required environment variables.
uvicorn app.main:app --host 127.0.0.1 --port 8001
```

If the selected branch uses a different application entry point or
configuration, follow that branch's instructions instead.

### 4. Start the M4 intelligence service

Activate the M4 environment, install its declared dependencies,
configure the local LLM runtime and model path, and start the
intelligence API using the entry point available in the selected branch.

The current local development setup has used port `8000` for M4. Confirm
the correct module path and command in that branch before starting it.

### 5. Start the frontend

From the frontend directory:

``` bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

Configure the frontend's API URLs to point to the local backend
services. Check CORS settings if the frontend and APIs use different
origins.

### 6. Verify the complete workflow

Before a demonstration or field deployment, verify all of the following:

-   The frontend can reach the backend.
-   Video uploads and analysis complete successfully.
-   Detections and evidence are stored in PostgreSQL.
-   Intelligence processing works with the local model.
-   Numeric validation and review flows behave as expected.
-   Alerts are generated only when the relevant detection and alert
    rules are implemented and validated.
-   The application does not make external network requests during
    offline operation.

Do not assume that an endpoint returning HTTP 200 proves that the
complete analysis or alert workflow is correct.

## Testing and validation

Testing should cover both software correctness and field suitability.

-   **API and integration tests:** Verify service communication, schema
    validation, database writes, and error handling.
-   **Detection evaluation:** Measure precision, recall, and
    false-positive/false-negative behavior on representative camera-trap
    footage.
-   **Fire-alert validation:** Test against labelled fire/smoke footage
    and hard negative examples; measure missed events and false alarms
    before operational use.
-   **LLM output validation:** Check generated claims against the
    supplied evidence, validate numeric values, and retain a
    human-review path.
-   **ReID evaluation:** Test identity consistency across lighting,
    camera angles, occlusion, and different cameras before claiming
    cross-camera identification.
-   **Offline acceptance test:** Disconnect the internet and test the
    entire workflow, including model loading, report generation, alerts,
    review, and service restarts.
-   **Security review:** Test authentication, authorization, upload
    restrictions, secret handling, database permissions, and exposure of
    sensitive location data.

A prototype alert or model prediction should not be treated as a
confirmed poaching event, fire, or animal identity without the required
verification.

## Repository organization

The exact layout varies by branch. The integrated project has used
directories and files similar to these:

``` text
VanDrishti/
├── backend/        # M1 API, database models, migrations, and routes
├── frontend/       # React/Vite monitoring dashboard
├── intelligence/   # M4 intelligence processing and service
├── contracts/      # JSON schemas and inter-module contracts
├── docs/           # Project documentation, where present
└── README.md
```

Use the branch containing the integrated files as the source of truth.
Do not assume every directory is present on every branch.


## Team and Academic Information

| Team Member     | Roll Number     |
|-----------------|-----------------|
| Anshika Sharma  | `<Roll number>` |
| Anurag Kushwaha | 2501921520091   |
| Anshika Khanna  | `<Roll number>` |
| Apoorva         | `<Roll number>` |

**Department:** Computer Science and Artificial Intelligence (CS AI)

**Institution:** GL Bajaj Institute of Technology and Management

**Academic Year:** 2026–27

## Responsible use

VanDrishti is intended to support authorized wildlife conservation and
monitoring. Access to sensitive observations should be limited to
trusted personnel. Detection results and generated intelligence may be
wrong and should be reviewed before consequential action is taken.

Do not use demonstration screenshots, public reports, or source-control
history to reveal protected species locations or operational details.

## License and distribution

This project is maintained as a private academic prototype. Do not
assume that the code, trained weights, datasets, or third-party
components share the same license.

Before redistributing any component, review its license and the
dataset's terms of use. Keep the repository private while sensitive-data
handling and distribution permissions are being reviewed.

------------------------------------------------------------------------

*VanDrishti --- local-first wildlife monitoring for responsible
conservation.*
