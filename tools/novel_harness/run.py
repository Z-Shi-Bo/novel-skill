import argparse
from datetime import datetime
from pathlib import Path

from case_loader import load_cases
from codex_adapter import run_codex_step
from codex_home import prepare_codex_home
from reporter import write_reports
from validators.contracts import run_named_validators
from validators.expectations import check_expectations
from workspace import prepare_case_directories, seed_workspace


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Run Codex $novel regression cases.')
    parser.add_argument('--suite', default='smoke', help='Case suite to run.')
    parser.add_argument('--case', dest='case_id', help='Run one case by id.')
    parser.add_argument(
        '--report-dir',
        help='Override reports directory. Defaults to tests/reports/runs/<run-id>.',
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[2]
    cases = load_cases(repo_root / 'tests' / 'cases', args.suite, args.case_id)
    run_root = build_run_root(repo_root, args.report_dir)
    reports = [execute_case(case, repo_root, run_root) for case in cases]
    summary = build_summary(args.suite, run_root, reports)
    write_reports(run_root, summary)
    print(f"[novel-harness] report: {run_root / 'summary.md'}")
    return 1 if summary['cases_failed'] else 0


def build_run_root(repo_root: Path, override: str | None) -> Path:
    if override:
        root = Path(override)
    else:
        run_id = datetime.now().strftime('%Y%m%d-%H%M%S')
        root = repo_root / 'tests' / 'reports' / 'runs' / run_id
    root.mkdir(parents=True, exist_ok=True)
    return root


def execute_case(case: dict, repo_root: Path, run_root: Path) -> dict:
    paths = prepare_case_directories(run_root, case['id'])
    fixture_dir = repo_root / 'tests' / 'fixtures' / case['fixture']
    seed_workspace(paths['workspace'], fixture_dir)
    prepare_codex_home(paths['codex_home'], repo_root)
    steps = []
    for index, step in enumerate(case['steps'], start=1):
        step_report = execute_step(step, index, paths)
        steps.append(step_report)
        if not step_report['passed']:
            break
    return {
        'id': case['id'],
        'purpose': case['purpose'],
        'passed': all(step['passed'] for step in steps),
        'steps': steps,
        'workspace': str(paths['workspace']),
    }


def execute_step(step: dict, index: int, paths: dict[str, Path]) -> dict:
    artifacts = paths['artifacts']
    last_message_path = artifacts / f'{index:02d}-{step["name"]}-last.txt'
    stdout_path = artifacts / f'{index:02d}-{step["name"]}-stdout.txt'
    stderr_path = artifacts / f'{index:02d}-{step["name"]}-stderr.txt'
    timeout_sec = int(step.get('timeout_sec', 240))
    result = run_codex_step(
        step['prompt'],
        paths['workspace'],
        paths['codex_home'],
        last_message_path,
        stdout_path,
        stderr_path,
        timeout_sec,
    )
    errors = evaluate_step(paths['workspace'], step, result)
    return {
        'name': step['name'],
        'passed': not errors,
        'duration_sec': result['duration_sec'],
        'errors': errors,
        'last_message_path': str(last_message_path),
        'stdout_path': str(stdout_path),
        'stderr_path': str(stderr_path),
    }


def evaluate_step(workspace: Path, step: dict, result: dict) -> list[str]:
    errors = []
    if result['timed_out']:
        return ['codex exec timed out before producing a final message.']
    if result['exit_code'] != 0:
        errors.append(f"codex exec failed with exit code {result['exit_code']}")
    expect = step.get('expect', {})
    errors.extend(check_expectations(workspace, result, expect))
    validators = expect.get('validators', [])
    errors.extend(run_named_validators(workspace, validators))
    return errors


def build_summary(suite: str, run_root: Path, reports: list[dict]) -> dict:
    passed = sum(1 for report in reports if report['passed'])
    return {
        'run_id': run_root.name,
        'suite': suite,
        'cases_total': len(reports),
        'cases_passed': passed,
        'cases_failed': len(reports) - passed,
        'cases': reports,
    }


if __name__ == '__main__':
    raise SystemExit(main())
