#!/usr/bin/python

"""
Meta-Blue Visualise Bluetooth Low Energy Metadata
# https://github.com/karulis/pybluez - pybluez library
# sudo apt-get install libbluetooth-dev
#https://matplotlib.org/users/pyplot_tutorial.html - dual graph tutorial

sudo apt-get install pkg-config
sudo apt-get install libboost-python-dev
sudo apt-get install libboost-thread-dev
sudo apt-get install libbluetooth-dev
sudo apt-get install libglib2.0-dev
sudo apt-get install python-dev
sudo pip install gattlib
sudo pip install matplotlib
sudo apt-get install python-tk
sudo pip install pybluez

"""


from bluetooth.ble import DiscoveryService
from time import gmtime, strftime, localtime
import time
import re
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import random

# Discovery Service used to identify devices
service = DiscoveryService()

# Set of MAC addresses
mac_set = set()

# List of MAC addresses in a single scan (formerly dev_list)
mac_list = []

# Colour list
colours = ['b','g','r','c','m','y','k']
# Can be updated - https://matplotlib.org/2.0.2/api/colors_api.html

# Dictionary to hold device colours
dev_colours = {}

#scatter_size = 5

def lescan(time_window):
	"""
	Finds devices in range within specified time window, return a list of devices
	"""
	devices = service.discover(time_window)
	# empty the list for each scan
	del mac_list[:]
	for address in devices:
		mac_list.append(address)
	return mac_list


def graph(graph_time):
	"""
	#Create a matrix of mac addresses against time
	"""
	graph_time = int(graph_time)
	
	scatter_size = 40 / graph_time 
	
	if scatter_size < 2:
		scatter_size = 2	
	print "Scatter size = ", scatter_size
	#scatter_size  = 6
	#exit()
	
	scan_window = 2 # time each scan is active for, 2 is best for consistency
	graph_time = int(graph_time)*60
			
	graph_time = int(graph_time)/scan_window
	# dictionary to store mac addresses and values to graph
	mac_dict = {}
	mac_value_count = 1	
	
	# Lists to store data for device number graph
	num_dev = []
	
	# Max number used to set graph y limit
	max_number = 0
	
	# Setup the graphs
	
	graph_time = int(graph_time)
	
	
	
	plt.ion()
	#fig, axarr = plt.subplots(2, sharex=True)
	fig, axarr = plt.subplots(2)
	axarr[0].set_title("BLE Metadata Tracking")
	#axarr[0].set_xlabel("Time")
	axarr[1].set_xlabel("Time (s)")
	axarr[0].set_ylabel("Number of Devices")
	axarr[1].set_ylabel("Device ID")
	axarr[0].grid(color='k', linestyle=':', linewidth=1)
	axarr[1].grid(color='k', linestyle=':', linewidth=1)
	
	times = []
	
	for i in range(graph_time+1):
		macs = lescan(scan_window)
		number = len(macs)
		if number > max_number:		
			max_number = number
		num_dev.append(number)
		times.append(i*scan_window)
		axarr[0].plot(times, num_dev, linewidth=1,c='r')
		#axarr[0].scatter(i*2,number, c='r', s=scatter_size)	
		
			
		
		for mac in macs:
			if mac in mac_dict:
				existing_mac_value = mac_dict[mac]
				colour = dev_colours[existing_mac_value]
				axarr[1].scatter(i*scan_window,existing_mac_value, c=colour, s=scatter_size)
			else:
				print mac
				mac_dict[mac] = mac_value_count
				colour = (random.choice(colours))
				dev_colours[mac_value_count] = colour
				axarr[1].scatter(i*scan_window,mac_value_count, c=colour, s=scatter_size)
				mac_value_count+=1
		
		plt.pause(0.0001)
		
	while(1):
		plt.pause(100)
	
	
graph(sys.argv[1])
# Usage 
# sudo python Meta-Blue.py 5
