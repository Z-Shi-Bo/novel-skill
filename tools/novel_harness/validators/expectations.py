from pathlib import Path


def check_expectations(workspace: Path, result: dict, expect: dict) -> list[str]:
    errors = []
    errors.extend(check_files_exist(workspace, expect.get('files_exist', [])))
    errors.extend(check_files_absent(workspace, expect.get('files_absent', [])))
    errors.extend(check_dirs_exist(workspace, expect.get('dirs_exist', [])))
    errors.extend(check_text_contains('stdout', result['stdout'], expect.get('stdout_contains', [])))
    errors.extend(
        check_text_contains(
            'last_message',
            result['last_message'],
            expect.get('last_message_contains', []),
        )
    )
    errors.extend(
        check_text_any_contains(
            result['last_message'],
            expect.get('last_message_any_contains', []),
        )
    )
    return errors


def check_files_exist(workspace: Path, relative_paths: list[str]) -> list[str]:
    return [
        f'Missing expected file: {relative}'
        for relative in relative_paths
        if not (workspace / relative).is_file()
    ]


def check_files_absent(workspace: Path, relative_paths: list[str]) -> list[str]:
    return [
        f'Unexpected file exists: {relative}'
        for relative in relative_paths
        if (workspace / relative).exists()
    ]


def check_dirs_exist(workspace: Path, relative_paths: list[str]) -> list[str]:
    return [
        f'Missing expected directory: {relative}'
        for relative in relative_paths
        if not (workspace / relative).is_dir()
    ]


def check_text_contains(label: str, text: str, needles: list[str]) -> list[str]:
    errors = []
    for needle in needles:
        if needle not in text:
            errors.append(f'{label} missing required text: {needle}')
    return errors


def check_text_any_contains(text: str, needles: list[str]) -> list[str]:
    if not needles:
        return []
    if any(needle in text for needle in needles):
        return []
    joined = ', '.join(needles)
    return [f'last_message must contain at least one of: {joined}']
