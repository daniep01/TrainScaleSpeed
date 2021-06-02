# TrainScaleSpeed
Use infrared light sensors and a RaspberryPi to calculate train speed on a model railway.

## Parts Used
- 2x [IR break beam sensors](https://thepihut.com/products/ir-break-beam-sensor-3mm-leds)
- 1x RaspberryPi (any type with GPIO)

## Operation
Sensors are placed 24 inches apart on either side of the track. The code assumes GPI 17 and 18 are used. With the script running a train passes between the sensors and the speed is calculated and displayed.
