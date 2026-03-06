import vector.canoe
import application_layer
import vector.canoe.threading

def updateDeserializedOuterStruct(person):
    application_layer.SerializationModel.SerializationService.Helper.DeserializedOuterStruct.origAge = person.age
    application_layer.SerializationModel.SerializationService.Helper.DeserializedOuterStruct.orig.age = person.age
    application_layer.SerializationModel.SerializationService.Helper.DeserializedOuterStruct.orig.name = person.name

def publishSerializedOuterStruct(serializedOuterStruct):
    application_layer.SerializationModel.JSONModifier.PlainPublisher = serializedOuterStruct

@vector.canoe.measurement_script
class Repeater:

    # Called before measurement start to perform necessary initializations,
    # e.g. to create objects. During measurement, few additional objects
    # should be created to prevent garbage collection runs in time-critical
    # simulations.
    def initialize(self):
        pass
    
    #Notification that the measurement starts.
    def start(self):
        pass
    
    #Notification that the measurement ends.
    def stop(self):
        pass
    
    # Cleanup after the measurement. Complement to Initialize. This is not
    # a "Dispose" method; your object should still be usable afterwards.
    def shutdown(self):
        pass

    @vector.canoe.on_update(application_layer.SerializationModel.JSONRepeatClient.PlainReceiver)
    def on_JSONClientPlainReceiver_update(self):
        receivedBytes = application_layer.SerializationModel.JSONRepeatClient.PlainReceiver.copy()
        application_layer.SerializationModel.JSONRepeatClient.PlainPublisher = receivedBytes

    @vector.canoe.on_update(application_layer.SerializationModel.GPBRepeatClient.PlainReceiver)
    def on_GPBClientPlainReceiver_update(self):
        receivedBytes = application_layer.SerializationModel.GPBRepeatClient.PlainReceiver.copy()
        application_layer.SerializationModel.GPBRepeatClient.PlainPublisher = receivedBytes

    @vector.canoe.on_update(application_layer.SerializationModel.JSONModifier.PlainReceiver)
    def on_JSONModifierPlainReceiver_update(self):
        receivedBytes = application_layer.SerializationModel.JSONModifier.PlainReceiver.copy()
        application_layer.SerializationModel.SerializationService.Serializer.Deserialize_Person.call_async(
            receivedBytes, lambda desarializedPerson: updateDeserializedOuterStruct(desarializedPerson)
        )
    
    @vector.canoe.on_update(application_layer.SerializationModel.SerializationService.Helper.DeserializedOuterStruct)
    def on_DeserializedOuterStruct_update(self):
        deserializationInput = application_layer.SerializationModel.SerializationService.Helper.DeserializedOuterStruct.copy()
        application_layer.SerializationModel.SerializationService.Serializer.Serialize_OuterStruct.call_async(
            deserializationInput, lambda serializedOuterStruct: publishSerializedOuterStruct(serializedOuterStruct)
        )
