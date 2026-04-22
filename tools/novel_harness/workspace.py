import shutil
from pathlib import Path


def prepare_case_directories(run_root: Path, case_id: str) -> dict[str, Path]:
    case_root = run_root / case_id
    paths = {
        'case_root': case_root,
        'workspace': case_root / 'workspace',
        'codex_home': case_root / 'codex-home',
        'artifacts': case_root / 'artifacts',
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def seed_workspace(workspace: Path, fixture_dir: Path) -> None:
    if not fixture_dir.exists():
        raise FileNotFoundError(f'Missing fixture directory: {fixture_dir}')
    shutil.copytree(fixture_dir, workspace, dirs_exist_ok=True)
