// SPDX-FileCopyrightText: 2024 Vector Informatik GmbH
//
// SPDX-License-Identifier: MIT

#pragma once

#include <functional>
#include <thread>
#include <stdexcept>
#include <vector>

using SignalHandler = std::function<void(int)>;

//forward
namespace {
class SignalMonitor;
} // namespace

// Global signal handler
static std::unique_ptr<SignalMonitor> gSignalMonitor;

////////////////////////////////////////////
// Inline Platform Specific Implementations
////////////////////////////////////////////
#include <windows.h>

namespace {

//forward
BOOL WINAPI systemHandler(DWORD ctrlType);

class SignalMonitor
{
    static constexpr int INVALID_SIGNAL_NUMBER = -1;

public:
    SignalMonitor(SignalHandler handler)
    {
        _handler = std::move(handler);

        auto ok = CreatePipe(&_readEnd, &_writeEnd, nullptr, 0);
        if (!ok)
        {
            throw std::runtime_error("SignalMonitor: Failed to create pipe for signal handler.");
        }
        DWORD nowait = PIPE_NOWAIT;
        ok = SetNamedPipeHandleState(_writeEnd, &nowait, nullptr, nullptr);
        if (!ok)
        {
            throw std::runtime_error(
                "SignalMonitor: Failed to create signal handler, cannot set read end of pipe to non-blocking.");
        }

        SetConsoleCtrlHandler(systemHandler, true);
        _worker = std::thread{std::bind(&SignalMonitor::workerMain, this)};
    }
    ~SignalMonitor()
    {
        SetConsoleCtrlHandler(systemHandler, false);
        Notify(INVALID_SIGNAL_NUMBER);
        _worker.join();
        CloseHandle(_writeEnd);
        CloseHandle(_readEnd);
    }
    void Notify(int signalNumber)
    {
        // No allocs, no error handling
        _signalNumber = signalNumber;
        uint8_t buf{};
        auto ok = WriteFile(_writeEnd, &buf, sizeof(buf), nullptr, nullptr);
        (void)ok;
    }

private:
    void workerMain()
    {
        std::vector<uint8_t> buf(1);
        // Blocking read until Notify() was called
        auto ok = ReadFile(_readEnd, buf.data(), static_cast<DWORD>(buf.size()), nullptr, nullptr);
        if (!ok)
        {
            throw std::runtime_error("SignalMonitor::workerMain: Failed to read from pipe.");
        }

        if ((_signalNumber != INVALID_SIGNAL_NUMBER) && _handler)
        {
            _handler(_signalNumber);
        }
    }

    HANDLE _readEnd{INVALID_HANDLE_VALUE}, _writeEnd{INVALID_HANDLE_VALUE};
    SignalHandler _handler;
    std::thread _worker;
    int _signalNumber{INVALID_SIGNAL_NUMBER};
};

BOOL WINAPI systemHandler(DWORD ctrlType)
{
    if (gSignalMonitor)
    {
        gSignalMonitor->Notify(static_cast<int>(ctrlType));
        return TRUE;
    }
    return FALSE;
}

} // end anonymous namespace


//! \brief RegisterSignalHandler can be used to portably register a single signal handler.
// It only relies on async-signal-safe C functions internally, but
// it uses a dedicated thread which safely runs the user-provided handler.
void RegisterSignalHandler(SignalHandler handler)
{
    gSignalMonitor.reset(new SignalMonitor(std::move(handler)));
}
