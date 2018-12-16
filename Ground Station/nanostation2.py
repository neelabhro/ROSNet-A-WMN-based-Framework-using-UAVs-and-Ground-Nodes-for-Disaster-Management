#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import glob
import os
import subprocess
import shutil

bridge = CvBridge()
img_dir = "/home/dcs/Desktop/send/"
data_path = os.path.join(img_dir, '*g')
files = glob.glob(data_path)
count = 0
i = 0
loop = 0
length = len(files)
flag = 0
n = 0
m = 0
l = 0
flag1 = 0

path1 = "/home/dcs/Desktop/receive"
os.chdir(path1)
a = subprocess.check_output("date")
a = str(a[0:-1])
a = a.replace(" ", "_")
subprocess.Popen(['mkdir', a])
src = '/home/dcs/Desktop/receive/%s/'%a


def callback(msg):
	global i
	print("Receiving files from drone")
	try:
		cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
	except CvBridgeError, e:
		print(e)
	else:
		cv2.imwrite("/home/dcs/Desktop/receive/%s/img%s_%i.jpg"%(a, a, i), cv2_img)
	i += 1

def sender():
	global length
	info_pub.publish(length)
	for f1 in files:
		print("sending file to drone")
		img = cv2.imread(f1)
		image_pub.publish(bridge.cv2_to_imgmsg(img, "bgr8"))
		rate.sleep()
	flag = 1
	send_confirm.publish(flag)

def info(data):
	global n
	n = data.data
	print('No of files to be received: ', data.data)

def confirm(var):
	global m
	m += 1

def receive(var2):
	global l
	l += 1


def main():
	global count, loop, image_pub, info_pub, rate, flag, send_confirm, flag1, l
	rospy.init_node('nanostation1', anonymous = True)
	info_pub = rospy.Publisher('nano_info', Int32, queue_size = 10)
	rospy.Subscriber('drone_info', Int32, info)
	rospy.Subscriber('receive_topic', Int32, confirm)
	rospy.Subscriber('send_topic', Int32, receive)
	send_confirm = rospy.Publisher('confirmation', Int32, queue_size = 10)
	image_pub = rospy.Publisher('image_receiver_nano1', Image, queue_size = 10)
	rospy.Subscriber('image_sender', Image, callback)

	rate = rospy.Rate(1)

	while not (rospy.is_shutdown()):
		inform = info_pub.get_num_connections()
		connections = image_pub.get_num_connections()

		if (inform == 1 and connections == 1 and flag1 == 0):
			print("drone connected")
			flag1 = 1

		if (i == n and l == 1):
			rospy.sleep(1)
			sender()
			print("all files sent")
			l = 0

		if (m == 1):
			print('all files received by drone')
			rospy.sleep(2)
			print("copying files to send folder..")
			source = os.listdir(src)
			for files in source:
				full_path = os.path.join(src, files)
				if full_path.endswith(".jpg"):
					shutil.copy(full_path, img_dir)
			print('successfully copied')
			rospy.sleep(2)
			break
		rate.sleep()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
