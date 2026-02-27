"""Upload a job output as a new revision of an existing model.

This demonstrates the Istari versioning workflow:
  1. Download an artifact from a completed job
  2. Re-upload it as a new revision of the original model
  3. Verify both revisions exist

Usage:
    python getting-started/02_version_model.py --model-id <MODEL_ID> --file <PATH>
    python getting-started/02_version_model.py --model-id <MODEL_ID> --file output.ntop --name "v2 — High Endurance"
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from istari_client import get_client


def main():
    parser = argparse.ArgumentParser(
        description="Upload a new revision of an existing model"
    )
    parser.add_argument(
        "--model-id",
        type=str,
        required=True,
        help="Model ID to add a new revision to",
    )
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to the file to upload as a new revision",
    )
    parser.add_argument(
        "--name",
        type=str,
        default=None,
        help="Version name (e.g. 'v2 — High Endurance')",
    )
    parser.add_argument(
        "--description",
        type=str,
        default=None,
        help="Description of what changed in this version",
    )
    args = parser.parse_args()

    client = get_client()
    file_path = Path(args.file)

    if not file_path.exists():
        print(f"Error: file not found: {file_path}")
        sys.exit(1)

    # Show current state
    model = client.get_model(args.model_id)
    print(f"Model: {model.display_name}")
    print(f"  Current revisions: {len(model.file.revisions)}")
    for rev in model.file.revisions:
        print(f"    - {rev.name} ({rev.size:,} bytes)")

    # Upload new revision
    print(f"\nUploading new revision from: {file_path.name}")
    updated = client.update_model(
        model_id=args.model_id,
        path=file_path,
        version_name=args.name,
        description=args.description,
    )

    # Show updated state
    refreshed = client.get_model(args.model_id)
    print(f"\nModel now has {len(refreshed.file.revisions)} revisions:")
    for rev in refreshed.file.revisions:
        print(f"  - {rev.name} ({rev.size:,} bytes)")

    print("\nDone! View the diff in Istari UI.")


if __name__ == "__main__":
    main()
