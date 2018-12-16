#!/usr/bin/env python
import subprocess
while True:
	process = subprocess.Popen(['ping', '-w', '3', '-i', '0.2', '-s', '65500', '192.168.1.150'])
	process.wait()
	output = process.poll()

	if output == 0:
		print("connected to Ground Station")
		break
	else:
		print("no connection")
#subprocess.Popen(['./cvcam.py'])

subprocess.Popen(['./nano2_comm.sh'])

