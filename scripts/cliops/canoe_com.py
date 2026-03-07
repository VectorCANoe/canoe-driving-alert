"""CANoe COM bridge for operator CLI commands.

This module centralizes CANoe COM access so command handlers stay thin.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class CanoeComError(RuntimeError):
    """Raised for CANoe COM interaction failures."""


@dataclass(frozen=True)
class DoctorCheck:
    name: str
    ok: bool
    detail: str


class CanoeComBridge:
    """Thin wrapper around CANoe COM API access patterns used by this project."""

    def __init__(self, app: Any):
        self._app = app

    @classmethod
    def connect(cls) -> "CanoeComBridge":
        try:
            import win32com.client as win32com_client  # type: ignore
        except Exception as ex:  # pragma: no cover - depends on host env
            raise CanoeComError(f"pywin32 import failed: {ex}") from ex
        try:
            app = win32com_client.Dispatch("CANoe.Application")
        except Exception as ex:  # pragma: no cover - depends on host env
            raise CanoeComError(f"CANoe COM attach failed: {ex}") from ex
        return cls(app)

    def measurement_running(self) -> bool:
        return bool(self._app.Measurement.Running)

    def measurement_start(self) -> None:
        self._app.Measurement.Start()

    def measurement_stop(self) -> None:
        self._app.Measurement.Stop()

    def measurement_reset(self) -> None:
        # Reset behavior with COM-safe sequence.
        if self.measurement_running():
            self.measurement_stop()
        self.measurement_start()

    def resolve_sysvar(self, namespace: str, variable: str) -> Any:
        attempts = [
            lambda: self._app.System.Namespaces(namespace).Variables(variable),
            lambda: self._app.System.Namespaces(namespace).Variables.Item(variable),
            lambda: self._app.System.Namespaces.Item(namespace).Variables(variable),
            lambda: self._app.System.Namespaces.Item(namespace).Variables.Item(variable),
            lambda: self._app.Configuration.SystemVariables.Namespaces(namespace).Variables(variable),
            lambda: self._app.Configuration.SystemVariables.Namespaces(namespace).Variables.Item(variable),
        ]
        for attempt in attempts:
            try:
                return attempt()
            except Exception:
                continue
        raise CanoeComError(f"System variable not found: {namespace}::{variable}")

    def get_sysvar(self, namespace: str, variable: str) -> Any:
        return self.resolve_sysvar(namespace, variable).Value

    def set_sysvar(self, namespace: str, variable: str, value: Any) -> Any:
        sv = self.resolve_sysvar(namespace, variable)
        sv.Value = value
        return sv.Value

    def call_capl_function(self, function_name: str, args: list[Any] | None = None) -> Any:
        args = args or []
        attempts = [
            lambda: self._app.CAPL.GetFunction(function_name).Call(*args),
            lambda: self._app.CAPL.Functions(function_name).Call(*args),
            lambda: self._app.CAPL.Function(function_name).Call(*args),
            lambda: self._app.CAPL.GetFunction(function_name).Call(args),
        ]
        last_error: Exception | None = None
        for attempt in attempts:
            try:
                return attempt()
            except Exception as ex:
                last_error = ex
                continue
        if last_error is None:
            raise CanoeComError(f"CAPL function call failed: {function_name}")
        raise CanoeComError(f"CAPL function call failed ({function_name}): {last_error}") from last_error

    def run_doctor(self, required_vars: list[tuple[str, str]], ensure_running: bool = False) -> list[DoctorCheck]:
        checks: list[DoctorCheck] = [DoctorCheck("CANoe COM attach", True, "ok")]
        try:
            running = self.measurement_running()
            checks.append(DoctorCheck("Measurement running", running, "running" if running else "stopped"))
            if ensure_running and not running:
                self.measurement_start()
                checks.append(DoctorCheck("Measurement auto-start", True, "started"))
        except Exception as ex:
            checks.append(DoctorCheck("Measurement status", False, str(ex)))

        for ns_name, var_name in required_vars:
            try:
                _ = self.get_sysvar(ns_name, var_name)
                checks.append(DoctorCheck(f"SysVar {ns_name}::{var_name}", True, "ok"))
            except Exception as ex:
                checks.append(DoctorCheck(f"SysVar {ns_name}::{var_name}", False, str(ex)))
        return checks

