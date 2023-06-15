#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist          
from time import sleep
from getkey import getkey, keys
from sys import exit

message = Twist()
speed = 0.5

def keyboard_publisher():
    publisher = rospy.Publisher('cmd_vel_robot', Twist, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    key = 'k'
    #Default settings, STOP and 50% of speed
    global message
    message.linear.x = 0.0
    message.linear.y = 0.0
    rospy.loginfo("Keyboard teleop is ON, press h for help")
    while not rospy.is_shutdown():
        sleep(0.1)
        key = getkey()
        if key == 'w':
            set_y(1)
            set_x(0)
            rospy.loginfo("Going forward...")
            publisher.publish(message)

        elif key == 's':
            set_y(-1)
            set_x(0)
            rospy.loginfo("Going backward...")
            publisher.publish(message)

        elif key == 'a':
            set_x(1)
            set_y(0)
            rospy.loginfo("Going left...")
            publisher.publish(message)

        elif key == 'd':
            set_x(-1)
            set_y(0)
            rospy.loginfo("Going right...")
            publisher.publish(message)

        elif key == 'q':
            decrease_speed()
            rospy.loginfo("Decreasing speed...")
            publisher.publish(message)

        elif key == 'e':
            increase_speed()
            rospy.loginfo("Increasing speed...")
            publisher.publish(message)

        elif key == 'x':
            set_x(0)
            set_y(0)
            rospy.loginfo("Stop...")
            publisher.publish(message)

        elif key == 'p':
            rospy.loginfo("Exiting program...")
            sleep(1)
            exit(0)

        elif key == 'h':
            rospy.loginfo("Help Menu")
            rospy.loginfo("\n  Help Menu  \n" +
                                    "w forward\n" +
                                    "s backward\n" +
                                    "a left\n" +
                                    "d right\n" +
                                    "q decrease speed\n" +
                                    "e increase speed\n" +
                                    "x stop\n" +
                                    "h help\n" +
                                    "p exit\n"
                                    )
        elif key == '`':
            pass

        else:
            rospy.loginfo("Unknown key, press h for help")
        
        key = '`'

def increase_speed():
    global message
    global speed
    speed += 0.05
    if(speed > 1):
        speed = 1 
    if message.linear.x > 0:
        set_x(1)
    elif message.linear.x < 0:
        set_x(-1)
    else:
        set_x(0)

    if message.linear.y > 0:
        set_y(1)
    elif message.linear.y < 0:
        set_y(-1)
    else:
        set_y(0)

def decrease_speed():
    global message
    global speed
    speed -= 0.05
    if(speed < 0.1):
        speed = 0.1
    if message.linear.x > 0:
        set_x(1)
    elif message.linear.x < 0:
        set_x(-1)
    else:
        set_x(0)

    if message.linear.y > 0:
        set_y(1)
    elif message.linear.y < 0:
        set_y(-1)
    else:
        set_y(0)

def set_x( val):
    global message
    message.linear.x = round(float(val*speed),2)

def set_y( val):
    global message
    message.linear.y = round(float(val*speed),2)

if __name__ == '__main__':
    try:
        keyboard_publisher()
    except rospy.ROSInterruptException:
        pass