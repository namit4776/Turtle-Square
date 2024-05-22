#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class TurtleSquareDrawer:
    def __init__(self):
        rospy.init_node('turtle_square_drawer', anonymous=True)
        self.vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.pose_sub = rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)
        self.pose = Pose()
        self.rate = rospy.Rate(10)  # Loop rate of 10 Hz

    def update_pose(self, data):
        self.pose = data

    def move_straight(self, distance):
        velocity_message = Twist()
        velocity_message.linear.x = 1.0
        velocity_message.angular.z = 0.0

        start_x = self.pose.x
        start_y = self.pose.y

        while not rospy.is_shutdown():
            traveled_distance = math.sqrt((self.pose.x - start_x) ** 2 + (self.pose.y - start_y) ** 2)
            if traveled_distance >= distance:
                break
            self.vel_pub.publish(velocity_message)
            self.rate.sleep()

        velocity_message.linear.x = 0.0
        self.vel_pub.publish(velocity_message)

    def rotate_by_angle(self, degrees):
        velocity_message = Twist()
        velocity_message.linear.x = 0.0
        velocity_message.angular.z = math.radians(30)

        start_time = rospy.Time.now().to_sec()
        current_angle = 0

        while not rospy.is_shutdown():
            current_time = rospy.Time.now().to_sec()
            current_angle = 30 * (current_time - start_time)
            if current_angle >= degrees:
                break
            self.vel_pub.publish(velocity_message)
            self.rate.sleep()

        velocity_message.angular.z = 0.0
        self.vel_pub.publish(velocity_message)

    def draw_square(self, side_length):
        for _ in range(4):
            self.move_straight(side_length)
            self.rotate_by_angle(90)

    def start_drawing(self):
        while not rospy.is_shutdown():
            self.draw_square(2.0)

if __name__ == '__main__':
    try:
        turtle_square_drawer = TurtleSquareDrawer()
        turtle_square_drawer.start_drawing()
    except rospy.ROSInterruptException:
        pass
