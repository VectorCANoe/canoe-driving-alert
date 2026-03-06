import vector.canoe
import vector.canoe.threading
import vector.canoe.tfs
import csv
from application_layer import SmartECG, SampleDataControl

from capl_exports.test_functions import TestUtils
import threading
from typing import Optional, Callable
from enum import Enum

class HeartRateObservationStatus(Enum):
  STILL_OBSERVING = 1
  MEASURED_HEART_RATE_AS_EXPECTED = 2
  MEASURED_HEART_RATE_UNEXPECTED = 3
  
ecg_sample_offset = 0
is_reset_finished_and_test_running = False
failing_heart_rate_deviation = 0
av_heart_rate_deviation = 0
sample_timer: Optional[vector.canoe.MsTimer] = None
reset_detection_algorithm_timer: Optional[vector.canoe.MsTimer] = None
ecg_recorded_samples_array: list[int] = []
reference_av_heart_rate_array: list[float] = []
av_heart_rate_offset = 0
heart_rate_observation_status = HeartRateObservationStatus.STILL_OBSERVING
test_finished_event = None

# store parameter values as constants since parameter files are not supported yet
initialization_related_number_of_heart_rates = 10
number_of_required_correct_av_heart_rates = 8
heart_rate_deviation_threshold = 10
input_frequency_ecg_without_arrhythmia = 200


def wait_for_heart_rate_observer_task(should_stop_thread: Callable[[], bool]):
  global heart_rate_observation_status
  import time
  
  while not should_stop_thread() and heart_rate_observation_status == HeartRateObservationStatus.STILL_OBSERVING:
    time.sleep(1)

  if test_finished_event is not None:
    test_finished_event.set()

@vector.canoe.tfs.export
@vector.canoe.tfs.trace_item("a31342c143aea0ddc7777")
@vector.canoe.tfs.trace_item("a31342c143aea0ddc7778")
@vector.canoe.tfs.test_case
def test_averaged_heart_rates(data_base_record_number: int):
  global heart_rate_observation_status
  global test_finished_event
  
  initialize_test_environment()
  reset_sut_beat_detection()
  start_sending_ecg_samples(data_base_record_number)
  
  # The HeartRateObserver monitors the measured heart rates derived from the sample data being transmitted.
  # By updating the heart_rate_observation_status, the HeartRateObserver indicates to the test whether the 
  # transmitted data has yielded accurately measured heart rates.
  should_stop = False
  wait_for_heart_rate_observer_thread = threading.Thread(target=wait_for_heart_rate_observer_task, args=([lambda: should_stop]))
  wait_for_heart_rate_observer_thread.start()
  
  test_finished_event = vector.canoe.threading.UserEvent()
  res = test_finished_event.wait(40000)
  should_stop = True
  
  if res != vector.canoe.threading.WaitingErrorCode.EVENT_OCCURRED:
    vector.canoe.tfs.Report.test_step_fail("", "Test timed out.")
  
  if heart_rate_observation_status == HeartRateObservationStatus.MEASURED_HEART_RATE_UNEXPECTED:
    vector.canoe.tfs.Report.test_step_fail("", "Heart rate calculated by SUT did not correspond to reference heart rate for heart rate number " + str(av_heart_rate_offset+1) + ". Deviation of average heart rate to reference was " + str(failing_heart_rate_deviation) + " .")
  
  if heart_rate_observation_status == HeartRateObservationStatus.MEASURED_HEART_RATE_AS_EXPECTED:
    vector.canoe.tfs.Report.test_step_pass("", "Test Case for averaged heart rate calculation for current data base record successfully passed!") 

@vector.canoe.measurement_script
class HeartRateObserver:
  @vector.canoe.on_update(SmartECG.SmartECG_IO.averagedHeartRate)
  def compare_average_heart_rate(self):
    global failing_heart_rate_deviation
    global av_heart_rate_deviation
    global av_heart_rate_offset
    global heart_rate_observation_status
    
    if heart_rate_observation_status != HeartRateObservationStatus.STILL_OBSERVING:
      return
    if not is_reset_finished_and_test_running:
      return
    if SmartECG.SmartECG_IO.averagedHeartRate.copy() == 0:
      return
    if av_heart_rate_offset >= len(reference_av_heart_rate_array):
      failing_heart_rate_deviation = av_heart_rate_deviation
      heart_rate_observation_status = HeartRateObservationStatus.MEASURED_HEART_RATE_UNEXPECTED
      return

    av_heart_rate_deviation = abs(SmartECG.SmartECG_IO.averagedHeartRate.copy() - reference_av_heart_rate_array[av_heart_rate_offset])
    if av_heart_rate_offset > initialization_related_number_of_heart_rates and av_heart_rate_deviation > heart_rate_deviation_threshold:
      failing_heart_rate_deviation = av_heart_rate_deviation
      if sample_timer is not None:
        sample_timer.cancel()
      heart_rate_observation_status = HeartRateObservationStatus.MEASURED_HEART_RATE_UNEXPECTED
      return
  
    if av_heart_rate_offset - initialization_related_number_of_heart_rates + 1 == number_of_required_correct_av_heart_rates:
      if sample_timer is not None:
        sample_timer.cancel()
      heart_rate_observation_status = HeartRateObservationStatus.MEASURED_HEART_RATE_AS_EXPECTED
      return
  
    av_heart_rate_offset += 1

def initialize_test_environment():
  global is_reset_finished_and_test_running
  global av_heart_rate_offset
  global heart_rate_observation_status

  stop_simulation_environment()
  av_heart_rate_offset = 0
  heart_rate_observation_status = HeartRateObservationStatus.STILL_OBSERVING
  is_reset_finished_and_test_running = False

def reset_sut_beat_detection():
  global is_reset_finished_and_test_running
  global reset_detection_algorithm_timer

  vector.canoe.tfs.Report.add_comment("Reset Beat Detection Algorithm of SUT...")
  reset_detection_algorithm_timer = vector.canoe.MsTimer(get_time_between_samples_ms(), reset_timer_handler)
  reset_detection_algorithm_timer.start()

  vector.canoe.tfs.Report.add_comment("Sending flat ECG baseline to reset algorithm ...")
  # Resetting the ECG baseline takes about 7 seconds.
  vector.canoe.threading.wait_for_timeout(7000)
  reset_detection_algorithm_timer.cancel()
  is_reset_finished_and_test_running = True

def start_sending_ecg_samples(data_base_record_number: int):
  global sample_timer

  load_data_base_records(data_base_record_number)

  vector.canoe.tfs.Report.add_comment("Starting to send ecg samples from MIT/BIH data base for data base record " + str(data_base_record_number) + " to SUT...")
  sample_timer = vector.canoe.MsTimer(get_time_between_samples_ms(), sample_timer_handler)
  sample_timer.start()

def load_data_base_records(data_base_record_number: int):
  global ecg_recorded_samples_array
  global ecg_sample_offset
  global ecg_recorded_samples_array
  global reference_av_heart_rate_array

  path_to_record = SampleDataControl.SampleDataControl.testDataDirectory.copy() + r'/Input/SampleData_200_Hz/Record' + str(data_base_record_number) +'.txt'
  path_to_reference_average_heart_rates = SampleDataControl.SampleDataControl.testDataDirectory.copy() + r'/Output_Reference/ReferenceDataAverageHeartRates_200Hz/Record' + str(data_base_record_number) +'_AverageHeartRates.txt'
  ecg_sample_offset = 0

  with open(path_to_record) as record_file:
    file_contents = next(csv.reader(record_file))
    ecg_recorded_samples_array = list(map(int, file_contents))

  with open(path_to_reference_average_heart_rates) as heart_rates_file:
    file_contents = next(csv.reader(heart_rates_file))
    reference_av_heart_rate_array = list(map(float, file_contents))

def stop_simulation_environment():
  TestUtils.initTestUnit()

  SampleDataControl.isEmergencySimulationRunning = False

def sample_timer_handler():
  global ecg_sample_offset
  global sample_timer
  if ecg_sample_offset < len(ecg_recorded_samples_array):
    SmartECG.SmartECG_IO.ecgAmplitude = ecg_recorded_samples_array[ecg_sample_offset]
    ecg_sample_offset += 1
    sample_timer = vector.canoe.MsTimer(get_time_between_samples_ms(), sample_timer_handler)
    sample_timer.start()

def reset_timer_handler():
  SmartECG.SmartECG_IO.ecgAmplitude = 0

def get_time_between_samples_ms() -> int:
  time_between_samples_in_ms = 1000 / input_frequency_ecg_without_arrhythmia
  time_between_samples_in_ms = int(time_between_samples_in_ms + 0.5)
  return time_between_samples_in_ms
