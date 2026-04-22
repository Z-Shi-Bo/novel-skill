import re
from pathlib import Path

import yaml

REQUIRED_MANIFEST_KEYS = {
    'title',
    'slug',
    'genre',
    'style',
    'audience',
    'language',
    'research_mode',
    'strong_sync',
    'current_phase',
    'current_volume',
    'current_chapter',
    'last_updated',
}
VALID_RESEARCH_MODES = {'off', 'on-demand', 'strict'}
VALID_PHASES = {
    'initialized',
    'brief',
    'bible',
    'characters',
    'outline',
    'drafted',
    'reviewed',
    'finalized',
    'synced',
}


def run_named_validators(workspace: Path, names: list[str]) -> list[str]:
    validators = {'manifest_contract': manifest_contract}
    errors = []
    for name in names:
        validator = validators.get(name)
        if validator is None:
            errors.append(f'Unknown validator: {name}')
            continue
        errors.extend(validator(workspace))
    return errors


def manifest_contract(workspace: Path) -> list[str]:
    manifests = list(workspace.glob('projects/*/project_manifest.yaml'))
    if len(manifests) != 1:
        return [f'Expected exactly one manifest, found {len(manifests)}.']
    data = yaml.safe_load(manifests[0].read_text(encoding='utf-8')) or {}
    errors = missing_manifest_keys(data)
    if errors:
        return errors
    return validate_manifest_values(data)


def missing_manifest_keys(data: dict) -> list[str]:
    missing = REQUIRED_MANIFEST_KEYS - set(data)
    if not missing:
        return []
    joined = ', '.join(sorted(missing))
    return [f'Manifest missing keys: {joined}']


def validate_manifest_values(data: dict) -> list[str]:
    errors = []
    if data['research_mode'] not in VALID_RESEARCH_MODES:
        errors.append(f"Invalid research_mode: {data['research_mode']}")
    if data['strong_sync'] not in {'true', 'false'}:
        errors.append(f"Invalid strong_sync: {data['strong_sync']}")
    if data['current_phase'] not in VALID_PHASES:
        errors.append(f"Invalid current_phase: {data['current_phase']}")
    errors.extend(validate_non_negative_int(data, 'current_volume'))
    errors.extend(validate_non_negative_int(data, 'current_chapter'))
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(data['last_updated'])):
        errors.append('last_updated must use YYYY-MM-DD.')
    return errors


def validate_non_negative_int(data: dict, key: str) -> list[str]:
    try:
        value = int(str(data[key]))
    except ValueError:
        return [f'{key} must be a non-negative integer string.']
    if value < 0:
        return [f'{key} must be >= 0.']
    return []
