"""CANoe COM bridge for operator CLI commands.

This module centralizes CANoe COM access so command handlers stay thin.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

from .platform_caps import require_canoe_runtime


class CanoeComError(RuntimeError):
    """Raised for CANoe COM interaction failures."""


@dataclass(frozen=True)
class DoctorCheck:
    name: str
    ok: bool
    detail: str


@dataclass(frozen=True)
class TestConfigurationSummary:
    name: str
    caption: str
    enabled: bool
    running: bool
    verdict: int
    test_unit_count: int
    type_code: int


class CanoeComBridge:
    """Thin wrapper around CANoe COM API access patterns used by this project."""

    def __init__(self, app: Any):
        self._app = app

    @classmethod
    def connect(cls) -> "CanoeComBridge":
        platform_error = require_canoe_runtime("CANoe COM attach")
        if platform_error:
            raise CanoeComError(platform_error)
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

    def _test_configuration_collection(self) -> Any:
        try:
            return self._app.Configuration.TestConfigurations
        except Exception as ex:
            raise CanoeComError(f"TestConfigurations collection unavailable: {ex}") from ex

    def _summarize_test_configuration(self, item: Any) -> TestConfigurationSummary:
        try:
            unit_count = int(item.TestUnits.Count)
        except Exception:
            unit_count = 0
        return TestConfigurationSummary(
            name=str(item.Name),
            caption=str(getattr(item, "Caption", item.Name)),
            enabled=bool(item.Enabled),
            running=bool(item.Running),
            verdict=int(item.Verdict),
            test_unit_count=unit_count,
            type_code=int(item.Type),
        )

    def list_test_configurations(self) -> list[TestConfigurationSummary]:
        configs = self._test_configuration_collection()
        out: list[TestConfigurationSummary] = []
        for idx in range(1, int(configs.Count) + 1):
            out.append(self._summarize_test_configuration(configs.Item(idx)))
        return out

    def _resolve_test_configuration(self, config_name: str) -> Any:
        key = config_name.strip().lower()
        configs = self._test_configuration_collection()
        for idx in range(1, int(configs.Count) + 1):
            item = configs.Item(idx)
            item_name = str(item.Name).strip().lower()
            item_caption = str(getattr(item, "Caption", item.Name)).strip().lower()
            if item_name == key or item_caption == key:
                return item
        raise CanoeComError(f"Test configuration not found: {config_name}")

    def get_test_configuration_summary(self, config_name: str) -> TestConfigurationSummary:
        return self._summarize_test_configuration(self._resolve_test_configuration(config_name))

    def start_test_configuration(self, config_name: str, *, ensure_measurement: bool = True, restart_if_running: bool = False) -> TestConfigurationSummary:
        item = self._resolve_test_configuration(config_name)
        if ensure_measurement and not self.measurement_running():
            self.measurement_start()
        if bool(item.Running):
            if not restart_if_running:
                raise CanoeComError(f"Test configuration already running: {config_name}")
            item.Stop()
            time.sleep(0.5)
        item.Start()
        return self._summarize_test_configuration(item)

    def stop_test_configuration(self, config_name: str) -> TestConfigurationSummary:
        item = self._resolve_test_configuration(config_name)
        if bool(item.Running):
            item.Stop()
        return self._summarize_test_configuration(item)

    def wait_test_configuration_complete(
        self,
        config_name: str,
        *,
        timeout_seconds: int,
        poll_ms: int = 500,
        require_running_transition: bool = True,
    ) -> TestConfigurationSummary:
        item = self._resolve_test_configuration(config_name)
        initial_verdict = int(item.Verdict)
        deadline = time.monotonic() + timeout_seconds
        started = not require_running_transition
        while True:
            summary = self._summarize_test_configuration(item)
            if summary.running:
                started = True
            elif started:
                return summary
            elif not require_running_transition and not summary.running:
                return summary
            elif summary.verdict != initial_verdict:
                return summary
            if time.monotonic() >= deadline:
                raise CanoeComError(
                    f"Timed out waiting for test configuration completion: {config_name} ({timeout_seconds}s)"
                )
            time.sleep(max(poll_ms, 50) / 1000.0)

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
            if ensure_running and not running:
                self.measurement_start()
                checks.append(DoctorCheck("Measurement running", True, "stopped -> started"))
                checks.append(DoctorCheck("Measurement auto-start", True, "started"))
            else:
                checks.append(DoctorCheck("Measurement running", running, "running" if running else "stopped"))
        except Exception as ex:
            checks.append(DoctorCheck("Measurement status", False, str(ex)))

        for ns_name, var_name in required_vars:
            try:
                _ = self.get_sysvar(ns_name, var_name)
                checks.append(DoctorCheck(f"SysVar {ns_name}::{var_name}", True, "ok"))
            except Exception as ex:
                checks.append(DoctorCheck(f"SysVar {ns_name}::{var_name}", False, str(ex)))
        return checks
