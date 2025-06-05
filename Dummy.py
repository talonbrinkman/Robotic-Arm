from machine import I2C, Pin
from pca9685 import PCA9685
import time
import random

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
pca = PCA9685(i2c)
pca.freq(50)

servos = [
    {'name': 'base', 'channel': 0, 'zeroAngle': 90, 'angle': 0, 'minAngle': 0, 'maxAngle': 180},
    {'name': 'shoulder', 'channel': 3, 'zeroAngle': 90, 'angle': 0, 'minAngle': 30, 'maxAngle': 150},
    {'name': 'elbow', 'channel': 4, 'zeroAngle': 90, 'angle': 0, 'minAngle': 0, 'maxAngle': 180},
]

def setServoAngle(channel, target_angle):
    delay = 0.02
    current_angle = None
    
    for servo in servos:
        if servo['channel'] == channel:
            current_angle = servo['angle']
            break
        
    step = 1 if target_angle > current_angle else -1

    servo_config = None
    for servo in servos:
        if servo['channel'] == channel:
            servo_config = servo
            break
    if servo_config:
        target_angle = max(servo_config['minAngle'], min(target_angle, servo_config['maxAngle']))
        
    for angle in range(current_angle, target_angle, step):
        min_pulse = 500
        max_pulse = 2500
        pulse_length = min_pulse + (angle / 180) * (max_pulse - min_pulse)
        duty = int((pulse_length / 20000) * 4095)
        pca.duty(channel, duty)
        for servo in servos:
            if servo['channel'] == channel:
                servo['angle'] = angle
        time.sleep(delay)

    min_pulse = 500
    max_pulse = 2500
    pulse_length = min_pulse + (target_angle / 180) * (max_pulse - min_pulse)
    duty = int((pulse_length / 20000) * 4095)
    pca.duty(channel, duty)
    
    for servo in servos:
        if servo['channel'] == channel:
            servo['angle'] = target_angle
    
def zeroServos():
    for servo in servos:
        setServoAngle(servo['channel'], servo['zeroAngle'])
        
def backAndForth():
    while True:
        for servo in servos:
            setServoAngle(servo['channel'], random.randint(0, 180))
        time.sleep(1)
try:
    zeroServos()
    time.sleep(1)
    backAndForth()
except KeyboardInterrupt:
    pass
finally:
    zeroServos()