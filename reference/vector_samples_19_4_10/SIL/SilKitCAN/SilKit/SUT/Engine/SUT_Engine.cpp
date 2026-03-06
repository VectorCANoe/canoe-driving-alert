#include "silkit/SilKit.hpp"

#include "ConsoleUI.hpp"
#include "SignalHandler.hpp"

using namespace std::chrono_literals;

class Engine
{
public:
    Engine() {}

private:
    const float maxRevolutionsPerMinute = 3400.0f;
    const float accelerationUp = 50.0f;
    const float accelerationDown = -200.0f;
    const std::chrono::milliseconds updatePeriod = 100ms;

    bool _isIgnitionOn = false;
    float _revolutionsPerMinute = 0;
    float _acceleration = 0;

    ConsoleUI _consoleUI;
    std::mutex _mutex;

private:
    auto Lock() -> std::unique_lock<decltype(_mutex)> { return std::unique_lock<decltype(_mutex)>{_mutex}; }

public:
    void OnCanFrame(uint8_t canFrameData)
    {
        auto lock = Lock();
        _isIgnitionOn = (canFrameData != 0);
    }

    std::array<uint8_t, 4> ToCanFramePayload()
    {
        auto lock = Lock();
        std::array<uint8_t, 4> payload{};
        auto rpmUint = static_cast<uint32_t>(std::fmax(0.0f, _revolutionsPerMinute));
        for (unsigned byteIndex = 0; byteIndex != payload.size(); ++byteIndex)
        {
            payload[byteIndex] = static_cast<uint8_t>(rpmUint >> (byteIndex * 8u)) & UINT8_C(0xFF);
        }
        return std::move(payload);
    }

    void Update()
    {
        std::this_thread::sleep_for(updatePeriod);

        {
            auto lock = Lock();
            if (_isIgnitionOn)
            {
                if (_revolutionsPerMinute <= 0)
                {
                    _acceleration = accelerationUp;
                }
                else if (_revolutionsPerMinute >= maxRevolutionsPerMinute)
                {
                    _acceleration = accelerationDown;
                }
                _revolutionsPerMinute += _acceleration;
            }
        }
    }

    void RenderConsoleUI(bool connectedToCANoe)
    {
        auto ignitionStateText = "ON";
        auto ignitionStateColor = Color::Green1;
        if (!_isIgnitionOn)
        {
            ignitionStateText = "OFF";
            ignitionStateColor = Color::Red1;
        }

        auto rpmToGauge = _revolutionsPerMinute / maxRevolutionsPerMinute;
        auto rpmUint = static_cast<uint32_t>(std::fmax(0.0f, _revolutionsPerMinute));

        auto connectedColor = connectedToCANoe ? Color::Green1 : Color::Red1;

        auto element = vbox({
            text("SIL Kit SUT Engine") | center | color(connectedColor) | borderDouble | color(connectedColor),
            gridbox({
                {text("Ignition") | align_right | size(WIDTH, EQUAL, 16) | border,
                 text(ignitionStateText) | center | color(ignitionStateColor) | size(WIDTH, EQUAL, 6) | border},
                {text("Engine Speed") | align_right | size(WIDTH, EQUAL, 16) | border,
                 text(" " + std::to_string(rpmUint)) | size(WIDTH, EQUAL, 6) | border,
                 gauge(rpmToGauge) | color(Color::Yellow1) | border},
            }),
        });

        _consoleUI.RenderToScreen(element);
    }
};

int main(int argc, char** argv)
{
    try
    {
        Engine engine{};

        const auto registryUri = "silkit://localhost:8500";
        const auto participantName = "Engine";
        const auto participantConfigurationString = R"(
            Logging:
              Sinks:
                - Level: Warn
                  Type: Stdout
        )";
        const auto config = SilKit::Config::ParticipantConfigurationFromString(participantConfigurationString);
        auto participant = SilKit::CreateParticipant(config, participantName, registryUri);

        constexpr auto canId_ReceiveIgnitionState = 0x67;
        constexpr auto canId_SendEngineState = 0x123;

        auto* canController = participant->CreateCanController("CanControllerEngine", "easy");
        canController->AddFrameHandler(
            [&engine, canId_ReceiveIgnitionState](auto controller, SilKit::Services::Can::CanFrameEvent canFrameEvent) {
                if (canFrameEvent.frame.canId == canId_ReceiveIgnitionState)
                {
                    engine.OnCanFrame(canFrameEvent.frame.dataField[0]);
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

        auto sendThread = std::thread{[&engine, systemMonitor, lifecycleService, canController, canId_SendEngineState] {
            while (lifecycleService->State() != SilKit::Services::Orchestration::ParticipantState::Running)
            {
            };
            while (lifecycleService->State() == SilKit::Services::Orchestration::ParticipantState::Running)
            {
                engine.Update();

                SilKit::Services::Can::CanFrame frame{};
                frame.canId = canId_SendEngineState;
                frame.dlc = 4;
                frame.dataField = SilKit::Util::MakeSpan(engine.ToCanFramePayload());
                canController->SendFrame(frame);

                bool connectedToCANoe = systemMonitor->IsParticipantConnected("CANoe");
                engine.RenderConsoleUI(connectedToCANoe);
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
