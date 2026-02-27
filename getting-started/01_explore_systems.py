"""Browse systems, configurations, snapshots, and files in Istari.

Usage:
    python getting-started/01_explore_systems.py
    python getting-started/01_explore_systems.py --system-id <SYSTEM_ID>
"""
import argparse
import sys
from pathlib import Path

# Allow imports from repo root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from istari_client import get_client


def list_systems(client, show_all=False):
    """List all systems the current user can access."""
    archive_status = "all" if show_all else "active"
    page = client.list_systems(page=1, size=20, archive_status=archive_status)
    print(f"Systems ({page.total} total):\n")
    for system in page.items:
        print(f"  {system.display_name}")
        print(f"    ID: {system.id}")
        if system.description:
            print(f"    Description: {system.description}")
        print()
    return page.items


def explore_system(client, system_id):
    """Drill into a system: configurations → snapshots → files."""
    system = client.get_system(system_id)
    print(f"System: {system.display_name}")
    print(f"  ID: {system.id}")
    print(f"  Description: {system.description or '—'}\n")

    # List configurations
    configs = client.list_configurations(system_id, page=1, size=50)
    print(f"Configurations ({configs.total}):\n")
    for config in configs.items:
        print(f"  {config.display_name}")
        print(f"    Config ID: {config.id}")

        # List snapshots for this configuration
        snapshots = client.list_snapshots(config.id, page=1, size=10)
        for snap in snapshots.items:
            print(f"    Snapshot: {snap.id}")

            # List files in this snapshot
            items = client.list_snapshot_items(snap.id, page=1, size=50)
            for item in items.items:
                rev = item.file_revision
                if rev:
                    print(f"      - {rev.name} ({rev.size:,} bytes)")
        print()


def main():
    parser = argparse.ArgumentParser(description="Explore Istari systems")
    parser.add_argument(
        "--system-id",
        type=str,
        default=None,
        help="Drill into a specific system by ID",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Include archived systems",
    )
    args = parser.parse_args()

    client = get_client()
    user = client.get_current_user()
    print(f"Connected as: {user.display_name} ({user.email})\n")

    if args.system_id:
        explore_system(client, args.system_id)
    else:
        list_systems(client, show_all=args.all)


if __name__ == "__main__":
    main()
