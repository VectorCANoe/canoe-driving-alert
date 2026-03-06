#include <iostream>

#include "ftxui/screen/screen.hpp"
#include "ftxui/component/component.hpp"

#include <Windows.h>

using namespace ftxui;

class ConsoleUI
{
public:
    ConsoleUI() { 
        HideCursor();
    }

private:

    void HideCursor()
    {
        HANDLE hStdOut = NULL;
        CONSOLE_CURSOR_INFO curInfo;
        hStdOut = GetStdHandle(STD_OUTPUT_HANDLE);
        GetConsoleCursorInfo(hStdOut, &curInfo);
        curInfo.bVisible = FALSE;
        SetConsoleCursorInfo(hStdOut, &curInfo);
    }

public:

    void RenderToScreen(ftxui::Element element) const
    {
        auto screen = Screen::Create(Dimension::Full(), Dimension::Full());
        Render(screen, element);
        std::cout << screen.ResetPosition() << screen.ToString() << std::flush;
    }
};
