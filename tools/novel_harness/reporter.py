import json
from pathlib import Path


def write_reports(run_root: Path, summary: dict) -> None:
    markdown_path = run_root / 'summary.md'
    json_path = run_root / 'summary.json'
    markdown_path.write_text(render_markdown(summary), encoding='utf-8')
    json_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )


def render_markdown(summary: dict) -> str:
    lines = [
        '# Novel Harness Report',
        '',
        f"- run_id: `{summary['run_id']}`",
        f"- suite: `{summary['suite']}`",
        f"- cases_total: `{summary['cases_total']}`",
        f"- cases_passed: `{summary['cases_passed']}`",
        f"- cases_failed: `{summary['cases_failed']}`",
        '',
    ]
    for case in summary['cases']:
        status = 'PASS' if case['passed'] else 'FAIL'
        lines.extend([
            f"## {case['id']} [{status}]",
            '',
            f"- purpose: {case['purpose']}",
            f"- workspace: `{case['workspace']}`",
            '',
        ])
        for step in case['steps']:
            step_status = 'PASS' if step['passed'] else 'FAIL'
            lines.append(f"### {step['name']} [{step_status}]")
            lines.append('')
            lines.append(f"- duration_sec: `{step['duration_sec']}`")
            lines.append(f"- last_message: `{step['last_message_path']}`")
            lines.append(f"- stdout: `{step['stdout_path']}`")
            lines.append(f"- stderr: `{step['stderr_path']}`")
            if step['errors']:
                lines.append('- errors:')
                lines.extend(f'  - {error}' for error in step['errors'])
            lines.append('')
    return '\n'.join(lines)
