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

img_dir = "/home/dcs/Desktop/send"
data_path = os.path.join(img_dir, '*g')
files = glob.glob(data_path)
count = 0
i = 0
loop = 0
length = len(files)
n = 0
flag = 0
flag1 = 0
flag2 = 0

bridge = CvBridge()

path1 = "/home/dcs/Desktop/receive"
os.chdir(path1)
a = subprocess.check_output("date")
a = str(a[0:-1])
a = a.replace(" ", "_")
subprocess.Popen(['mkdir', a])
src = '/home/dcs/Desktop/receive/%s/'%a

def callback1(msg):
	global i
	print("Receiving image from Central Server")
	try:
		cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
	except CvBridgeError, e:
		print(e)
	else:
		cv2.imwrite("/home/dcs/Desktop/receive/%s/nano1%s_%i.jpg"%(a, a, i), cv2_img)
	i += 1

def callback2(msg):
	global i
	print("Receiving image from Ground Station 1")
	try:
		cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
	except CvBridgeError, e:
		print(e)
	else:
		cv2.imwrite("/home/dcs/Desktop/receive/%s/nano2%s_%i.jpg"%(a, a, i), cv2_img)
	i += 1

def sender():
	global length
	info_pub.publish(length)
	for f1 in files:
		print("sending image")
		img = cv2.imread(f1)
		image_pub.publish(bridge.cv2_to_imgmsg(img, "bgr8"))
		rate.sleep()
	flag2 = 1
	send_confirm.publish(flag2)


def info(data):
	global n
	n = data.data
	print("no of files to be received: ", data.data)

def confirm(var):
	global flag1
	flag1 += 1
	



def main():
	global count, loop, image_pub, info_pub, rate, flag, send_confirm, flag2
	rospy.init_node("drone", anonymous = True)
	info_pub = rospy.Publisher('drone_info', Int32, queue_size = 10)
	rospy.Subscriber('nano_info', Int32, info)
	rospy.Subscriber('confirmation', Int32, confirm)
	send_confirm = rospy.Publisher('send_topic', Int32, queue_size = 10)
	receive_pub = rospy.Publisher('receive_topic', Int32, queue_size = 10)
	image_pub = rospy.Publisher('image_sender', Image, queue_size = 10)
	rospy.Subscriber('image_receiver_nano1', Image, callback2)
	rospy.Subscriber('image_receiver_nano2', Image, callback1)

	bridge = CvBridge()

	rate = rospy.Rate(1)
	
	while not (rospy.is_shutdown()):
		inform = info_pub.get_num_connections()
		connections = image_pub.get_num_connections()

		if (inform == 1 and connections == 1 and flag == 0):
			print("receiver connected")
			sender()
			print("all files sent")
			rospy.sleep(3)
			flag = 1

		if (i == n and flag == 1 and flag1 == 1):
			receive_pub.publish(flag1)
			rospy.sleep(1)
			print("All files received")
			rospy.sleep(2)
			print("copying files to send folder ..")
			source = os.listdir(src)
			for f in source:
				full_path = os.path.join(src, f)
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
