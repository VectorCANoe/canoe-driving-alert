from __future__ import annotations

import argparse
import sys

from cliops.common import SCRIPTS, run_cmd


def cmd_package_build_exe(args: argparse.Namespace) -> int:
    cmd = [sys.executable, str(SCRIPTS / 'release' / 'build_sdv_exe.py'), '--mode', args.mode]
    if args.clean:
        cmd.append('--clean')
    return run_cmd(cmd)


def cmd_package_bundle_portable(args: argparse.Namespace) -> int:
    cmd = [sys.executable, str(SCRIPTS / 'release' / 'build_portable_bundle.py')]
    if args.clean:
        cmd.append('--clean')
    if args.rebuild_exe:
        cmd.append('--rebuild-exe')
    if args.mode:
        cmd.extend(['--mode', args.mode])
    if args.output_dir:
        cmd.extend(['--output-dir', args.output_dir])
    if args.bundle_name:
        cmd.extend(['--bundle-name', args.bundle_name])
    if args.zip_name:
        cmd.extend(['--zip-name', args.zip_name])
    return run_cmd(cmd)


def cmd_package_validate_contract(args: argparse.Namespace) -> int:
    cmd = [sys.executable, str(SCRIPTS / 'release' / 'validate_release_contract.py')]
    return run_cmd(cmd)


def cmd_package_clean(args: argparse.Namespace) -> int:
    cmd = [sys.executable, str(SCRIPTS / 'release' / 'clean_generated_outputs.py'), '--scope', args.scope]
    if args.run_id:
        cmd.extend(['--run-id', args.run_id])
    if args.phase:
        cmd.extend(['--phase', args.phase])
    if args.all_runs:
        cmd.append('--all-runs')
    if args.yes:
        cmd.append('--yes')
    return run_cmd(cmd)
