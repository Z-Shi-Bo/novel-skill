from __future__ import annotations

from pathlib import Path

from common import parser_with_project
from build_project_index import main as build_project_index_main
from diagnose_project import sync_review_index, sync_summary_index


def main() -> None:
    parser = parser_with_project("Sync summary and review indexes.")
    args = parser.parse_args()
    project_dir = Path(args.project)
    sync_summary_index(project_dir)
    sync_review_index(project_dir)
    # Rebuild unified project index after sync.
    import sys

    previous = sys.argv[:]
    try:
        sys.argv = ["build_project_index.py", "--project", str(project_dir)]
        build_project_index_main()
    finally:
        sys.argv = previous
    print(project_dir)


if __name__ == "__main__":
    main()
