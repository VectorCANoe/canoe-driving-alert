# Run Procedure

> [!IMPORTANT]
> This document reflects the current development baseline and the planned target architecture.
> Some runtime, diagnostic, and verification details are still under implementation and may change.

## Purpose

This document defines the standard import, compile, run, and evidence procedure for the active CANoe baseline.

## Procedure

1. open the active configuration in CANoe GUI
2. restore required node visibility and database assignment
3. confirm panel and SysVar surfaces are loaded
4. sync active CAPL changes from `src/capl/` into `cfg/channel_assign/`
5. compile CAPL nodes
6. start measurement or native Test Unit execution
7. capture verdict, report, and supporting evidence
8. update reviewer-facing verification records if the run is official

## Expected Outputs

- compile result
- runtime verdict or Test Unit verdict
- report path when native Test Unit assets are used
- screenshot or write-window capture when required by the evidence policy

## Working Rule

Treat compile success and runtime success as separate gates.
When runtime delivery is still uncertain, report the run as pending rather than inferring correctness from configuration alone.