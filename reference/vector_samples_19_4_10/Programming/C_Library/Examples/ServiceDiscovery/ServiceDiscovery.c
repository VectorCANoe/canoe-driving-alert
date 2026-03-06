// ServiceDiscovery.c : Example of a CANalyzer/CANoe C Library
//
// This sample file demonstrates the usage of Service Discovery in a 
// CANalyzer/CANoe C Library.
//

#include "CCL/CCL.h"

int32_t gCreateConsumerTimer;
int32_t gDestroyConsumerTimer;
int32_t gProvideServiceTimer;
int32_t gSubscribeEventsTimer;

cclServiceID gTheService;
cclProviderID gStaticProvider;
cclConsumerID gDynamicConsumer;
cclAddressID gConsumerAddress;
int32_t gSysVarConsumer;
int32_t gSysVarProvider;
int32_t gSysVarEvent1;
int32_t gSysVarEvent2;
int32_t gSysVarEvent3;

void OnMeasurementPreStart();
void OnMeasurementStart();
void OnCreateConsumer(int64_t time, int32_t timerID);
void OnDestroyConsumer(int64_t time, int32_t timerID);
void OnProvideService(int64_t time, int32_t timerID);
void OnSubscribeEvents(int64_t time, int32_t timerID);
void OnConnectionStateConsumer(cclTime time, cclValueID valueID);
void OnConnectionStateProvider(cclTime time, cclValueID valueID);

#define SERVICE_PATH          "ValueEntities::TheService"
#define DYNAMIC_CONSUMER_NAME "DynamicConsumer"
#define STATIC_CONSUMER_NAME  "Client1"
#define STATIC_PROVIDER_NAME  "Server1"
#define STATIC_PROVIDER_PATH  SERVICE_PATH "[" STATIC_PROVIDER_NAME "]"
#define DYNAMIC_CONSUMER_PORT SERVICE_PATH ".consumerSide[" DYNAMIC_CONSUMER_NAME "," STATIC_PROVIDER_NAME "]"
#define DYNAMIC_PROVIDER_PORT SERVICE_PATH ".providerSide[" DYNAMIC_CONSUMER_NAME "," STATIC_PROVIDER_NAME "]"


void cclOnDllLoad()
{
  cclSetMeasurementPreStartHandler(&OnMeasurementPreStart);
  cclSetMeasurementStartHandler(&OnMeasurementStart);
}

void OnMeasurementPreStart()
{
  gCreateConsumerTimer = cclTimerCreate(&OnCreateConsumer);
  gDestroyConsumerTimer = cclTimerCreate(&OnDestroyConsumer);
  gProvideServiceTimer = cclTimerCreate(&OnProvideService);
  gSubscribeEventsTimer = cclTimerCreate(&OnSubscribeEvents);
}

void OnMeasurementStart()
{
  gTheService = cclServiceGetID(SERVICE_PATH);
  gConsumerAddress = cclAbstractCreateAddress(gTheService, DYNAMIC_CONSUMER_NAME);
  gStaticProvider = cclProviderGetID(STATIC_PROVIDER_PATH);

  gSysVarConsumer = cclSysVarGetID("TheService_consumerSide_DynamicConsumer_Server1");
  gSysVarProvider = cclSysVarGetID("TheService_providerSide_DynamicConsumer_Server1");
  gSysVarEvent1 = cclSysVarGetID("Event1_SubscriptionState");
  gSysVarEvent2 = cclSysVarGetID("Event2_SubscriptionState");
  gSysVarEvent3 = cclSysVarGetID("Event3_SubscriptionState");

  cclTimerSet(gCreateConsumerTimer, cclTimeMilliseconds(2000));
  cclTimerSet(gProvideServiceTimer, cclTimeMilliseconds(3000));
}

void UpdateConnectionState(const char* port, int32_t sysVarID, cclValueHandler handler)
{
  int64_t connectionState;
  cclValueID valueID = cclValueGetID(CCL_COMMUNICATION_OBJECTS, port, CCL_MEMBER_CONNECTION_STATE, CCL_IMPL);
  cclValueGetInteger(valueID, &connectionState);
  cclSysVarSetInteger(sysVarID, (int32_t)(connectionState + 1));
  cclValueSetHandler(valueID, false, handler);
}

void OnConnectionStateConsumer(cclTime time, cclValueID valueID)
{
  int64_t connectionState;
  cclValueGetInteger(valueID, &connectionState);
  cclSysVarSetInteger(gSysVarConsumer, (int32_t)(connectionState + 1));
}

void OnConnectionStateProvider(cclTime time, cclValueID valueID)
{
  int64_t connectionState;
  cclValueGetInteger(valueID, &connectionState);
  cclSysVarSetInteger(gSysVarProvider, (int32_t)(connectionState + 1));
}

void UpdateSubscriptionState(cclTime time, cclValueID valueID)
{
  int64_t subscriptionState;
  cclValueID event1ID = cclValueGetID(CCL_COMMUNICATION_OBJECTS, DYNAMIC_CONSUMER_PORT ".Event1", CCL_MEMBER_SUBSCRIPTION_STATE, CCL_IMPL);
  cclValueGetInteger(event1ID, &subscriptionState);
  cclSysVarSetInteger(gSysVarEvent1, (int32_t)(subscriptionState + 1));
  cclValueSetHandler(event1ID, false, &UpdateSubscriptionState);

  cclValueID event2ID = cclValueGetID(CCL_COMMUNICATION_OBJECTS, DYNAMIC_CONSUMER_PORT ".Event2", CCL_MEMBER_SUBSCRIPTION_STATE, CCL_IMPL);
  cclValueGetInteger(event2ID, &subscriptionState);
  cclSysVarSetInteger(gSysVarEvent2, (int32_t)(subscriptionState + 1));
  cclValueSetHandler(event2ID, false, &UpdateSubscriptionState);

  cclValueID event3ID = cclValueGetID(CCL_COMMUNICATION_OBJECTS, DYNAMIC_CONSUMER_PORT ".Event3", CCL_MEMBER_SUBSCRIPTION_STATE, CCL_IMPL);
  cclValueGetInteger(event3ID, &subscriptionState);
  cclSysVarSetInteger(gSysVarEvent3, (int32_t)(subscriptionState + 1));
  cclValueSetHandler(event3ID, false, &UpdateSubscriptionState);
}

void OnCreateConsumer(int64_t time, int32_t timerID)
{
  // add a dynamic consumer
  gDynamicConsumer = cclAddConsumerByName(gTheService, DYNAMIC_CONSUMER_NAME, true);
  cclSetConsumerAddress(gDynamicConsumer, gConsumerAddress, CCL_PROVIDER_NONE);

  UpdateConnectionState(DYNAMIC_CONSUMER_PORT, gSysVarConsumer, &OnConnectionStateConsumer);
  UpdateConnectionState(DYNAMIC_PROVIDER_PORT, gSysVarProvider, &OnConnectionStateProvider);

  UpdateSubscriptionState(0, -1);

  // subscribe events for dynamic consumer in 2 seconds
  cclTimerSet(gSubscribeEventsTimer, cclTimeMilliseconds(2000));

  // destroy the consumer in 10 seconds
  cclTimerSet(gDestroyConsumerTimer, cclTimeMilliseconds(10000));
}

void OnDestroyConsumer(int64_t time, int32_t timerID)
{
  cclRemoveConsumer(gTheService, gDynamicConsumer);

  cclSysVarSetInteger(gSysVarConsumer, 0);
  cclSysVarSetInteger(gSysVarProvider, 0);
  cclSysVarSetInteger(gSysVarEvent1, 0);
  cclSysVarSetInteger(gSysVarEvent2, 0);
  cclSysVarSetInteger(gSysVarEvent3, 0);

  cclTimerSet(gCreateConsumerTimer, cclTimeMilliseconds(2000));
}

void OnProvideService(int64_t time, int32_t timerID)
{
  bool isServiceProvided;
  cclIsServiceProvided(gStaticProvider, &isServiceProvided);
  if (isServiceProvided)
    cclReleaseService(gStaticProvider);
  else
    cclProvideService(gStaticProvider);

  cclTimerSet(gProvideServiceTimer, cclTimeMilliseconds(3000));
}

void OnSubscribeEvents(int64_t time, int32_t timerID)
{
  cclConsumedEventID consumedEvent1 = cclAbstractConsumedEventGetID(DYNAMIC_CONSUMER_PORT ".Event1");
  cclAbstractSubscribeEvent(consumedEvent1);
  cclConsumedEventID consumedEvent2 = cclAbstractConsumedEventGetID(DYNAMIC_CONSUMER_PORT ".Event2");
  cclAbstractSubscribeEvent(consumedEvent2);
  cclConsumedEventID consumedEvent3 = cclAbstractConsumedEventGetID(DYNAMIC_CONSUMER_PORT ".Event3");
  cclAbstractSubscribeEvent(consumedEvent3);
}
