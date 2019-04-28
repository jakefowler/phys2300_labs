"""
This program takes data GPS and temperature data of a helium ballon from two different files. 
One file is comma separated and the other is tab separated. The GPS data is a lot less frequent 
so the data needed to be interpolated. There is also a lot of extra data from when the balloon
was on the ground after that was stripped off. The data is then graphed.
"""
import sys
import matplotlib.pyplot as plt
import numpy as np
import scipy
import pandas as pd
import csv
from datetime import datetime as dt

def read_wx_data(wx_file, harbor_data):
    """
    Read temperature and time data from file.
    Populates the harbor_data dictionary with two lists: wx_times and wx_temperatures
    :param wx_file: File object with data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    data = pd.read_csv(wx_file, usecols=[1,3]) # reads in the time and temperature columns into a pandas dataframe
    times = data["Time"].values
    startTime = dt.strptime(times[0], '%H:%M:%S') # first time in file used to find delta time
    harbor_data["wx_times"] = []
    for time in times:
        delta_t = dt.strptime(time,'%H:%M:%S') - startTime
        harbor_data['wx_times'].append(float(delta_t.total_seconds()/3600))
    harbor_data["wx_temperatures"] = data["Ch1:Deg F"].tolist()
    for temp in harbor_data["wx_temperatures"]:
        temp = float(temp)

def read_gps_data(gps_file, harbor_data):
    """
    Read gps and altitude data from file.
    Populates the harbor_data dictionary with two lists: gps_times and gps_altitude
    :param gps_file: File object with gps data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    hours = [] # list to hold the times converted to hours
    altitude = [] # list to hold the altitudes from the file
    with open(gps_file, newline = '') as tabFile:
        tabFile = csv.reader(tabFile, delimiter='\t')
        next(tabFile, None)
        next(tabFile, None)
        firstLine = next(tabFile)
        startingTime = float(firstLine[0]) + (float(firstLine[1])/60) + (float(firstLine[2])/3600)
        hours.append(0.0)
        altitude.append(float(firstLine[6]))
        for line in tabFile:
            hours.append(float(line[0]) + (float(line[1])/60) + (float(line[2])/3600) - startingTime)
            altitude.append(float(line[6]))
    harbor_data["gps_times"] = hours
    harbor_data["gps_altitude"] = altitude

def interpolate_wx_from_gps(harbor_data):
    """
    Compute wx altitudes by interpolating from gps altitudes
    Populates the harbor_data dictionary with four lists:
        1) wx correlated altitude up
        2) wx correlated temperature up
        3) wx correlated altitude down
        4) wx correlated temperature down
        5) wx correlated altitude
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    wx_correlated_alt = [] # list to hold all of the correlated altitudes to be used for first plot
    cutoff_index = 0 # variable to hold the index where the wx_times is over the max gps_times
    max_gps_time = max(harbor_data['gps_times']) # used for cutting out the extra data from the wx data that is past this time
    count_to_add = 0 # variable to keep track of how many numbers need to be added inbetween alt values for interpolation
    index = 0 # index used for the gps data while looping through the wx_times data
    for time in harbor_data["wx_times"]:
        if time > max_gps_time:
            wx_correlated_alt.extend(np.linspace(harbor_data["gps_altitude"][index - 1],
                                        harbor_data["gps_altitude"][index],
                                        num=count_to_add)) 
            break
        if(time > harbor_data["gps_times"][index]):
            if index == 0:
                wx_correlated_alt.extend(np.linspace(harbor_data["gps_altitude"][index], harbor_data["gps_altitude"][index], num=count_to_add + 1)) # this may make the len incorrect
            else:
                wx_correlated_alt.extend(np.linspace(harbor_data["gps_altitude"][index - 1], harbor_data["gps_altitude"][index], num=count_to_add + 1)) # this may make the len incorrect
            count_to_add = 0
            index += 1
        else:
            count_to_add +=1
        cutoff_index += 1
    
    harbor_data["wx_times"] = harbor_data["wx_times"][:cutoff_index]
    harbor_data["wx_temperatures"] = harbor_data["wx_temperatures"][:cutoff_index]

    index_max_alt = wx_correlated_alt.index(max(wx_correlated_alt))
    harbor_data["wx_correlated_alt"] = wx_correlated_alt
    harbor_data["wx_correlated_alt_up"] = wx_correlated_alt[:index_max_alt + 1]
    harbor_data["wx_correlated_alt_down"] = wx_correlated_alt[index_max_alt:]
    harbor_data["wx_correlated_temp_up"] = harbor_data["wx_temperatures"][:index_max_alt + 1]
    harbor_data["wx_correlated_temp_down"] = harbor_data["wx_temperatures"][index_max_alt:]

def plot_figs(harbor_data):
    """
    Plot 2 figures with 2 subplots each.
    :param harbor_data: A dictionary to collect data.
    :return: nothing
    """
    plt.figure(1)
    plt.subplot(2, 1, 1)
    plt.title("Harbor Flight Data")
    plt.plot(harbor_data["wx_times"], harbor_data["wx_temperatures"])
    plt.ylabel("Temperature, F")

    plt.subplot(2, 1, 2)
    plt.ylabel("Altitude, ft")
    plt.xlabel("Mission Elapsed Time, Hours")
    plt.plot(harbor_data["wx_times"], harbor_data["wx_correlated_alt"])
    plt.show()

    plt.figure(2)
    plt.subplot(1, 2, 1)
    plt.title("Harbor Ascent Flight Data")
    plt.ylabel("Altitude, Ft")
    plt.xlabel("Temperature, F")
    plt.plot(harbor_data["wx_correlated_temp_up"], harbor_data["wx_correlated_alt_up"])

    plt.subplot(1, 2, 2)
    plt.title("Harbor Descent Flight Data")
    plt.xlabel("Temperature, F")
    plt.yticks([20000, 40000, 60000, 80000])
    plt.plot(harbor_data["wx_correlated_temp_down"], harbor_data["wx_correlated_alt_down"])
    plt.show()
    
def main():
    """
    Main function
    :return: Nothing
    """
    harbor_data = {}
    #wx_file = sys.argv[1]                   # first program input param
    wx_file = "./TempPressure.txt"
    #gps_file = sys.argv[2]                  # second program input param
    gps_file = "./GPSData.txt"

    read_wx_data(wx_file, harbor_data)      # collect weather data
    read_gps_data(gps_file, harbor_data)    # collect gps data
    interpolate_wx_from_gps(harbor_data)    # calculate interpolated data
    plot_figs(harbor_data)                  # display figures

if __name__ == '__main__':
    main()
    exit(0)
