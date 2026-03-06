#include "silkit/SilKit.hpp"

#include "ConsoleUI.hpp"
#include "SignalHandler.hpp"

using namespace std::chrono_literals;

class Lights
{
public:
    Lights() {}

private:
    const uint8_t flashLightBit = 1 << 0;
    const uint8_t headLightBit = 1 << 1;

    const std::chrono::milliseconds updatePeriod = 10ms;
    const std::chrono::milliseconds flashPeriod = 500ms;
    std::chrono::milliseconds _timeElapsed{0ms};

    enum class State : uint8_t
    {
        On,
        Off
    };
    State _flashLightState{State::Off};
    State _headLightState{State::Off};
    bool _isFlashLightOn{false};

    ConsoleUI _consoleUI;
    std::mutex _mutex;

private:
    auto Lock() -> std::unique_lock<decltype(_mutex)> { return std::unique_lock<decltype(_mutex)>{_mutex}; }

public:
    void OnCanFrame(uint8_t canFrameData)
    {
        auto lock = Lock();
        _flashLightState = (canFrameData & flashLightBit) ? State::On : State::Off;
        _headLightState = (canFrameData & headLightBit) ? State::On : State::Off;
    }

    std::array<uint8_t, 1> ToCanFramePayload()
    {
        auto lock = Lock();
        uint8_t canFrameData = 0x0;
        if (_headLightState == State::On)
        {
            canFrameData |= headLightBit;
        }
        if (_flashLightState == State::On && _isFlashLightOn)
        {
            canFrameData |= flashLightBit;
        }
        return {canFrameData};
    }

    void Update()
    {
        std::this_thread::sleep_for(updatePeriod);
        _timeElapsed += updatePeriod;

        if (_timeElapsed >= flashPeriod)
        {
            auto lock = Lock();
            _timeElapsed = 0ms;
            if (_flashLightState == State::On)
            {
                _isFlashLightOn = !_isFlashLightOn;
            }
        }
    }

    void RenderConsoleUI(bool connectedToCANoe)
    {
        auto headLightStateText = "ON";
        auto headLightStateColor = Color::Green1;
        if (_headLightState == State::Off)
        {
            headLightStateText = "OFF";
            headLightStateColor = Color::Red1;
        }

        auto flashLightStateText = "ON";
        auto flashLightStateColor = Color::Green1;
        if (_flashLightState == State::Off)
        {
            flashLightStateText = "OFF";
            flashLightStateColor = Color::Red1;
        }
        auto isFlashLightOnToGauge = static_cast<float>(_isFlashLightOn);

        auto connectedColor = connectedToCANoe ? Color::Green1 : Color::Red1;

        auto element = vbox({
            text("SIL Kit SUT Lights") | center | color(connectedColor) | borderDouble | color(connectedColor),
            gridbox({
                {text("Head light") | align_right | size(WIDTH, EQUAL, 16) | border,
                 text(headLightStateText) | center | color(headLightStateColor) | size(WIDTH, EQUAL, 6) | border},
                {text("Hazard Flasher") | align_right | size(WIDTH, EQUAL, 16) | border,
                 text(flashLightStateText) | center | color(flashLightStateColor) | size(WIDTH, EQUAL, 6) | border,
                 gauge(isFlashLightOnToGauge) | color(Color::Yellow1) | border},
            }),
        });

        _consoleUI.RenderToScreen(element);
    }
};

int main(int argc, char** argv)
{
    try
    {
        Lights lights{};

        const auto registryUri = "silkit://localhost:8500";
        const auto participantName = "Lights";
        const auto participantConfigurationString = R"(
            Logging:
              Sinks:
                - Level: Warn
                  Type: Stdout
        )";
        const auto config = SilKit::Config::ParticipantConfigurationFromString(participantConfigurationString);
        auto participant = SilKit::CreateParticipant(config, participantName, registryUri);

        constexpr auto canId_ReceiveLightState = 0x76;
        constexpr auto canId_SendLightState = 0x321;

        auto* canController = participant->CreateCanController("CanControllerLights", "easy");
        canController->AddFrameHandler(
            [&lights, canId_ReceiveLightState](auto controller, SilKit::Services::Can::CanFrameEvent canFrameEvent) {
                if (canFrameEvent.frame.canId == canId_ReceiveLightState)
                {
                    lights.OnCanFrame(canFrameEvent.frame.dataField[0]);
                }
            });

        auto lifecycleService =
            participant->CreateLifecycleService({SilKit::Services::Orchestration::OperationMode::Autonomous});

        auto systemMonitor = participant->CreateSystemMonitor();

        RegisterSignalHandler([lifecycleService](auto signalValue) {
            {
                auto state = lifecycleService->State();
                if (state == SilKit::Services::Orchestration::ParticipantState::Running
                    || state == SilKit::Services::Orchestration::ParticipantState::Paused)
                {
                    lifecycleService->Stop("User requested to stop");
                }
            }
        });

        lifecycleService->SetCommunicationReadyHandler([canController]() {
            canController->Start();
        });

        auto sendThread = std::thread{[&lights, systemMonitor, lifecycleService, canController, canId_SendLightState] {
            while (lifecycleService->State() != SilKit::Services::Orchestration::ParticipantState::Running)
            {
            };
            while (lifecycleService->State() == SilKit::Services::Orchestration::ParticipantState::Running)
            {
                lights.Update();

                SilKit::Services::Can::CanFrame frame{};
                frame.canId = canId_SendLightState;
                frame.dlc = 1;
                frame.dataField = SilKit::Util::MakeSpan(lights.ToCanFramePayload());
                canController->SendFrame(frame);

                bool connectedToCANoe = systemMonitor->IsParticipantConnected("CANoe");
                lights.RenderConsoleUI(connectedToCANoe);
            }
        }};

        auto participantStateFuture = lifecycleService->StartLifecycle();
        participantStateFuture.wait();
        if (sendThread.joinable())
        {
            sendThread.join();
        }
    }
    catch (const std::exception& error)
    {
        std::cerr << "Something went wrong: " << error.what() << std::endl;
        std::cout << "Press enter to stop the process..." << std::endl;
        std::cin.ignore();
        return -1;
    }
}
