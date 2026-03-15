from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BLUEPRINT = ROOT / 'product' / 'sdv_operator' / 'config' / 'native_testcase_blueprints_v1.json'
TEST_UNITS_ROOT = ROOT / 'canoe' / 'tests' / 'modules' / 'test_units'

IMPLEMENTED_ANCHORS = {
    'TC_CANOE_UT_CORE_011_ADAS_WARNING_SELECTION',
    'TC_CANOE_IT_V2_006_FAILSAFE_MIN_WARNING',
}


def esc(text: str) -> str:
    return text.replace('\\', '\\\\').replace('"', '\\"')


def load_blueprints() -> list[dict]:
    data = json.loads(BLUEPRINT.read_text(encoding='utf-8'))
    assets: list[dict] = []
    for pack in data['packs']:
        for asset in pack['assets']:
            merged = dict(asset)
            merged['pack_id'] = pack['pack_id']
            merged['pack_status'] = pack.get('status', 'mandatory')
            assets.append(merged)
    return assets


def fixture_name(asset_id: str) -> str:
    tokens = asset_id.split('_')
    filtered = [t for t in tokens if t not in {'TC', 'CANOE', 'UT', 'IT', 'NET'} and not t.isdigit()]
    return ''.join(token.title() for token in filtered)


def yaml_vtestunit(asset: dict, draft: bool) -> str:
    description_prefix = 'Draft native CANoe Test Unit skeleton' if draft else 'Native CANoe Test Unit'
    detail = asset['primary_intent'].rstrip('.')
    return (
        'version: 2.1.0\n\n'
        'test-unit-information:\n'
        f"  caption: {asset['asset_id']}\n"
        f"  description: {description_prefix} for {detail}.\n"
        'test-unit-implementation:\n'
        f"  - source-file-path: {asset['asset_id']}.vtesttree.yaml\n"
        f"  - source-file-path: {asset['asset_id']}.can\n"
    )


def yaml_vtesttree(asset: dict, draft: bool) -> str:
    scenario = asset.get('scenario_id')
    desc_prefix = 'Draft skeleton' if draft else 'Native verification'
    if scenario is not None:
        desc = f"{desc_prefix} for {asset['primary_intent']} based on validation harness scenario {scenario}."
    else:
        desc = f"{desc_prefix} for {asset['primary_intent']}."
    return (
        'version: 2.2.0\n\n'
        'test-tree:\n'
        f"  - test-fixture: {fixture_name(asset['asset_id'])}\n"
        f"    description: {desc}\n"
        '    elements:\n'
        f"      - capl-test-case: {asset['asset_id']}\n"
        f"        title: {asset['asset_id']}\n"
    )


def can_skeleton(asset: dict) -> str:
    scenario = asset.get('scenario_id')
    intent = asset['primary_intent']
    oracle_lines = asset.get('oracle_summary', [])
    evidence_lines = asset.get('evidence', [])
    timing_lines = []
    for key, value in asset.get('timing_ms', {}).items():
        timing_lines.append(f'  // - {key}: {value} ms')

    header = [
        '/*@!Encoding:65001*/',
        'includes',
        '{',
        '  #include "..\\common\\ValidationHarnessTestCommon.cin"',
        '}',
        '',
        'variables',
        '{',
        '}',
        '',
        f"export testcase {asset['asset_id']}()",
        '{',
        f'  // Dev2 blueprint intent: {intent}',
        f'  // Pack: {asset["pack_id"]}',
        '  // Draft skeleton only: Dev1 must bind exact runtime messages/signals/asserts before enabling this asset in the mandatory suite.',
    ]
    if scenario is not None:
        header.extend([
            f'  // Scenario ID: {scenario}',
            '  if (!resetValidationHarnessIfNeeded())',
            '  {',
            '    return;',
            '  }',
            '',
            f'  if (!launchScenarioAndWait({scenario}, 1500, 1200))',
            '  {',
            '    return;',
            '  }',
            '',
        ])
    else:
        header.extend([
            '  // No fixed scenarioId is assigned for this network/diagnostic asset.',
            '  // Dev1 must inject the matching traffic/request path before wiring concrete oracle asserts.',
            '  if (!resetValidationHarnessIfNeeded())',
            '  {',
            '    return;',
            '  }',
            '',
        ])

    body = []
    body.append(f'  testStepPass("blueprint-intent", "Intent: {esc(intent)}");')
    for idx, oracle in enumerate(oracle_lines, start=1):
        body.append(f'  testStepPass("oracle-guide-{idx}", "Expected: {esc(oracle)}");')
    for idx, evidence in enumerate(evidence_lines, start=1):
        body.append(f'  testStepPass("evidence-guide-{idx}", "Evidence: {esc(evidence)}");')
    if timing_lines:
        body.append('')
        body.extend(timing_lines)
    body.extend([
        '',
        '  testStepFail("oracle-hook", "Draft skeleton only. Connect concrete stimulus/oracle hooks before enabling this testcase.");',
        '',
        '  resetValidationHarnessIfNeeded();',
        '}',
        ''
    ])
    return '\n'.join(header + body)


def normalize_anchor(asset: dict, asset_dir: Path) -> None:
    (asset_dir / f"{asset['asset_id']}.vtestunit.yaml").write_text(yaml_vtestunit(asset, draft=False), encoding='utf-8')
    (asset_dir / f"{asset['asset_id']}.vtesttree.yaml").write_text(yaml_vtesttree(asset, draft=False), encoding='utf-8')


def write_draft(asset: dict, asset_dir: Path) -> None:
    asset_dir.mkdir(parents=True, exist_ok=True)
    (asset_dir / f"{asset['asset_id']}.can").write_text(can_skeleton(asset), encoding='utf-8')
    (asset_dir / f"{asset['asset_id']}.vtestunit.yaml").write_text(yaml_vtestunit(asset, draft=True), encoding='utf-8')
    (asset_dir / f"{asset['asset_id']}.vtesttree.yaml").write_text(yaml_vtesttree(asset, draft=True), encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate native CANoe testcase skeletons from Dev2 blueprints.')
    parser.add_argument('--write', action='store_true', help='write files to test_units')
    args = parser.parse_args()

    assets = load_blueprints()
    created = []
    normalized = []
    for asset in assets:
        asset_dir = TEST_UNITS_ROOT / asset['asset_id']
        if asset['asset_id'] in IMPLEMENTED_ANCHORS:
            if args.write:
                normalize_anchor(asset, asset_dir)
            normalized.append(asset['asset_id'])
            continue
        if args.write:
            write_draft(asset, asset_dir)
        created.append(asset['asset_id'])

    print('[NATIVE_TEST_SKELETONS] normalized anchors:')
    for item in normalized:
        print(f'- {item}')
    print('[NATIVE_TEST_SKELETONS] generated draft skeletons:')
    for item in created:
        print(f'- {item}')


if __name__ == '__main__':
    main()
