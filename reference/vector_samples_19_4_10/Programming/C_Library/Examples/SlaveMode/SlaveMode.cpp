// CANoeSlave.cpp : Example of a CANoe C Library
//
// This sample file demonstrates the usage of the Slave Mode of 
// CANoe in a C Library.
//

#include "CCL/CCL.h"

#include <thread>
#include <mutex>
#include <deque>

#if defined(_WIN32)
#  include <windows.h>
#elif defined(__linux__)
#  include <string.h>
#endif


extern void OnMeasurementPreStart();
extern void OnMeasurementStart();
extern void OnMeasurementStop();
extern void OnDllUnload();
extern void OnCanMessageReceived(struct cclCanMessage* message);
extern void StartEventThread();
extern void StopEventThread();
extern void OnMessageQueueTimer(int64_t time, int32_t timerID);
extern void OnTimerIncrementTimer(int64_t time, int32_t timerID);

/*
 * Different implementations for Windows and Linux
 * Windows uses Events and Linux uses the named fifo /tmp/CANoeSlave
 */
void WaitForEvent();
void ShutdownEventThread();

// global listener thread
std::thread gListenerThread;

// thread control
bool gThreadRunning;

// protect message queue
std::mutex gMutex;

// message queue to transfer messages from the input queue into CANoe's processing.
// sending messages to CANoe (cclCanOutputMessage) must happen on CANoe's main thread, i.e. sent in a timer event callback (OnTimer)
std::deque<uint32_t> gMessageQueue;

int32_t gQueueTimerID;
int32_t gIncrementTimerID;

int64_t gDeltaIncrementTime;

void cclOnDllLoad()
{
  cclSetMeasurementPreStartHandler(&OnMeasurementPreStart);
  cclSetMeasurementStartHandler(&OnMeasurementStart);
  cclSetMeasurementStopHandler(&OnMeasurementStop);
  cclSetDllUnloadHandler(&OnDllUnload);
}


void OnMeasurementPreStart()
{
  // 100 milliseconds are just used to demonstrate the interactive generator in CANoe
  gDeltaIncrementTime = cclTimeMilliseconds(100);
  // For real world usage we suggest to use 100 microseconds.
  // gDeltaIncrementTime = cclTimeMicroseconds(100);

  int32_t rc;
  gQueueTimerID = cclTimerCreate(&OnMessageQueueTimer);
  gIncrementTimerID = cclTimerCreate(&OnTimerIncrementTimer);

  bool isSlaveMode = false;
  rc = cclIsRunningInSlaveMode(&isSlaveMode);

  rc = cclCanSetMessageHandler(1, CCL_CAN_ALLMESSAGES, &OnCanMessageReceived);
  StartEventThread();
}


void OnMeasurementStart()
{
  int32_t rc;
  rc = cclTimerSet(gQueueTimerID, 1); // one nanosecond
  rc = cclTimerSet(gIncrementTimerID, gDeltaIncrementTime);
}

void OnMeasurementStop()
{
  StopEventThread();
}

void OnDllUnload()
{
}

void OnCanMessageReceived(struct cclCanMessage *message)
{
  uint32_t messageId = cclCanValueOfIdentifier(message->id);
  cclPrintf("C Library Example: OnCanMessageReceived with ID: 0x%X", messageId);
}


void OnMessageQueueTimer(int64_t time, int32_t timerID)
{
  int32_t channel = 1;
  uint32_t id = cclCanMakeStandardIdentifier(0x234);
  uint32_t flags = 0;
  uint8_t dataLength = 8;
  uint8_t data[8] = { 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08 };
  int32_t rc;

  gMutex.lock();
  // flush queue and put messages on internal CAN bus
  while (!gMessageQueue.empty())
  {
    uint32_t msg = gMessageQueue.front();
    gMessageQueue.pop_front();
    memcpy(&data[0], &msg, sizeof(msg));
    rc = cclCanOutputMessage(channel, id, flags, dataLength, data);
  }
  gMutex.unlock();
  rc = cclTimerSet(gQueueTimerID, gDeltaIncrementTime);
}

void OnTimerIncrementTimer(int64_t time, int32_t timerID)
{
  // called when simulation step (increment time) is finished.
  // can be used to transfer all output data to the external tool
  // 
  int32_t rc = cclTimerSet(gIncrementTimerID, gDeltaIncrementTime);
}

void StartEventThread()
{
  gListenerThread = std::thread(WaitForEvent);
}

void StopEventThread()
{
  // signal thread to finish
  gThreadRunning = false;
  ShutdownEventThread();
  gListenerThread.join();
  gListenerThread = std::thread();
}

#if defined(_WIN32)
void ShutdownEventThread()
{
  HANDLE hEvent = OpenEventA(EVENT_MODIFY_STATE, false, "Global\\CANoeSignalTriggerTimeDemo");
  SetEvent(hEvent);
  CloseHandle(hEvent);
}

void WaitForEvent()
{
  HANDLE hEvent[2];
  hEvent[0] = CreateEventA(NULL, true, false, "Global\\CANoeSignalTriggerTimeDemo");
  hEvent[1] = CreateEventA(NULL, true, false, "Global\\CANoeSignalTriggerMessageDemo");
  gThreadRunning = true;
  uint32_t msg = 0; // used in this example to simulate a received message that is put into the queue
  while (gThreadRunning)
  {
    cclWrite("Wait for Signal");
    DWORD h = WaitForMultipleObjects(2, hEvent, false, INFINITE); // or wait an amount of time
    size_t arrayIndex = h - WAIT_OBJECT_0;
    ResetEvent(hEvent[arrayIndex]);
    if (gThreadRunning)
    {
      if (arrayIndex == 0)
      {
        // trigger time
        cclWrite("Receive time trigger");
        auto rc = cclIncrementTimerBase(gDeltaIncrementTime, 1); // returns immediately, avoid additional calls until OnTimerIncrementTimer was called
      }
      else if (arrayIndex == 1)
      {
        cclPrintf("Received Message: %i", msg);
        // received message, put into queue
        gMutex.lock();
        msg++;
        gMessageQueue.push_back(msg);
        gMutex.unlock();
      }
    }
    else
    {
      cclWrite("Received shutdown");
    }
  }
  cclWrite("Exiting loop\n");
  CloseHandle(hEvent[1]);
  CloseHandle(hEvent[0]);
}
#elif defined(__linux__)

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>

const char fifoName[] = "/tmp/CANoeSlave";

void ShutdownEventThread()
{
  int fd = open(fifoName, O_WRONLY);
  close(fd);
}

void WaitForEvent()
{
  int res = 0;
  res = mkfifo(fifoName, 0666);
  if (res == -1)
  {
    if (errno != 17) // file exists, assume it's our fifo from a previous run
    {
      perror("mkfifo");
      // cclWrite and cclIncrementTime to tell the user?
      return;
    }
  }

  int fd = open(fifoName, O_RDONLY);
  if (fd < 0)
  {
    perror("open");
    // cclWrite and cclIncrementTime to tell the user?
    return;
  }

  gThreadRunning = true;
  uint32_t msg = 0; // used in this example to simulate a received message that is put into the queue

  char buf[256];
  while (gThreadRunning)
  {
    cclWrite("Wait for Signal");
    memset(buf, 0, sizeof(buf));
    res = read(fd, buf, sizeof(buf));

    if (gThreadRunning)
    {
      if (buf[0] == 't')
      {
        // trigger time
        cclWrite("Receive time trigger");
        auto rc = cclIncrementTimerBase(gDeltaIncrementTime, 1); // returns immediately, avoid additional calls until OnTimerIncrementTimer was called
      }
      else if (buf[0] == 'm')
      {
        cclPrintf("Received Message: %i", msg);
        // received message, put into queue
        gMutex.lock();
        msg++;
        gMessageQueue.push_back(msg);
        gMutex.unlock();
      }
    }
    else
    {
      cclWrite("Received shutdown");
    }

    // in case the fifo was closed at the other end, reopen it.
    if (res == 0)
    {
      close(fd);
      fd = open(fifoName, O_RDONLY);
      if (fd < 0)
      {
        perror("open");
        return;
      }
    }
  }
  close(fd);
  unlink(fifoName);
  cclWrite("Exiting loop\n");
}
#endif

