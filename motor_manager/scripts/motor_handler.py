#!/usr/bin/env python3
import RPi.GPIO as GPIO
import rospy
from geometry_msgs.msg import Twist          
from time import sleep
from signal import signal, SIGINT

in1 = 23
in2 = 24
in3 = 27
in4 = 22
en2 = 4
en = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(en, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)
p=GPIO.PWM(en,1000)
p2 = GPIO.PWM(en2, 1000)

def handler(signal_received, frame):
    #Clean GPIO pins when CTRL C
    GPIO.cleanup()


def motor_handler():
    rospy.init_node('motor_handler', anonymous=True)
    rospy.Subscriber('cmd_vel_robot', Twist, direction_callback)
    rospy.spin()

def direction_callback(data):
    if data.linear.y > 0:
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        p.ChangeDutyCycle(round(data.linear.y*100))
        p2.ChangeDutyCycle(round(data.linear.y*100))
    elif data.linear.y < 0:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        p.ChangeDutyCycle(-1*round(data.linear.y*100))
        p2.ChangeDutyCycle(-1*round(data.linear.y*100))
    elif data.linear.x > 0:
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        p.ChangeDutyCycle(round(data.linear.x*100))
        p2.ChangeDutyCycle(round(data.linear.x*100))
    elif data.linear.x < 0:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        p.ChangeDutyCycle(-1*round(data.linear.x*100))
        p2.ChangeDutyCycle(-1*round(data.linear.x*100))
    else:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)

def main(args=None):
    signal(SIGINT, handler)
    GPIO.setup(in1,GPIO.OUT)
    GPIO.setup(in2,GPIO.OUT)
    GPIO.setup(in3,GPIO.OUT)
    GPIO.setup(in4,GPIO.OUT)
    GPIO.setup(en,GPIO.OUT)
    GPIO.setup(en2,GPIO.OUT)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    p.start(0)
    p2.start(0)
    motor_handler()

if __name__ == '__main__':
    main()
