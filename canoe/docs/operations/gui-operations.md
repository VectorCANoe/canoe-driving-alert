# GUI Operations

> [!IMPORTANT]
> This document reflects the current development baseline and the planned target architecture.
> Some runtime, diagnostic, and verification details are still under implementation and may change.

## Purpose

This document defines which CANoe operations must remain GUI-first.

## GUI-First Scope

Use the CANoe GUI for the following:

- open, save, and save-as of `canoe/cfg/*.cfg`
- generation or update of `*.cfg.ini` and `*.stcfg`
- channel mapping, hardware assignment, IL registration, and network setup
- visible node placement and multibus visibility restoration inside the active configuration

## Direct-Edit Exceptions

Direct text edits remain acceptable for:

- `canoe/project/panel/*.xvp`
- `canoe/project/sysvars/project.sysvars`
- developer-facing Markdown documentation

## Recovery Rule

If configuration integrity becomes questionable:

1. reload through CANoe GUI
2. save through CANoe GUI
3. then document the stable result in text documents

## Working Rule

Do not patch GUI-managed configuration files directly unless the task is an explicit recovery operation.
Use `canoe/cfg/GUI_ONLY_OPERATIONS.md` as the detailed local checklist when deeper GUI procedure is needed.