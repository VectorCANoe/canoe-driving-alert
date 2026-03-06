#include <functional>
#include <memory>
#include <cmath>

#include "rclcpp/rclcpp.hpp"
#include "adas_msgs/msg/input_ros.hpp"
#include "adas_msgs/msg/output_ros.hpp"

using std::placeholders::_1;

class ADASNode : public rclcpp::Node
{
public:
  ADASNode() : Node("adas_node")
  {
    subscription = this->create_subscription<adas_msgs::msg::InputRos>("adas_ros_input", 10, std::bind(&ADASNode::onRadarObject, this, _1));
    publisher = this->create_publisher<adas_msgs::msg::OutputRos>("adas_ros_output", 10);
  }

private:
  void onRadarObject(const adas_msgs::msg::InputRos& input)
  {
    // Receive inputs
    radarObjectTrackingId = input.radar_object.tracking_id;
    radarObjectMeasurementStatus = input.radar_object.measurement_status;
    radarObjectPosX = input.radar_object.pos_x;
    radarObjectPosY = input.radar_object.pos_y;
    radarObjectPosZ = input.radar_object.pos_z;
    radarObjectSpeed = input.radar_object.speed;
    
    RCLCPP_INFO(this->get_logger(), "Input ROS: '%d' '%d' '%f' '%f' '%f' '%f' '%f'", radarObjectTrackingId, radarObjectMeasurementStatus, radarObjectPosX, radarObjectPosY, radarObjectPosZ, radarObjectSpeed);
    
    // Calculate and publish results
    executeSimpleADASAlgorithm();
  }
  
  void executeSimpleADASAlgorithm()
  {
    // For simple demonstration purpose: React only on specific radar object from whom we know that it is braking in front of us
    if (radarObjectTrackingId == 2)
    {
      timeToImpact = 99999; // ms
      isWarningActive = 0;

      if (radarObjectMeasurementStatus == 2) // Radar object is active and measured
      {
        if (radarObjectPosY < 3.0 && radarObjectPosY > -3.0) // Radar object is in same lane
        {
          if (radarObjectSpeed < 0) // Radar Object is slower
          {
            timeToImpact = (radarObjectPosX / std::abs(radarObjectSpeed)) * 1000;

            if (timeToImpact < 3000) // ms
            {
              isWarningActive = 1;
            }
            else
            {
              isWarningActive = 0;
            }
          }
        }
      }
    }
    
    // Publish outputs
    auto output = adas_msgs::msg::OutputRos();
    output.results.time_to_impact = timeToImpact;
    output.results.is_warning_active = isWarningActive;
    
    RCLCPP_INFO(this->get_logger(), "Output ROS: '%f' '%d'", output.results.time_to_impact, output.results.is_warning_active);
    publisher->publish(output);
  }
  
  // Inputs: CANoe => ROS
  rclcpp::Subscription<adas_msgs::msg::InputRos>::SharedPtr subscription;
  uint64_t radarObjectTrackingId;
  uint64_t radarObjectMeasurementStatus;
  double radarObjectPosX;
  double radarObjectPosY;
  double radarObjectPosZ;
  double radarObjectSpeed;
  
  // Outputs: ROS => CANoe
  rclcpp::Publisher<adas_msgs::msg::OutputRos>::SharedPtr publisher;
  double timeToImpact;
  int32_t isWarningActive;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ADASNode>());
  rclcpp::shutdown();
  
  return 0;
}
