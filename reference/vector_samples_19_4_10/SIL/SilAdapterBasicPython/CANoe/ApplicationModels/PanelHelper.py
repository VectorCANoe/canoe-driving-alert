import vector.canoe
from application_layer import RoomTemperatureControl
from application_layer.ExploratoryTesting import Panel

@vector.canoe.measurement_script
class PanelHelper:

    def start(self):
        RoomTemperatureControl.Sensor1.Temperature.register_on_change_handler(self.set_panel_average_temperature)
        RoomTemperatureControl.Sensor2.Temperature.register_on_change_handler(self.set_panel_average_temperature)
        RoomTemperatureControl.Sensor3.Temperature.register_on_change_handler(self.set_panel_average_temperature)
        self.set_panel_average_temperature()

    def set_panel_average_temperature(self):
        Panel.AverageTemperature = (RoomTemperatureControl.Sensor1.Temperature.copy() \
                                  + RoomTemperatureControl.Sensor2.Temperature.copy() \
                                  + RoomTemperatureControl.Sensor3.Temperature.copy()) / 3

