import os
import re
import shutil
from pathlib import Path


def detect_source_codex_home() -> Path:
    env_home = os.environ.get('CODEX_HOME')
    return Path(env_home) if env_home else Path.home() / '.codex'


def prepare_codex_home(target: Path, repo_root: Path) -> Path:
    source = detect_source_codex_home()
    target.mkdir(parents=True, exist_ok=True)
    copy_auth_file(source, target)
    write_minimal_config(source, target)
    copy_skill_under_test(repo_root, target)
    return target


def copy_auth_file(source: Path, target: Path) -> None:
    source_path = source / 'auth.json'
    if not source_path.exists():
        raise FileNotFoundError(f'Missing required Codex auth file: {source_path}')
    shutil.copy2(source_path, target / 'auth.json')


def write_minimal_config(source: Path, target: Path) -> None:
    config_text = (source / 'config.toml').read_text(encoding='utf-8')
    model = extract_value(config_text, 'model') or 'gpt-5.4'
    provider = extract_value(config_text, 'model_provider') or 'openai'
    provider_name = extract_provider_value(config_text, provider, 'name') or provider
    base_url = extract_provider_value(config_text, provider, 'base_url')
    rendered = [
        f'model = "{model}"',
        f'model_provider = "{provider}"',
        'model_reasoning_effort = "medium"',
        'approval_policy = "never"',
        'sandbox_mode = "danger-full-access"',
        'network_access = "enabled"',
        'disable_response_storage = true',
        '',
        f'[model_providers.{provider}]',
    ]
    if base_url:
        rendered.append(f'base_url = "{base_url}"')
    rendered.append(f'name = "{provider_name}"')
    (target / 'config.toml').write_text('\n'.join(rendered) + '\n', encoding='utf-8')


def extract_value(config_text: str, key: str) -> str | None:
    match = re.search(rf'^{re.escape(key)}\s*=\s*"([^"]+)"', config_text, re.M)
    return match.group(1) if match else None


def extract_provider_value(config_text: str, provider: str, key: str) -> str | None:
    section = rf'^\[model_providers\.{re.escape(provider)}\]$(.*?)(?=^\[|\Z)'
    match = re.search(section, config_text, re.M | re.S)
    if not match:
        return None
    return extract_value(match.group(1), key)


def copy_skill_under_test(repo_root: Path, target: Path) -> None:
    source_skill = repo_root / 'skills' / 'novel'
    if not source_skill.exists():
        raise FileNotFoundError(f'Missing skill under test: {source_skill}')
    dest_skill = target / 'skills' / 'novel'
    shutil.copytree(source_skill, dest_skill, dirs_exist_ok=True)
