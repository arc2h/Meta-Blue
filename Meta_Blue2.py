#!/usr/bin/python

# https://pythonprogramming.net/live-graphs-matplotlib-tutorial/
# https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.subplots.html
# https://www.scivision.dev/matplotlib-force-integer-labeling-of-axis/

"""
Bluetooth Visualisation, using the MatplotLib Animation function 

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


import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

from bluetooth.ble import DiscoveryService
from time import gmtime, strftime, localtime
import time
import re
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import random

from matplotlib.ticker import MaxNLocator

style.use('fivethirtyeight')

# Discovery Service used to identify devices
service = DiscoveryService()

# Set of MAC addresses
mac_set = set()

# List of MAC addresses in a single scan (formerly dev_list)
mac_list = []

# Dictionaries to store device ID's and colours
mac_dict = {}
dev_colours = {}

# Colour list
colours = ['b','g','r','c','m','y','k']
# Can be updated - https://matplotlib.org/2.0.2/api/colors_api.html

start_time = time.time()

# Lists to hold times and number of devices
xs = [] # Time
ys = [] # Devices

# Setup graph
# Create Figure with subplots 2 deep 1 wide
fig, axs = plt.subplots(2,1, sharex=True)
#axs[0].set_title("Number of Devices")
#axs[1].set_title("Device Identities")
axs[0].set_ylabel("Number of Devices")
axs[1].set_xlabel("Time (s)")
axs[0].yaxis.set_major_locator(MaxNLocator(integer=True))
axs[1].set_ylabel("Device ID")
axs[1].yaxis.set_major_locator(MaxNLocator(integer=True))
fig.suptitle("Bluetooth Device Tracking", fontsize=24)
fig.canvas.set_window_title("Meta_Blue")

mac_value_count = 1

print "Devices seen in current run"

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

def animate(i):
	"""
	Uses the animation function to create animated graphs
	"""
	global mac_value_count
	global dev_colours
	
	current_time = time.time() - start_time	
	
	timer = 1
	devices = lescan(timer)
	num_devices = len(devices)
	
	# Update lists for number of devices over time
	xs.append(current_time)
	ys.append(num_devices)
	
	
	# Plot number of devices
	axs[0].plot(xs, ys, linewidth=1,c='r')
	
	# Plot MAC addresses from current list, do not clear each time, to persist previous mac addresses
	for mac in devices:
		if mac in mac_dict:
			existing_mac_value = mac_dict[mac]
			colour = dev_colours[existing_mac_value]
			#print mac, colour, existing_mac_value
			axs[1].scatter(current_time, existing_mac_value, c=colour)
		
		else:
			print mac
			mac_dict[mac] = mac_value_count
			colour = (random.choice(colours))
			dev_colours[mac_value_count] = colour
			axs[1].scatter(current_time ,mac_value_count, c=colour)#, s=scatter_size)
			mac_value_count+=1
			#print "new", mac, colour

# Animate the figure at 1000ms intervals
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()

