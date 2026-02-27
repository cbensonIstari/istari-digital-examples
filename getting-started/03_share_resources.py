"""Share an Istari system and its files with a teammate by email.

Note: Systems and files must be shared separately in Istari.

Usage:
    python getting-started/03_share_resources.py --system-id <ID> --email user@example.com
    python getting-started/03_share_resources.py --system-id <ID> --email user@example.com --role viewer
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from istari_client import get_client
from istari_digital_client import AccessSubjectType, AccessRelation


def main():
    parser = argparse.ArgumentParser(
        description="Share a system and its files with a user"
    )
    parser.add_argument(
        "--system-id",
        type=str,
        required=True,
        help="System ID to share",
    )
    parser.add_argument(
        "--email",
        type=str,
        required=True,
        help="Email of the user to share with",
    )
    parser.add_argument(
        "--role",
        type=str,
        default="editor",
        choices=["viewer", "editor"],
        help="Access level (default: editor)",
    )
    args = parser.parse_args()

    client = get_client()
    relation = (
        AccessRelation.EDITOR if args.role == "editor" else AccessRelation.VIEWER
    )

    # Share the system
    print(f"Sharing system {args.system_id} with {args.email} as {args.role}...")
    client.create_access_by_email(
        resource_id=args.system_id,
        subject_type=AccessSubjectType.USER,
        subject_email=args.email,
        relation=relation,
    )
    print("  System shared.")

    # Collect all file IDs from the system's configurations
    configs = client.list_configurations(args.system_id, page=1, size=50)
    file_ids = set()

    for config in configs.items:
        snapshots = client.list_snapshots(config.id, page=1, size=10)
        for snap in snapshots.items:
            items = client.list_snapshot_items(snap.id, page=1, size=100)
            for item in items.items:
                if item.file_revision and item.file_revision.file_id:
                    file_ids.add(item.file_revision.file_id)

    # Also collect files from model artifacts
    models = client.list_models(system_id=args.system_id, page=1, size=100)
    for model in models.items:
        if model.file:
            file_ids.add(model.file.id)
        for artifact in model.artifacts:
            if artifact.file:
                file_ids.add(artifact.file.id)

    # Share each file
    print(f"Sharing {len(file_ids)} files...")
    for file_id in file_ids:
        try:
            client.create_access_by_email(
                resource_id=file_id,
                subject_type=AccessSubjectType.USER,
                subject_email=args.email,
                relation=relation,
            )
        except Exception as e:
            print(f"  Warning: could not share file {file_id}: {e}")

    print(f"\nDone! Shared system + {len(file_ids)} files with {args.email}.")


if __name__ == "__main__":
    main()
