# Sync Rule

> [!IMPORTANT]
> This document reflects the current development baseline and the planned target architecture.
> Some runtime, diagnostic, and verification details are still under implementation and may change.

## Purpose

This document defines the fixed sync rule between `src/capl` and `cfg/channel_assign`.

## Source Of Truth

- `canoe/src/capl/**` is the source of truth
- `canoe/cfg/channel_assign/**` is the GUI import mirror

## Mandatory Rule

Whenever a CAPL node is changed in `src/capl/`, mirror the same active change into `cfg/channel_assign/` before treating the update as complete.

## Completion Gate

A CAPL change is not complete until all of the following are true:

1. source update is done in `src/capl/`
2. mirror update is done in `cfg/channel_assign/`
3. CAPL compile is clean
4. runtime result is reviewed separately if the change affects behavior

## Non-Rules

- do not treat `cfg/channel_assign/` as an independent source tree
- do not infer runtime success from compile success alone
- do not widen DBC visibility or transport settings as a shortcut for stale source/mirror drift