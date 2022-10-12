#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
from ipaddress import ip_address
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative


# Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--protocol', help="Protocol used for the connection", default="tcp")
parser.add_argument('--ip', help="IP address for the connection", default="127.0.0.1")
parser.add_argument('--port',
                    help="initial port string for the connection",default="5760")
parser.add_argument('--instances', help="Number of instances to be connected", default="0")
args = parser.parse_args()

instances = int(args.instances)
initial_port = int(args.port)
ip_addr = args.ip
protocol = args.protocol

print(ip_addr)

connection_string = []
for i in range(instances):
    connection_string.append(protocol + ':' + ip_addr + ':' + str(initial_port+10*i))
    print(connection_string[i])
sitl = None


# Start SITL if no connection string specified
if len(connection_string) == 0:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string.append(sitl.connection_string())


# Connect to the Vehicle
vehicles = []
for i in range(instances):
    print('Connecting to vehicle on: %s' % connection_string[i])
    vehicles.append(connect(connection_string[i], wait_ready = True))
    print('Connected to vehicle on: %s' % connection_string[i])


# def arm_and_takeoff(aTargetAltitude):
#     """
#     Arms vehicle and fly to aTargetAltitude.
#     """

#     print("Basic pre-arm checks")
#     # Don't try to arm until autopilot is ready
#     while not vehicle.is_armable:
#         print(" Waiting for vehicle to initialise...")
#         time.sleep(1)

#     print("Arming motors")
#     # Copter should arm in GUIDED mode
#     vehicle.mode = VehicleMode("GUIDED")
#     vehicle.armed = True

#     # Confirm vehicle armed before attempting to take off
#     while not vehicle.armed:
#         print(" Waiting for arming...")
#         time.sleep(1)

#     print("Taking off!")
#     vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

#     # Wait until the vehicle reaches a safe height before processing the goto
#     #  (otherwise the command after Vehicle.simple_takeoff will execute
#     #   immediately).
#     while True:
#         print(" Altitude: ", vehicle.location.global_relative_frame.alt)
#         # Break and return from function just below target altitude.
#         if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
#             print("Reached target altitude")
#             break
#         time.sleep(1)


# arm_and_takeoff(10)

# print("Set default/target airspeed to 3")
# vehicle.airspeed = 3

# print("Going towards first point for 30 seconds ...")
# point1 = LocationGlobalRelative(-35.361354, 149.165218, 20)
# vehicle.simple_goto(point1)

# # sleep so we can see the change in map
# time.sleep(30)

# print("Going towards second point for 30 seconds (groundspeed set to 10 m/s) ...")
# point2 = LocationGlobalRelative(-35.363244, 149.168801, 20)
# vehicle.simple_goto(point2, groundspeed=10)

# # sleep so we can see the change in map
# time.sleep(30)

# print("Returning to Launch")
# vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting script
print("Closing vehicle objects")
for vehicle in vehicles:
    vehicle.close()

# Shut down simulator if it was started.
if sitl:
    sitl.stop()
