import os
import shutil
import subprocess
import time
from pathlib import Path


def run_codex_step(
    prompt: str,
    workspace: Path,
    codex_home: Path,
    last_message_path: Path,
    stdout_path: Path,
    stderr_path: Path,
    timeout_sec: int,
) -> dict:
    env = os.environ.copy()
    env['CODEX_HOME'] = str(codex_home)
    cmd = build_command(prompt, workspace, last_message_path)
    started = time.time()
    timed_out = False
    forced_stop = False
    with stdout_path.open('w', encoding='utf-8') as stdout_file:
        with stderr_path.open('w', encoding='utf-8') as stderr_file:
            process = subprocess.Popen(
                cmd,
                cwd=workspace,
                stdout=stdout_file,
                stderr=stderr_file,
                text=True,
                env=env,
            )
            exit_code, timed_out, forced_stop = wait_for_process(
                process,
                last_message_path,
                timeout_sec,
            )
    duration_sec = round(time.time() - started, 2)
    return {
        'exit_code': exit_code,
        'timed_out': timed_out,
        'forced_stop': forced_stop,
        'duration_sec': duration_sec,
        'stdout': read_text(stdout_path),
        'stderr': read_text(stderr_path),
        'last_message': read_text(last_message_path),
        'command': cmd,
    }


def build_command(prompt: str, workspace: Path, last_message_path: Path) -> list[str]:
    reasoning = os.environ.get('NOVEL_HARNESS_REASONING', 'medium')
    return [
        resolve_codex_bin(),
        'exec',
        '--skip-git-repo-check',
        '--ephemeral',
        '-c',
        f'model_reasoning_effort="{reasoning}"',
        '--color',
        'never',
        '-C',
        str(workspace),
        '-o',
        str(last_message_path),
        prompt,
    ]


def wait_for_process(
    process: subprocess.Popen,
    last_message_path: Path,
    timeout_sec: int,
) -> tuple[int | None, bool, bool]:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        exit_code = process.poll()
        if exit_code is not None:
            return exit_code, False, False
        time.sleep(1)
    if read_text(last_message_path):
        terminate_process(process)
        return 0, False, True
    terminate_process(process)
    return None, True, False


def terminate_process(process: subprocess.Popen) -> None:
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=10)


def resolve_codex_bin() -> str:
    explicit = os.environ.get('CODEX_BIN')
    if explicit:
        return explicit
    for candidate in ('codex.cmd', 'codex'):
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    raise FileNotFoundError('Unable to locate Codex CLI. Set CODEX_BIN if needed.')


def read_text(path: Path) -> str:
    if not path.exists():
        return ''
    return path.read_text(encoding='utf-8').strip()
