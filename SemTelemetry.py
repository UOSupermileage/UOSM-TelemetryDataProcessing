import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def inst_efficiency(joule1, speed1, joule2, speed2, t1, t2):
    """
Determines the instantaneous efficiency between two points in time

Parameters
----------

joule1 : float
         all_energy at t1
speed1 : float
         gps_speed at t1
joule1 : float
         all_energy at t1

joule2 : float
         all_energy at t2
speed2 : float
         gps_speed at t2
joule2 : float
         all_energy at t2
t1 : float
         time at t1
t2 : float
         time at t2

"""
    distance = ((speed1 + speed2) / 3.6 / 2) * (t2 - t1) * 3600
    return distance / 1000 / ((joule2 - joule1) / 3600000)

"""

"""
class SemTelemetry:
    def __init__(self, file, start, stop):
        # TODO: perhaps we can read the file to determine start and stop

        self.file = file
        self.start = start
        self.stop = stop
        try:
            self.data = pd.read_csv(file, delimiter=";", index_col=0)
        except FileNotFoundError:
            print("File Not Found. Ensure it is in the current directory")

    # TODO: determine desired functions
    # TODO: make functions that will execute the desired analysis for given run, optional parameters i.e steps

    # TODO: separate into their own functions or establish case for each type of graph

    def get_inst_efficiency(self, samples, start=self.start, stop=self.stop):
        """
        Determines the instantaneous efficiency from the specified run
        :param start: the first recording ID in the evaluated file
        :param stop: the last recording ID in the evaluated file
        :param samples: the number of data samples to be considered as one instant
        :return:
        """
        # start is beginning index , stop is end index
        # pre-condition: the start and stop indexes as well as file name are valid
        i = start + samples
        timeRef = self.data["Time"][start]
        time = []
        inst_eff = []
        while i < stop:
            inst_eff.append(
                inst_efficiency(self.data["all_energy"][i - samples], self.data["gps_speed"][i - samples],
                                self.data["all_energy"][i], self.data["gps_speed"][i], self.data["Time"][i - samples],
                                self.data["Time"][i]))
            time.append((self.data["Time"][i - samples / 2] - timeRef) * 3600)
            i += 1
        print("Overall", np.average(inst_eff))

        return time, inst_eff

    def eff_speed_current_v_time(self, samples, start=self.start, stop=self.stop):
        current = self.data['jm3_current'] / 1000
        time1 = (self.data["Time"] - self.data["Time"][start]) * 3600
        speed = self.data["gps_speed"]
        time, inst_eff = self.get_inst_efficiency(samples, start, stop)

        plt.figure(figsize=(14, 9))
        plt.plot(time1, speed, "-", label="Speed (km/h)")
        plt.plot(time1, current, "-", label="Current (A)")
        plt.title("Instantaneous Efficiency and Current")
        plt.xlabel("Time (s)")
        plt.ylabel("Instantaneous Efficiency (km/kWh)")
        plt.ylim([0, 120])
        # plt.xlim([0,1000])
        plt.plot(time[0:len(time)], inst_eff[0:len(inst_eff)], "-o", markersize=2, label="Efficiency (km/kWh)")
        plt.legend()
        plt.show()

    def current_speed_voltage_v_time(self):
        current = self.data["jm3_current"] / 1000
        speed = self.data["gps_speed"]
        voltage = self.data["jm3_voltage"] / 1000
        time1 = (self.data["Time"] - self.data["Time"][self.start]) * 3600

        plt.figure(figsize=(14, 9))
        plt.title("Various information")
        plt.plot(time1, current, label="Current (A)")
        plt.plot(time1, speed, label="Speed (km/h)")
        plt.plot(time1, voltage, label="Voltage (V)")
        plt.xlabel("Time (s)")
        plt.legend()
        plt.show()

    def efficiency_v_speed(self, samples, start=self.start, stop=self.stop):
        # TODO: correct logical error since speed and efficiency don't have matching time coordinates/pairs hence
        #  weird graph -> actually no
        inst_eff = self.get_inst_efficiency(samples, start, stop)[1]
        speed = self.data["gps_speed"]

        plt.figure(figsize=(14, 9))
        plt.xlabel("Speed")
        plt.ylabel("Efficiency")
        plt.ylim([0, 100])
        plt.plot(speed[0:7319 - 2535], inst_eff[0:7319 - 2535], "o", markersize=2)  # TODO: bounds from where?
        plt.title("Efficiency vs speed")
        plt.show()
        return

    def current_v_speed(self):
        current = self.data['jm3_current'] / 1000
        speed = self.data["gps_speed"]

        plt.plot(speed[0:1149], current[0:1149], "o", markersize=2)
        plt.title("Current vs speed")
        plt.show()
        return

    # TODO: plot acceleration vs speed
