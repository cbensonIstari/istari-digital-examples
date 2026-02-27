"""Run an nTopology model via the Istari SDK.

Submits a @ntop:run_model job with configurable wing parameters,
polls until completion, and lists the resulting artifacts.

Usage:
    python ntop/run_ntop_model.py --model-id <MODEL_ID>
    python ntop/run_ntop_model.py --model-id <MODEL_ID> --input ntop/v4_input.json
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from time import sleep

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from istari_client import get_client
from istari_digital_client import Job, JobStatusName

# nTop job configuration
FUNCTION = "@ntop:run_model"
TOOL_NAME = "ntopcl"
TOOL_VERSION = "5.30"
OPERATING_SYSTEM = "RHEL 8"


def monitor_job(client, job_id, poll_interval=5):
    """Poll job status until completion or failure."""
    while True:
        sleep(poll_interval)
        job = client.get_job(job_id)
        timestamp = datetime.now().strftime("%H:%M:%S")
        status = job.status.name.value
        print(f"  [{timestamp}] {status}")
        if job.status.name in {JobStatusName.COMPLETED, JobStatusName.FAILED}:
            return job


def main():
    parser = argparse.ArgumentParser(description="Run nTop model in Istari")
    parser.add_argument(
        "--model-id",
        type=str,
        required=True,
        help="Istari model ID for the nTop file",
    )
    parser.add_argument(
        "--input",
        type=str,
        default=str(Path(__file__).resolve().parent / "v4_input.json"),
        help="Path to input parameters JSON (default: ntop/v4_input.json)",
    )
    parser.add_argument(
        "--agent-id",
        type=str,
        default=None,
        help="Specific agent ID to assign the job to",
    )
    args = parser.parse_args()

    client = get_client()

    # Load input parameters
    input_path = Path(args.input)
    with open(input_path) as f:
        input_data = json.load(f)

    print(f"Model ID: {args.model_id}")
    print(f"Parameters: {input_path.name}")
    for inp in input_data.get("inputs", []):
        unit = inp.get("units", "")
        print(f"  {inp['name']}: {inp['value']} {unit}")

    # Submit the job
    print(f"\nSubmitting {FUNCTION} job...")
    job: Job = client.add_job(
        model_id=args.model_id,
        function=FUNCTION,
        tool_name=TOOL_NAME,
        tool_version=TOOL_VERSION,
        assigned_agent_id=args.agent_id,
        operating_system=OPERATING_SYSTEM,
        parameters={"ntop_input_json": input_data},
    )
    print(f"Job created: {job.id}")

    # Monitor
    print("\nMonitoring...")
    final_job = monitor_job(client, job.id)

    if final_job.status.name == JobStatusName.COMPLETED:
        print("\nJob completed!")
        model = client.get_model(args.model_id)
        print(f"\nArtifacts ({len(model.artifacts)}):")
        for artifact in model.artifacts:
            rev = artifact.file.revisions[0] if artifact.file.revisions else None
            name = rev.name if rev else "unknown"
            size = f"{rev.size:,} bytes" if rev else "?"
            print(f"  - {name} ({size})")
    else:
        print("\nJob FAILED.")
        if final_job.status_history:
            for s in final_job.status_history:
                msg = getattr(s, "message", None) or ""
                print(f"  {s.name}: {msg}")
        sys.exit(1)


if __name__ == "__main__":
    main()
