import json
import argparse
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from time import sleep
# from dotenv import load_dotenv
from istari_digital_client import (
    Client,
    Configuration,
    Job,
    JobStatusName,
    Model,
)

###
# Initial Setup
###
# load_dotenv()

NTOP_MODEL_NAME = "nTopGrp3_v6"
NTOP_MODEL_INPUT_JSON = "v4_input.json"

# OPERATING_SYSTEM = "Windows 10"
OPERATING_SYSTEM = "RHEL 8"

# Create temporary directory for intermediate files
USE_TEMP_DIR = False

if USE_TEMP_DIR:
    temp_dir = TemporaryDirectory()
    TEMP_PATH = Path(temp_dir.name)
    print(f"Using temp directory: {TEMP_PATH}")
else:
    TEMP_PATH = Path(__file__).resolve().parent
    print(f"Using parent directory: {TEMP_PATH}")

# Model file to use
NTOP_MODEL_FILE = Path(__file__).resolve().with_name(
    f"{NTOP_MODEL_NAME}.ntop"
)
input_json_path = Path(__file__).resolve().with_name(NTOP_MODEL_INPUT_JSON)

# Configure client with environment variables
config = Configuration(
    registry_url="REPLACE_WITH_REGISTRY_URL",
    registry_auth_token=(
        "REPLACE_WITH_REGISTRY_AUTH_TOKEN"
    ),
)

# Make a new client
client = Client(config)


def monitor_job(job: Job, description: str = "Job") -> bool:
    """Poll job status until completion or failure."""
    while True:
        sleep(5)
        job = client.get_job(job.id)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {description} status: {job.status.name.value}")
        if job.status.name in {
            JobStatusName.COMPLETED,
            JobStatusName.FAILED,
        }:
            break

    if job.status.name == JobStatusName.COMPLETED:
        print(f"[{timestamp}]{description} completed successfully!")
        return True
    else:
        print(f"[{timestamp}]{description} FAILED!")
        return False


def main() -> None:
    """Main function to run nTop integration test."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Run nTop model integration test"
    )
    parser.add_argument(
        "--agent_id",
        type=str,
        default=None,
        help=(
            "Specific agent ID to assign jobs to "
            "(default: None for auto-assignment)"
        )
    )
    parser.add_argument(
        "--model_id",
        type=str,
        default=None,
        help=(
            "Existing model ID to use instead of uploading a new model "
            "(default: None to upload model)"
        )
    )
    args = parser.parse_args()

    ###
    # Upload nTop model (only if not using existing model)
    ###
    model_id_to_use: str
    if args.model_id:
        print(f"Using existing model ID: {args.model_id}")
        model_id_to_use = args.model_id
    else:
        print("Uploading nTop model...")
        ntop_model: Model = client.add_model(
            path=NTOP_MODEL_FILE,
            description="nTop Model File",
            display_name=NTOP_MODEL_NAME,
        )
        model_id_to_use = ntop_model.id
        print(f"Uploaded nTop model with {ntop_model.id=} "
            f"{ntop_model.revision.id=}")

    ###
    # Run @ntop:run_model
    # This runs the nTop model with the configured inputs passed as a
    # parameter
    ###
    print("\nLoading input JSON for run...")
    with open(input_json_path, "r") as f:
        input_json_data = json.load(f)

    print("\nStarting @ntop:run_model...")
    print(f"Using model_id: {model_id_to_use}")

    run_job: Job = client.add_job(
        model_id=model_id_to_use,
        function="@ntop:run_model",
        tool_name="ntopcl",
        tool_version="5.30",
        assigned_agent_id=args.agent_id,
        operating_system=OPERATING_SYSTEM,
        parameters={"ntop_input_json": input_json_data},
    )
    print(f"Run job created with {run_job.id=}")

    if not monitor_job(run_job, "Run"):
        print("Run failed, exiting...")
        exit(1)

    # Refresh model to get final artifacts
    final_model = client.get_model(model_id_to_use)
    print(f"\nFinal model artifacts ({len(final_model.artifacts)}):")
    for artifact in final_model.artifacts:
        print(f"  * {artifact.name} (id: {artifact.id})")

    # Cleanup temp directory
    if USE_TEMP_DIR:
        temp_dir.cleanup()

    print("\n✓ nTop integration completed successfully!")


if __name__ == "__main__":
    main()
