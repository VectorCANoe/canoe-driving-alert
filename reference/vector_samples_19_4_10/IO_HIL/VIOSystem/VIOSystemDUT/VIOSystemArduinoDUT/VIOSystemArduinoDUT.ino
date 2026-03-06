// VIO System With DUT (Arduino board plus some LEDs and stuff)
// 2024-02-28 visdim

// Pin compatibility for 2 different displays:
// DEBO LCD 2.2 inch 240x176  | ST7789 1.3 inch 240x240 IPS
// ------------------------------------------------------------------------------------
// #01 VCC -> VCC             | ---
// #02 GND -> GND             | ---
// #03 GND -> GND         /---| ---
// #04 NC  -> nc          |   | ---
// #05 NC  -> nc          \---| #01 GND -> GND (greenwire to pin 3 of the PCB)
// #06 LED -> VCC             | #02 VCC -> VCC (3.3V only!) 
// #07 CLK -> D52/CLK         | #03 SCL -> D52/SCK
// #08 SDI -> D51/MOSI        | #04 SDA -> D51/MOSI
// #09 RS  -> D31             | #05 RES -> D31
// #10 RST -> D33             | #06 DC  -> D33
// #11 CS  -> D35 = HIGH      | #07 BLK -> D35
// ------------------------------------------------------------------------------------------
// This pin assignment allows the use of the 1.3 inch display in the 2.2 inch display layout:
// Pin 1 of the 1.3 inch display goes into Pin5 of the PCB (and so on...)
// Attention: needs one greenwire from Pin3 (GND) to Pin5 (NC) of the PCB!

// available fonts for 2.2 inch display
// Terminal6x8[];
// Terminal11x16[];
// Terminal12x16[];
// Trebuchet_MS16x21[];

#include "SPI.h"
#include "TFT_22_ILI9225.h"

// DEBO Display 2.2 inch, 220x176 pixel
#define TFT_CS  35  // CS   Pin 11 on display
#define TFT_RST 33  // RST  Pin 10 on display
#define TFT_RS  31  // RS    Pin 9 on display
#define TFT_SDI 51  // MOSI  Pin 8 on display
#define TFT_CLK 52  // SCK   Pin 7 on display
#define TFT_LED 0   // 0 if wired to +5V directly
#define TFT_BRIGHTNESS 200 // Initial brightness of TFT backlight (optional)
// cs_blk is used to make the 1.3 inch display (pin BLK) pin-compatible with the 2.2 inch disp. (pin CS)
int cs_blk = 35;

// Use hardware SPI
TFT_22_ILI9225 tft = TFT_22_ILI9225(TFT_RST, TFT_RS, TFT_CS, TFT_LED, TFT_BRIGHTNESS);

// Input signals and pins
int canoeRunningIn = 13; // input signal to show that CANoe is running (VIO4028 output [ch. 1, pin2])
int dutRunningIn = 12;   // input signal to show that the DUT is running (VIO4028 output [ch.2, pin1], after pressing button on DUT)
int counterSpeedIn = A1;   // input pin
int pwmDimmVoltageIn = A0;    // input pin
int distEchoIn = 27;  // input pin

// Output signals and pins
int counterBit0Out = 4; // Counter bits
int counterBit1Out = 5;
int counterBit2Out = 6;
int counterBit3Out = 7;
int pwmDimmDutyCycleOut = 11; // PWM signal to LED
int distTrigOut = 26;   // Duty cycle signal to VIO
int distDistanceOut = 10; // output pin

// Internal signals
int canoeRunning = 0; // internal signal
int dutRunning = 0;   // internal signal

// Flags to avoid flickering display (update display only on value change)
int canoeIdleFlag = 0;
int canoeRunningFlag = 0;
int dutRunningFlag = 0;

// 4 bit Counter
unsigned long previousCounterMillis = 0;
int counterInitialInterval = 500; // milliseconds, initial counter speed
float counterInterval = counterInitialInterval / 2; // milliseconds
float counterSpeed = 0;      // internal signal
int counterValue = 0;
bool counterBit0 = 0; // internal signal: counter bits
bool counterBit1 = 0;
bool counterBit2 = 0;
bool counterBit3 = 0;

// PWM dimmable LED
unsigned long previousPwmMillis = 0;
int pwmInterval = 200; // msec update interval for PWM dimmable LED
int pwmDimmVoltage = 0;
int pwmDimmDutyCycle = 0;

// Distance measurement
unsigned long previousDistMillis = 0;
int distInterval = 333; // msec update interval for distance measurement
unsigned long distTime = 0;
unsigned long distDistance = 0;

// Setup (runs once at startup): 
// Initialize I/Os and display, print some welcome text
void setup(void) 
{
  Serial.begin(9600);
  
  // Set input pin directions
  pinMode(canoeRunningIn, INPUT);
  pinMode(dutRunningIn, INPUT);
  pinMode(pwmDimmVoltageIn, INPUT);
  pinMode(distEchoIn, INPUT);
  pinMode(counterSpeedIn, INPUT);

  // Set output pin directions
  pinMode(counterBit0Out, OUTPUT);
  pinMode(counterBit1Out, OUTPUT);
  pinMode(counterBit2Out, OUTPUT);
  pinMode(counterBit3Out, OUTPUT);
  pinMode(pwmDimmDutyCycleOut, OUTPUT);
  pinMode(distTrigOut, OUTPUT);
  pinMode(distDistanceOut, OUTPUT);  
  // Set cs_blk signal to HIGH for both display types
  pinMode(cs_blk, OUTPUT);
  digitalWrite(cs_blk, HIGH);
 
  // Init display
  tft.begin();
  // PORTRAIT ORIENTATION:
  //tft.setOrientation(0); // text: 0=above the pins, 1=left of the pins 2=below the pins, 3=right of the pins
  // LADSCAPE ORIENTATION:
  tft.setOrientation(3); // text: 0=above the pins, 1=left of the pins 2=below the pins, 3=right of the pins
  
  // Draw big Vector arrow
  // PORTRAIT ORIENTATION:
  // tft.fillTriangle(13, 35, 163, 110, 13, 185, COLOR_RED);
  // tft.fillTriangle(13, 68, 97, 110, 13, 152, COLOR_BLACK);
  // LANDSCAPE ORIENTATION:
  tft.fillTriangle(35, 13, 185, 88, 35, 163, COLOR_RED);
  tft.fillTriangle(35, 46, 119, 88, 35, 130, COLOR_BLACK);
  delay(3000);
  
  // Write DUT info as start text
  tft.fillRectangle(0, 0, tft.maxX() - 1, tft.maxY() - 1, COLOR_RED);
  tft.fillRectangle(4, 4, tft.maxX() - 5, tft.maxY() - 5, COLOR_BLACK);
  // Draw small Vector arrow
  tft.fillTriangle (168, 15, 198, 30, 168, 45, COLOR_RED);
  tft.fillTriangle (168, 22, 184, 30, 168, 38, COLOR_BLACK);
  tft.setFont(Terminal11x16); // tft.setFont(Terminal12x16); 
  tft.drawText(15,10, "VIO System DUT");
  tft.setFont(Terminal6x8); // tft.setFont(Terminal12x16); 
  // PORTRAIT ORIENTATION
  // tft.drawText(20,30, "Tunable counter"); // 30
  // tft.drawText(20,45, "Analog-dimmable LED"); // 45
  // tft.drawText(20,60, "PWM-controlled fan"); // 60
  // tft.drawText(20,75, "PWM-dimmable LED"); // 75
  // tft.drawText(20,90, "Distance sensor"); // 90
  // tft.drawText(20,105, "Temp. sensor"); // 105, "Temp. sensor (I2C)");
  // tft.drawText(20,120, "System Clock"); // 120, "Clock module (SPI)");
  // tft.drawText(15,135, "DISPLAY:"); // 135
  // tft.drawText(20,150, "DEBO LCD 2.2"); // 150
  // tft.drawText(20,165, "220x176 Pixel"); // 165
  // tft.drawText(20,180, "INI9225 Driver"); // 180
  // tft.drawText(20,193, "SPI I/F"); // 195
  // LANDSCAPE ORIENTATION:
  tft.drawText(20,30, "Tunable counter"); // 30
  tft.drawText(20,40, "Analog-dimmable LED"); // 45
  tft.drawText(20,50, "PWM-controlled fan"); // 60
  tft.drawText(20,60, "PWM-dimmable LED"); // 75
  tft.drawText(20,70, "Distance sensor"); // 90
  tft.drawText(20,80, "Temp. sensor"); // 105, "Temp. sensor (I2C)");
  tft.drawText(20,90, "System Clock"); // 120, "Clock module (SPI)");
  tft.drawText(15,110, "DISPLAY:"); // 135
  tft.drawText(20,120, "DEBO LCD 2.2"); // 150
  tft.drawText(20,130, "220x176 Pixel"); // 165
  tft.drawText(20,140, "INI9225 Driver"); // 180
  tft.drawText(20,150, "SPI I/F"); // 195
  delay(3000);
}
  
// Main loop:
// Runs continuously, generates traffic light style indicator, runs counter etc.
void loop(void) 
{
  // Read signals for 'Traffic light style' status indicator
  canoeRunning = digitalRead(canoeRunningIn);
  dutRunning = digitalRead(dutRunningIn) & canoeRunning;

  // Generate 'Traffic light style' status indicator: CANoe halted, DUT halted
  if ((canoeRunning == 0) && (canoeIdleFlag == 0))
  {
    tft.setFont(Terminal6x8); // tft.setFont(Terminal12x16); 
    // PORTAIT ORIENTATION
    // tft.fillRectangle(10, 137, tft.maxX() - 10, tft.maxY() - 10, COLOR_BLACK);
    // tft.drawRectangle(110, 147, 162, 167, COLOR_WHITE);
    // tft.fillCircle(120, 157, 7, COLOR_RED);
    // tft.drawCircle(136, 157, 7, COLOR_YELLOW);
    // tft.drawCircle(152, 157, 7, COLOR_GREEN);
    // tft.drawText(20,145, "CANoe Halted");
    // tft.drawText(20,160, "DUT Halted");
    // tft.drawText(20,185, "Please use CANoe cfg");
    // tft.drawText(20,200, "'VIOSystemDUT.cfg'");
    // LANDSCAPE ORIENTATION
    tft.fillRectangle(10, 100, tft.maxX() - 10, tft.maxY() - 10, COLOR_BLACK);
    tft.drawRectangle(110, 108, 162, 128, COLOR_WHITE);
    tft.fillCircle(120, 118, 7, COLOR_RED);
    tft.drawCircle(136, 118, 7, COLOR_YELLOW);
    tft.drawCircle(152, 118, 7, COLOR_GREEN);
    tft.drawText(20,110, "CANoe Halted");
    tft.drawText(20,120, "DUT Halted");
    tft.drawText(20,140, "Please start CANoe cfg");
    tft.drawText(20,150, "'VIOSystemDUT.cfg'");
    canoeIdleFlag = 1;
    canoeRunningFlag = 0;
    dutRunningFlag = 0;
  }
  
  // Generate 'Traffic light style' status indicator: CANoe runs, DUT halted
  if ((canoeRunning == 1) && (dutRunning == 0) && (canoeRunningFlag == 0))
  {
    tft.setFont(Terminal6x8); // tft.setFont(Terminal12x16); 
    // PORTRAIT ORIENTATION:
    // tft.fillRectangle(10, 137, tft.maxX() - 10, tft.maxY() - 10, COLOR_BLACK);
    // tft.drawRectangle(110, 147, 162, 167, COLOR_WHITE);
    // tft.drawCircle(120, 157, 7, COLOR_RED);
    // tft.fillCircle(136, 157, 7, COLOR_YELLOW);
    // tft.drawCircle(152, 157, 7, COLOR_GREEN);
    // tft.drawText(20,145, "CANoe Running");
    // tft.drawText(20,160, "DUT Halted");
    // tft.drawText(20,185, "To start DUT, press");
    // tft.drawText(20,200, "button below display");
    // LANDSCAPE ORIENTATION:
    tft.fillRectangle(10, 100, tft.maxX() - 10, tft.maxY() - 10, COLOR_BLACK);
    tft.drawRectangle(110, 108, 162, 128, COLOR_WHITE);
    tft.drawCircle(120, 118, 7, COLOR_RED);
    tft.fillCircle(136, 118, 7, COLOR_YELLOW);
    tft.drawCircle(152, 118, 7, COLOR_GREEN);
    tft.drawText(20,110, "CANoe Running");
    tft.drawText(20,120, "DUT Halted");
    tft.drawText(20,140, "To start DUT, please press");
    tft.drawText(20,150, "button left of the display");
    canoeIdleFlag = 0;
    canoeRunningFlag = 1;
    dutRunningFlag = 0;
  }
  
  // Generate 'Traffic light style' status indicator: CANoe runs, DUT runs
  if ((canoeRunning == 1) && (dutRunning == 1) && (dutRunningFlag == 0))
  {
    tft.setFont(Terminal6x8); // tft.setFont(Terminal12x16); 
    // PORTRAIT ORIENTATION:
    // tft.fillRectangle(10, 137, tft.maxX() - 10, tft.maxY() - 10, COLOR_BLACK);
    // tft.drawRectangle(110, 147, 162, 167, COLOR_WHITE);
    // tft.drawCircle(120, 157, 7, COLOR_RED);
    // tft.drawCircle(136, 157, 7, COLOR_YELLOW);
    // tft.fillCircle(152, 157, 7, COLOR_GREEN);
    // tft.drawText(20,145, "CANoe Running");
    // tft.drawText(20,160, "DUT Running");
    // tft.drawText(20,185, "Please check CANoe");
    // tft.drawText(20,200, "for test results");
    // LANDSCAPE ORIENTATION:
    tft.fillRectangle(10, 100, tft.maxX() - 10, tft.maxY() - 10, COLOR_BLACK);
    tft.drawRectangle(110, 108, 162, 128, COLOR_WHITE);
    tft.drawCircle(120, 118, 7, COLOR_RED);
    tft.drawCircle(136, 118, 7, COLOR_YELLOW);
    tft.fillCircle(152, 118, 7, COLOR_GREEN);
    tft.drawText(20,110, "CANoe Running");
    tft.drawText(20,120, "DUT Running");
    tft.drawText(20,140, "Please check CANoe and DUT:");
    tft.drawText(20,150, "Inputs versus Outputs");
    canoeIdleFlag = 0;
    canoeRunningFlag = 0;
    dutRunningFlag = 1;
  }

  
  // 4 Bit Counter
  unsigned long currentMillis = millis();
  if (currentMillis - previousCounterMillis >= counterInterval)
  {
    previousCounterMillis = millis();
    counterBit0 = (counterValue & 1); // extract bits
    counterBit1 = ((counterValue/2) & 1);
    counterBit2 = ((counterValue/4) & 1);
    counterBit3 = ((counterValue/8) & 1);
    digitalWrite(counterBit0Out, counterBit0);
    digitalWrite(counterBit1Out, counterBit1);
    digitalWrite(counterBit2Out, counterBit2);
    digitalWrite(counterBit3Out, counterBit3);
	  if (dutRunning == 1)
    {					
      counterValue = counterValue + 1;
    }
    if (counterValue == 16)
    {
      counterValue = 0;
    }
    counterSpeed = analogRead(counterSpeedIn)/51.15; // speed 2..20, voltage 100..1023
    // avoid divide by zero at start of measurement
    if (counterSpeed < 1)
    {    
      counterSpeed = 2;
    }
    // recalc. counter interval depending on slider 
    counterInterval = counterInitialInterval / counterSpeed;
  }


 // Distance Measurement
  currentMillis = millis();
  if ((currentMillis - previousDistMillis >= distInterval))
  {
    previousDistMillis = millis();
    digitalWrite(distTrigOut, LOW);
    delay(2);
    digitalWrite(distTrigOut, HIGH);
    delay(5);
    digitalWrite(distTrigOut, LOW);
    distTime = pulseIn(distEchoIn, HIGH, 6000); // timeout needed! (6000us equals 100cm)
    distDistance = (distTime/2) * 0.03432; // Distance in cm (measured time is in us!)
    if ((distDistance > 0) && (distDistance < 100) && (dutRunning == 1))
    {
      analogWrite(distDistanceOut, distDistance*2.55); // PWM duty cycle 100% equals 255dez
    }
    else
    {
      analogWrite(distDistanceOut, 0);
    }
  }


  // PWM dimmable LED
  currentMillis = millis();
  if ((currentMillis - previousPwmMillis >= pwmInterval))
  {
    previousPwmMillis = millis();
    // read poti input & generate PWM output: voltage input 0..1023, dutyCycle output 0..255
    pwmDimmVoltage = analogRead(pwmDimmVoltageIn); 
    if (dutRunning == 1)
    {
      analogWrite(pwmDimmDutyCycleOut, pwmDimmVoltage/4);
    }
    else 
    {
      analogWrite(pwmDimmDutyCycleOut, 0);
    }
  }
}
