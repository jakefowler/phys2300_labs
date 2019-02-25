'''
--------------------------------------------------------------------------------
G e n e r a l I n f o r m a t i o n
--------------------------------------------------------------------------------
Name: weather.py

Usage: python datafile

Description: Code to analyze weather data

Inputs: name of data file containing weather data

Outputs: plots and analysis

Auxiliary Files: None

Special Instructions: None

--------------------------------------------------------------------------------
'''
import sys
import matplotlib.pylab as plt
import numpy as np

# Pseudocode:
# 1) get the name of the data file from the user on the command line
# 2) open the data file
# 3) read the first line of data and throw it away (it is the header info the computer doesn't need)
#       from all the remaining lines:
#       read in the date (index 2) and temperature (index 3)
#       parse the date string into year, month, day
#       convert year, month, day into decimal years for plotting
# 4) make two lists for the time series - the decimal year list and the temperature list
# 5) sort the data by month so we can average it and take the standard deviation later
# 6) Plot the results


def parse_data(infile):
    """
    Function to parse weather data
    :param infile: weather data input file
    :return: two lists. One list with the information from the third column (date) and the fourth column (temperature)
                        One list with the information from the third column (date) and the 18th (min) and 19th column (max temp)
    """
 
    wdates_and_temp = []    # list of dates data broken up into year, month, day, and then the temperature for that day
    wdates_min_max = []     # list of year along with min and max temperatures for each day

    with open(infile, mode='r') as file:
        data = file.readlines()[1:]

        for line in data:
            values = line.split()
            date = values[2]
            wdates_and_temp.append([float(date[0:4]), float(date[4:6]), float(date[6:]), float(values[3])])
            wdates_min_max.append([float(date[0:4]), float(values[18]), float(values[17])])
        
    file.close()

    return wdates_and_temp, wdates_min_max

def calc_mean_std_dev(wdates_and_temp):
    """
    Calculate the mean temperature per month
    Calculate the standard deviation per month's mean
    :param wdates: list with dates fields
    :param wtemp: temperature per month
    :return: means, std_dev: months_mean and std_dev lists
    """
    means = []
    std_dev = []
    temp_list = []
    wdates_and_temp.sort(key = lambda x: x[1])

    month = 1.0
    for val in wdates_and_temp:
        if val[1] > month:
            month += 1
            means.append(np.mean(temp_list))
            std_dev.append(np.std(temp_list))
            temp_list.clear()
        temp_list.append(val[3])
        
    means.append(np.mean(temp_list))
    std_dev.append(np.std(temp_list))
    return means, std_dev

def plot_data_task1(wyear, wtemp, month_mean, month_std):
    """
    Create plot for Task 1.
    :param: wyear: list with year (in decimal)
    :param: wtemp: temperature per
    :param: month_mean: list with month's mean values
    :param: month_std: list with month's mean standard dev values
    """
    # Create canvas with two subplots
    plt.figure()
    plt.subplot(2, 1, 1)                # select first subplot
    plt.title("Temperatures at Ogden")
    plt.plot(wyear, wtemp, "bo")
    plt.ylabel("Temperature, F")
    plt.xlabel("Decimal Year")

    plt.subplot(2, 1, 2)                # select second subplot
    plt.ylabel("Temperature, F")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthNumber = list(range(1, 13, 1))
    plt.xlim([0.7, 13])
    plt.ylim([0, 90])
    width = 0.8
    plt.bar(monthNumber, month_mean, yerr=month_std, width=width,
            color="lightgreen", ecolor="black", linewidth=1.5)
    plt.xticks(monthNumber, months)
    plt.show()      # display plot

def calc_min_max(wdates_min_max):
    """
    Function that finds the min and max temperature for each year and then returns it as a list.
    :param: wdates_min_max: list that contains the year, min, and max temperatures
    :returns: year_min_max: list with the min and max temperature of each year
    """
    year_min_max = []
    min_temp = 212
    max_temp = 0
    wdates_min_max.sort(key = lambda x: x[0])
    year = wdates_min_max[0][0] 
    for val in wdates_min_max:
        if val[0] > year:
            year_min_max.append([year, min_temp, max_temp])
            year = val[0]
            min_temp = val[1]
            max_temp = val[2]
        if val[1] < min_temp:
            min_temp = val[1]
        if val[2] > max_temp and val[2] < 200:
            max_temp = val[2]
    year_min_max.append([year, min_temp, max_temp])

    return year_min_max


def plot_data_task2(year_min_max):
    """
    Function that plots the min and max temperatures for each year
    :param: year_min_max: list that holds the year and the min and max temperatures for that year
    """
    year = np.array(year_min_max)[:,0].tolist()
    min = np.array(year_min_max)[:,1].tolist()
    max = np.array(year_min_max)[:,2].tolist()
    plt.plot(year, min, "bo", label="Minimum Temp")
    plt.plot(year, max, "ro", label="Maximum Temp")
    plt.ylabel("Temperature, F")
    plt.xlabel("Year")
    plt.title("Min and Max Temperature by Year")
    plt.legend()
    plt.show()



def main(infile):
    weather_data = infile    # take data file as input parameter to file
    wdates_and_temp, wdates_min_max = parse_data(weather_data)
    # Calculate mean and standard dev per month
    month_mean, month_std = calc_mean_std_dev(wdates_and_temp)
    #               1) years,                                 2) temperature,                       3) month_mean, 4) month_std
    plot_data_task1(np.array(wdates_and_temp)[:,0].tolist(), np.array(wdates_and_temp)[:,-1].tolist(), month_mean, month_std)
    year_min_max = calc_min_max(wdates_min_max)
    plot_data_task2(year_min_max)



if __name__ == "__main__":
    # infile = 'data/CDO6674605799016.txt'  # for testing
    # Note: the 0th argument is the program itself.
    infile = sys.argv[1]
    main(infile)
    # exit(0)
