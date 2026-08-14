# arduino-radar
DIY Arduino Radar using HC-SR04 ultrasonic sensor and servo motor. Real-time distance detection and 180-degree scanning.
# Arduino Radar

A real-time ultrasonic radar system built with Arduino, HC-SR04 ultrasonic sensor, servo motor, and Python/Pygame visualization.

The system scans the surrounding area by rotating an ultrasonic sensor and measures the distance of objects at different angles. The Arduino sends the measured angle and distance to a computer through USB Serial communication, while a Python application displays the measurements as a radar interface.

---

## Project Overview

This project is a DIY Arduino-based radar scanner designed for learning and experimenting with:

- Arduino programming
- Ultrasonic distance measurement
- Servo motor control
- Serial communication
- Python programming
- Real-time data visualization
- Robotics
- Mechatronics
- Embedded systems

The ultrasonic sensor is mounted on a servo motor. The servo rotates the sensor through approximately 180 degrees.

At each angle, the HC-SR04 measures the distance to an object.

The Arduino then sends the measurement to the computer using Serial communication.

The Python visualization receives the data and displays:

- Radar scanning angle
- Detected object
- Object distance
- Scanning direction
- System status
- Simulation mode or Arduino connection status

---

# System Architecture

The complete system works as follows:

```text
             ┌──────────────────┐
             │     HC-SR04      │
             │ Ultrasonic Sensor│
             └────────┬─────────┘
                      │
                      │ Distance
                      ▼
             ┌──────────────────┐
             │     Arduino      │
             │                  │
             │ Servo Control    │
             │ Distance Measure │
             └────────┬─────────┘
                      │
                      │ USB Serial
                      │ 9600 baud
                      ▼
             ┌──────────────────┐
             │      Python      │
             │                  │
             │    PySerial      │
             │       +          │
             │     Pygame       │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │ Radar Visualizer │
             │                  │
             │ Angle            │
             │ Distance         │
             │ Object Detection │
             └──────────────────┘
## 🎥 Demo

Watch the Arduino Radar in action:

[![Arduino Radar Demo](https://img.youtube.com/vi/O_y4yvUxZsg/maxresdefault.jpg)](https://www.youtube.com/watch?v=O_y4yvUxZsg)

▶️ **[Watch the full demo on YouTube](https://www.youtube.com/watch?v=O_y4yvUxZsg)**
