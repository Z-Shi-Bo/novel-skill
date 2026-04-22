from pathlib import Path

import yaml

REQUIRED_CASE_KEYS = {"id", "suite", "purpose", "fixture", "steps"}
REQUIRED_STEP_KEYS = {"name", "prompt", "expect"}


def load_cases(cases_dir: Path, suite: str | None, case_id: str | None) -> list[dict]:
    cases = []
    for path in sorted(cases_dir.glob('*.yaml')):
        case = yaml.safe_load(path.read_text(encoding='utf-8')) or {}
        validate_case(case, path)
        if suite and case['suite'] != suite:
            continue
        if case_id and case['id'] != case_id:
            continue
        case['_path'] = str(path)
        cases.append(case)
    if not cases:
        raise FileNotFoundError('No cases matched the provided filters.')
    return cases


def validate_case(case: dict, path: Path) -> None:
    missing = REQUIRED_CASE_KEYS - set(case)
    if missing:
        joined = ', '.join(sorted(missing))
        raise ValueError(f'{path} missing case keys: {joined}')
    if not isinstance(case['steps'], list) or not case['steps']:
        raise ValueError(f'{path} must define at least one step.')
    for index, step in enumerate(case['steps'], start=1):
        missing = REQUIRED_STEP_KEYS - set(step)
        if missing:
            joined = ', '.join(sorted(missing))
            raise ValueError(
                f'{path} step {index} missing step keys: {joined}'
            )
