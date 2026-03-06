// LIN.c : Example of a CANalyzer/CANoe C Library
//
// This example file demonstrates the usage of the LIN bus in a 
// CANalyzer/CANoe C Library.
//

#include "CCL/CCL.h"

/* Declare all handler functions to be registered with CANoe/CANalyzer: */
extern void OnMeasurementPreStart();
extern void OnMeasurementStart();
extern void OnTimer(int64_t time, int32_t timerID);
extern void OnLinFrame0x33(struct cclLinFrame* frame);
extern void OnLinFrame0x34(struct cclLinFrame* frame);
extern void OnLinFrame0x01(struct cclLinFrame* frame);
extern void OnSleepModeEvent(struct cclLinSleepModeEvent* event);
extern void OnWakeupFrame(struct cclLinWakeupFrame* frame);
extern void OnError(struct cclLinError* error); 
extern void OnSysVar_SchedulerStart(int64_t time, int32_t sysVarID);
extern void OnSysVar_SchedulerStop(int64_t time, int32_t sysVarID);
extern void OnSysVar_ChangeScheduleTable(int64_t time, int32_t sysVarID);
extern void OnSysVar_SendHeader(int64_t time, int32_t sysVarID);
extern void OnSysVar_UpdateResponse(int64_t time, int32_t sysVarID);
extern void OnSysVar_SendGotoSleep(int64_t time, int32_t sysVarID);
extern void OnSysVar_SendWakeup(int64_t time, int32_t sysVarID);

/* Define a global timer identifier: */
int32_t gTimerID;

/* Define global (CANoe/CANalyzer) system variable identifier: */
int32_t gSysVarID_SchedulerStart;
int32_t gSysVarID_SchedulerStop;
int32_t gSysVarID_ScheduleChange;
int32_t gSysVarID_SendHeader;
int32_t gSysVarID_UpdateResponse;
int32_t gSysVarID_SOF;
int32_t gSysVarID_SyncBreak;
int32_t gSysVarID_SyncDel;
int32_t gSysVarID_EOH;
int32_t gSysVarID_EOF;
int32_t gSysVarID_SendGotoSleep;
int32_t gSysVarID_SendWakeup;

double gTimeFactorNS = 1000000000.0;
double gTimeFactorUS = 1000000.0;

/* Define a global data array to be sent over the LIN bus: */
uint8_t gData[8] = {0, 0, 0, 0, 0, 0, 0, 0};

/* This function will be called on loading the DLL created by this project: */
void cclOnDllLoad()
{
  /* Register handler for measurement pre start and measurement start. These handlers
     are needed to register further handlers and to initialize data structures used
     by the handlers. */
  cclSetMeasurementPreStartHandler(&OnMeasurementPreStart);
  cclSetMeasurementStartHandler(&OnMeasurementStart);
}

/* Handler function called just before measurement starts. Registers further handlers
   and initializes data structures. Any handler should be registered here, because 
   otherwise they will not be called on measurement start.*/
void OnMeasurementPreStart()
{
  uint8_t data[8] = {1, 2, 3, 4, 5, 6, 7, 8};

  /* Register timer handler and save the identifier returned for further usage. */
  gTimerID = cclTimerCreate(&OnTimer);

  /* Register a handler function for LIN frame 0x33 on channel 1. The handler will be
     called by CANoe/CANalyzer whenever LIN frame 0x33 is transmitted or received on 
     channel 1: */
  if  (CCL_SUCCESS != cclLinSetFrameHandler(1, 0x33, &OnLinFrame0x33))
  {
     cclWrite("C Library Example: Could not set frame handler OnLinFrame0x33");
  }

  /* Do the same for LIN frame 0x34...: */
  if  (CCL_SUCCESS != cclLinSetFrameHandler(1, 0x34, &OnLinFrame0x34))
  {
    cclWrite("C Library Example: Could not set frame handler OnLinFrame0x34");
  }

  /* ... and for LIN frame 0x01: */
  if  (CCL_SUCCESS != cclLinSetFrameHandler(1, 0x01, &OnLinFrame0x01))
  {
    cclWrite("C Library Example: Could not set frame handler OnLinFrame0x01");
  }

  /* Configure LIN responses for simulation with the data array defined above. 
     First for LIN frame 0x33. The response of the frame will be sent with the data...:*/
  if (CCL_SUCCESS != cclLinUpdateResponseData(1, 0x33, 6, data))
  {
    cclWrite("C Library Example: Could not update response data of ID 0x33");
  }

  /* ... then for LIN frame 0x34...: */
  if (CCL_SUCCESS != cclLinUpdateResponseData(1, 0x34, 6, data))
  {
    cclWrite("C Library Example: Could not update response data of ID 0x34");
  }

  /* ... and for LIN frame 0x36: */
  if (CCL_SUCCESS != cclLinUpdateResponseData(1, 0x36, 3, data))
  {
      cclWrite("C Library Example: Could not update response data of ID 0x36");
  }

  /* Configure identifier not defined in the LDF. Here we use the global data array: */
  if (CCL_SUCCESS != cclLinUpdateResponseData(1, 0x01, 2, gData))
  {
    cclWrite("C Library Example: Could not update response data if ID 0x01");
  }

  /* Register a handler function for LIN frame 0x33 on channel 2. Note that this only 
     works if the LIN channels 1 and 2 are connected to each other (looped): */
  if  (CCL_SUCCESS != cclLinSetFrameHandler(2, 0x33, &OnLinFrame0x33))
  {
    cclWrite("C Library Example: Could not set message handler OnLinFrame0x33");
  }

  /* Do the same for LIN frame 0x34: */
  if  (CCL_SUCCESS != cclLinSetFrameHandler(2, 0x34, &OnLinFrame0x34))
  {
    cclWrite("C Library Example: Could not set message handler OnLinFrame0x34");
  }
  
  /* Register a sleep mode event handler on channel 1. This handler is called whenever 
     a sleep mode event appears on the LIN bus: */
  if (CCL_SUCCESS != cclLinSetSleepModeEventHandler(1, &OnSleepModeEvent))
  {
    cclWrite("C Library Example: Could not set event handler OnSleepModeEvent");
  }

  /* Register a wakeup frame handler on channel 1. This handler is called whenever a 
     wakeup frame appears on the LIN bus: */
  if (CCL_SUCCESS != cclLinSetWakeupFrameHandler(1, &OnWakeupFrame))
  {
    cclWrite("C Library Example: Could not set message handler OnWakeupFrame");
  }

  /* Register an error handler for all LIN frames on channel 1. You may also register
     the handler only for a specific LIN frame by passing the frame identifier instead
     of CCL_LIN_ALLMESSAGES to the function: */
  if (CCL_SUCCESS != cclLinSetErrorHandler(1, CCL_LIN_ALLMESSAGES, &OnError))
  {
    cclWrite("C Library Example: Could not set error handler OnError");
  }

  /* Obtain system variable identifier from CANoe/CANalyzer. These are needed to access
     the system variables for modification: */
  gSysVarID_SchedulerStart = cclSysVarGetID("LIN::SchedulerStart");
  gSysVarID_SchedulerStop = cclSysVarGetID("LIN::SchedulerStop");
  gSysVarID_ScheduleChange = cclSysVarGetID("LIN::ChangeScheduleTable");
  gSysVarID_SendHeader = cclSysVarGetID("LIN::SendHeader");
  gSysVarID_UpdateResponse = cclSysVarGetID("LIN::UpdateResponse");
  gSysVarID_SOF = cclSysVarGetID("LIN::SOF");
  gSysVarID_SyncBreak = cclSysVarGetID("LIN::SyncBreak");
  gSysVarID_SyncDel = cclSysVarGetID("LIN::SyncDel");
  gSysVarID_EOH = cclSysVarGetID("LIN::EOH");
  gSysVarID_EOF = cclSysVarGetID("LIN::EOF");
  gSysVarID_SendGotoSleep = cclSysVarGetID("LIN::SendGotoSleep");
  gSysVarID_SendWakeup = cclSysVarGetID("LIN::SendWakeup");

  /* Register some system variable handler functions using the identifiers. The functions 
     will be called by CANoe/CANalyzer whenever the value of the system variable to which
     the function is registered gets an update: */
  cclSysVarSetHandler(gSysVarID_SchedulerStart, &OnSysVar_SchedulerStart);
  cclSysVarSetHandler(gSysVarID_SchedulerStop, &OnSysVar_SchedulerStop);
  cclSysVarSetHandler(gSysVarID_ScheduleChange, &OnSysVar_ChangeScheduleTable);
  cclSysVarSetHandler(gSysVarID_SendHeader, &OnSysVar_SendHeader);
  cclSysVarSetHandler(gSysVarID_UpdateResponse, &OnSysVar_UpdateResponse);
  cclSysVarSetHandler(gSysVarID_SendGotoSleep, &OnSysVar_SendGotoSleep);
  cclSysVarSetHandler(gSysVarID_SendWakeup, &OnSysVar_SendWakeup);
}

/* Called on measurement start. Can be used e.g. to initialize internal variables with
   default values and to start the simulation. 
   In this example it just issues a message to the Write window of CANoe/CANalyzer. */
void OnMeasurementStart()
{
  cclWrite("C Library Example: OnMeasurementStart");
}

/* Called if the timer expires. Can be used to react on timing events. 
   In this example it changes the currently set schedule table back to the first
   schedule table. */
void OnTimer(int64_t time, int32_t timerID)
{
  /* Change schedule table back to the first schedule table. */
  cclLinChangeSchedtable(1, 0);
}

/* Handler function for LIN frame 0x33. */
void OnLinFrame0x33(struct cclLinFrame* frame)
{
  /* Do something (hopefully useful) with the frame, e.g. modify its data. Here we
     check only the channel on which the frame came in and issue a message to the
     Write window of CANoe/CANalyzer: */
  if (frame->channel == 2)
  {
    cclWrite("C Library Example: OnLinFrame0x33 on channel 2");
  }
}

/* Handler function for LIN frame 0x34. */
void OnLinFrame0x34(struct cclLinFrame* frame)
{
  /* Same as for LIN frame 0x33: */
  if (frame->channel == 2)
  {
    cclWrite("C Library Example: OnLinFrame0x34 on channel 2");
  }
}

/* Handler function for LIN frame 0x01. */
void OnLinFrame0x01(struct cclLinFrame* frame)
{ 
  /* Set some system variables with values computed from the time values of
     the frame. To do so, we need the identifier of the system variables 
     obtained in OnMeasurementPreStart(): */
  double sof         = frame->timestampSOF/gTimeFactorNS;
  double syncBreak   = frame->timeSyncBreak/gTimeFactorUS;
  double syncDel     = frame->timeSyncDel/gTimeFactorUS;
  double eoh         = frame->timestampEOH/gTimeFactorNS;
  double eof         = frame->timestampEOF/gTimeFactorNS;

  cclSysVarSetFloat(gSysVarID_SOF       , sof); 
  cclSysVarSetFloat(gSysVarID_SyncBreak , syncBreak); 
  cclSysVarSetFloat(gSysVarID_SyncDel   , syncDel); 
  cclSysVarSetFloat(gSysVarID_EOH       , eoh); 
  cclSysVarSetFloat(gSysVarID_EOF       , eof); 
  /* While measurement is running, you should see the system variable values 
     changing in the "Frame Timings" window of the configuration in CANoe/CANalyzer. */
}

/* Handler function for system variable "SchedulerStart". This handler is called when
   you click on the "Start Scheduler" button in the "Control of LIN Transmission" window
   of the CANoe/CANalyzer configuration. */
void OnSysVar_SchedulerStart(int64_t time, int32_t sysVarID)
{
  /* Get current value of the system variable: */
  int32_t startScheduler;
  cclSysVarGetInteger(gSysVarID_SchedulerStart, &startScheduler);

  if (startScheduler == 1)
  {
    /* Start scheduler on channel 1: */
    cclLinStartScheduler(1);
    cclWrite("C Library Example: OnSysVar_SchedulerStart");
    /* You should see frames getting periodically updated in the Trace window. */
  }
}

/* Handler function for system variable "SchedulerStop". This handler is called when
   you click on the "Stop Scheduler" button in the "Control of LIN Transmission" window
   of the CANoe/CANalyzer configuration. */
void OnSysVar_SchedulerStop(int64_t time, int32_t sysVarID)
{
  /* Get current value of the system variable: */
  int32_t stopScheduler;
  cclSysVarGetInteger(gSysVarID_SchedulerStop, &stopScheduler);

  if (stopScheduler == 1)
  {
    /* Stop scheduler on channel 1: */
    cclLinStopScheduler(1);
    cclWrite("C Library Example: OnSysVar_SchedulerStop");
    /* You should see either no frame at all or frames not getting updated in the Trace window. */
  }
}

/* Handler function for system variable "ChangeScheduleTable". This handler is called when
   you click on the "Change Table" button in the "Control of LIN Transmission" window
   of the CANoe/CANalyzer configuration. */
void OnSysVar_ChangeScheduleTable(int64_t time, int32_t sysVarID)
{
  /* Get current value of the system variable: */
  int32_t tableIndex;
  cclSysVarGetInteger(gSysVarID_ScheduleChange, &tableIndex);

  if (tableIndex == 1)
  {
    /* Change table to index 1 and set timer to 5 seconds. Note that the table indexes are null based,
       that is: tableIndex 0 is the first, tableIndex 1 the second schedule table (etc.).*/
    cclLinChangeSchedtable(1, tableIndex); 
    cclTimerSet(gTimerID, cclTimeMilliseconds(5000));
    cclWrite("C Library Example: OnSysVar_ChangeScheduleTable");
    /* You should see frames sent by the second schedule table until the timer expires (about 5 seconds). 
       After the timer has expired, handler function OnTimer() will be called and sets the schedule table
       back to the first table. */
  }
}

/* Handler function for system variable "SendHeader". This handler is called when you click
   on the "Send Header ID = 0x01" button in the "Control of LIN Transmission" window of the
   CANoe/CANalyzer configuration. */
void OnSysVar_SendHeader(int64_t time, int32_t sysVarID)
{
  /* Get current value of the system variable: */
  int32_t sendHeader;
  cclSysVarGetInteger(gSysVarID_SendHeader, &sendHeader);

  if (sendHeader == 1)
  {
    /* Send header of frame identifier 0x01 on channel 1: */
    cclLinSendHeader(1, 0x01);
    cclWrite("C Library Example: OnSysVar_SendHeader");
  }
}

/* Handler function for system variable "UpdateResponse". This handler is called when you click
   on the "Update Response ID = 0x01" button in the "Control of LIN Transmission" window of the
   CANoe/CANalyzer configuration. */
void OnSysVar_UpdateResponse(int64_t time, int32_t sysVarID)
{
  /* Get current value of the system variable: */
  int32_t updateResponse;
  cclSysVarGetInteger(gSysVarID_UpdateResponse, &updateResponse);

  if (updateResponse == 1)
  {
    /* Modify global data array in some way...: */
    gData[0] += 1;
    gData[1] += 1;
    /* ... and update the response of the frame with the modified data: */
    cclLinUpdateResponseData(1, 0x01, 2, gData); 
    cclWrite("C Library Example: OnSysVar_UpdateResponse");
  }
}

/* Handler function for system variable "SendGotoSleep". This handler is called when you click
   on the "Goto Sleep" button in the "Control of LIN Transmission" window of the CANoe/CANalyzer 
   configuration. */
void OnSysVar_SendGotoSleep(int64_t time, int32_t sysVarID)
{
  /* Get current value of the system variable: */
  int32_t gotoSleep;
  cclSysVarGetInteger(gSysVarID_SendGotoSleep, &gotoSleep);

  if (gotoSleep == 1)
  {
    /* Send goto sleep event to the LIN network on channel 1:*/
    cclLinGotoSleep(1);
    cclWrite("C Library Example: OnSysVar_SendGotoSleep");
    /* Two green MasterReq ("Go-to-Sleep") events, one for each channel, should appear in
       the Trace window. Update of LIN frames should be halted.*/
  }
}

/* Handler function for system variable "SendWakeup". This handler is called when you click
   on the "Wakeup" button in the "Control of LIN Transmission" window of the CANoe/CANalyzer
   configuration. */
void OnSysVar_SendWakeup(int64_t time, int32_t sysVarID)
{
  /* Get current value of the system variable: */
  int32_t wakeup;
  cclSysVarGetInteger(gSysVarID_SendWakeup, &wakeup);

  if (wakeup == 1)
  {
    /* Send wakeup request to the LIN network on channel 1:*/
    cclLinWakeup(1);
    cclWrite("C Library Example: OnSysVar_SendWakeup");
    /* Two green WakeupRequest events, one for each channel, should appear in the Trace window. 
       All LIN frames should be updated again.*/
  }
}

/* Handler function for sleep mode events. Can be used to pause the simulation. */
void OnSleepModeEvent(struct cclLinSleepModeEvent* event)
{
  /* Here we just issue messages to the Write window of CANoe/CANalyzer: */
  if (event->channel == 1)
  {
    cclWrite("C Library Example: OnSleepModeEvent on channel 1");
  }
  else
  {
    cclWrite("C Library Example: OnSleepModeEvent on channel 2");
  }
}

/* Handler function for wakeup frames. Can be used to restart the simulation. */
void OnWakeupFrame(struct cclLinWakeupFrame* frame)
{
  /* Here we just issue messages to the Write window of CANoe/CANalyzer: */
  if (frame->channel == 1)
  {
    cclWrite("C Library Example: OnWakeupFrame on channel 1");
  }
  else
  {
    cclWrite("C Library Example: OnWakeupFrame on channel 2");
  }
}

/* Error handler function. Should be implemented to allow the simulation to react on errors. */
void OnError(struct cclLinError* error)
{
  /* Use this handler function to implement a proper error handling in the simulation. In this
     example, we just issue a message for each of the error types known by CANoe/CANalyzer to 
     the Write window: */
  switch (error->type)
  {
  case CCL_LIN_ERROR_CHECKSUM:
    cclPrintf("C Library Example: Checksum error (Frame Id: 0x%x, CRC=%i)", 
      error->id, error->crc);
    break;
  case CCL_LIN_ERROR_TRANSMISSION:
    cclPrintf("C Library Example: Transmission error (Full time: %i, Header time: %i)", 
      error->fullTime, error->headerTime);
    break;
  case CCL_LIN_ERROR_RECEIVE:
    cclPrintf("C Library Example: Receive error (Frame Id: 0x%x, Expected DLC: %i, Offending byte: %i, Short error: %i)", 
      error->id, error->dlc, error->offendingByte, error->shortError);
    break;
  case CCL_LIN_ERROR_SYNC:
    cclWrite("C Library Example: Sync error");
    break;
  case CCL_LIN_ERROR_SLAVETIMEOUT:
    cclPrintf("C Library Example: Slave Timeout error (Slave Id: 0x%x)", 
      error->slaveId);
    break;
  default:
    break;
  }
}