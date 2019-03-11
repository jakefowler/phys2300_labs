'''
Assignment to learn how to interpolate data1
'''
import sys
#import matplotlib.pyplot as plt
import numpy as np
import scipy
import pandas as pd

# https://youtu.be/-zvHQXnBO6c

def read_wx_data(wx_file, harbor_data):
    """
    Read temperature and time data from file.
    Populates the harbor_data dictionary with two lists: wx_times and wx_temperatures
    :param wx_file: File object with data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    data = pd.read_csv(wx_file, usecols=[1,3])
    harbor_data["wx_data"] = data
    harbor_data["wx_times"] = data["Time"] #.tolist()
    harbor_data["wx_temperatures"] = data["Ch1:Deg F"] #.tolist()
    #print(harbor_data)
    

def read_gps_data(gps_file, harbor_data):
    """
    Read gps and altitude data from file.
    Populates the harbor_data dictionary with two lists: gps_times and gps_altitude
    :param gps_file: File object with gps data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    data = pd.read_csv(gps_file, sep='\t', skiprows=[1]) # I needed to add lineterminator='\r' to work on mac
    #print(data)
    print(data.columns[-1].values)
    harbor_data["gps_times"] = data.iloc[:, :3]
    harbor_data["gps_altitude"] = data.iloc[:,-1]
    print("altitude\n",data.iloc[:,-1])


def interpolate_wx_from_gps(harbor_data):
    """
    Compute wx altitudes by interpolating from gps altitudes
    Populates the harbor_data dictionary with four lists:
        1) wx correlated altitude up
        2) wx correlated temperature up
        3) wx correlated altitude down
        4) wx correlated temperature down
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    pass


def plot_figs(harbor_data):
    """
    Plot 2 figures with 2 subplots each.
    :param harbor_data: A dictionary to collect data.
    :return: nothing
    """
    pass


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
    print("Data after it has all been read in")
    print(harbor_data)

if __name__ == '__main__':
    main()
    exit(0)
