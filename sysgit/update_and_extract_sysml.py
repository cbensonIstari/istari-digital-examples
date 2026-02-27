"""Download, edit, re-upload, and extract a SysML v2 model.

Demonstrates the full SysGit workflow:
  1. Download a SysML model from Istari
  2. Make a text edit (e.g. update a requirement value)
  3. Re-upload as a new revision
  4. Run @istari:extract_sysmlv2 to regenerate diagrams

Usage:
    python sysgit/update_and_extract_sysml.py --model-id <MODEL_ID>
    python sysgit/update_and_extract_sysml.py --model-id <MODEL_ID> --find "1000" --replace "1500"
"""
import argparse
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from time import sleep

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from istari_client import get_client
from istari_digital_client import JobStatusName

# SysGit extraction configuration
EXTRACT_FUNCTION = "@istari:extract_sysmlv2"
TOOL_NAME = "sysgit"
TOOL_VERSION = "0.1.8"
OPERATING_SYSTEM = "Ubuntu 22.04"


def monitor_job(client, job_id, description="Job", poll_interval=5):
    """Poll job status until completion or failure."""
    while True:
        sleep(poll_interval)
        job = client.get_job(job_id)
        timestamp = datetime.now().strftime("%H:%M:%S")
        status = job.status.name.value
        print(f"  [{timestamp}] {description}: {status}")
        if job.status.name in {JobStatusName.COMPLETED, JobStatusName.FAILED}:
            return job


def main():
    parser = argparse.ArgumentParser(
        description="Update and extract a SysML v2 model"
    )
    parser.add_argument(
        "--model-id",
        type=str,
        required=True,
        help="Istari model ID for the SysML file",
    )
    parser.add_argument(
        "--find",
        type=str,
        default=None,
        help="Text to find in the SysML file",
    )
    parser.add_argument(
        "--replace",
        type=str,
        default=None,
        help="Text to replace it with",
    )
    parser.add_argument(
        "--extract-only",
        action="store_true",
        help="Skip editing, just run extraction on current model",
    )
    args = parser.parse_args()

    client = get_client()

    # Step 1: Download current model
    model = client.get_model(args.model_id)
    print(f"Model: {model.display_name}")

    if not args.extract_only:
        content = model.read_text()
        print(f"  Downloaded ({len(content):,} chars)")

        if args.find and args.replace:
            # Step 2: Edit
            count = content.count(args.find)
            if count == 0:
                print(f"  Warning: '{args.find}' not found in model.")
            else:
                content = content.replace(args.find, args.replace)
                print(f"  Replaced '{args.find}' → '{args.replace}' ({count} occurrences)")

            # Step 3: Re-upload as new revision
            with tempfile.NamedTemporaryFile(
                suffix=".sysml", mode="w", delete=False
            ) as tmp:
                tmp.write(content)
                tmp_path = Path(tmp.name)

            updated = client.update_model(
                model_id=args.model_id,
                path=tmp_path,
                description=f"Updated: {args.find} → {args.replace}",
            )
            tmp_path.unlink()
            print(f"  Uploaded as new revision")
        else:
            print("  No --find/--replace specified, skipping edit.")

    # Step 4: Run extraction
    print(f"\nSubmitting {EXTRACT_FUNCTION} job...")
    job = client.add_job(
        model_id=args.model_id,
        function=EXTRACT_FUNCTION,
        tool_name=TOOL_NAME,
        tool_version=TOOL_VERSION,
        operating_system=OPERATING_SYSTEM,
        parameters={},
    )
    print(f"Job created: {job.id}")

    final_job = monitor_job(client, job.id, "Extraction")

    if final_job.status.name == JobStatusName.COMPLETED:
        print("\nExtraction complete!")
        refreshed = client.get_model(args.model_id)
        print(f"Artifacts ({len(refreshed.artifacts)}):")
        for artifact in refreshed.artifacts:
            rev = artifact.file.revisions[0] if artifact.file.revisions else None
            name = rev.name if rev else "unknown"
            print(f"  - {name}")
    else:
        print("\nExtraction FAILED.")
        sys.exit(1)


if __name__ == "__main__":
    main()
