from dataclasses import dataclass
from typing import List
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


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
    distance = ((speed1 + speed2) / 3.6 / 2) * (t2 - t1).total_seconds() * 3600

    jouleDiff = joule2 - joule1

    return distance / 1000 / ((jouleDiff if jouleDiff != 0 else -1) / 3600000)


@dataclass
class TelemetryDataPoint:
    timestamp: datetime
    speed: float
    current: float
    voltage: float
    rpm: int


@dataclass
class InstantEfficiencyDataPoint:
    timestamp: datetime
    instant_efficiency: float


class TelemetryProcessor:
    def get_inst_efficiency(
        data: List[TelemetryDataPoint], sampleSize: int
    ) -> List[InstantEfficiencyDataPoint]:
        """
        Determines the instantaneous efficiency from the specified data
        :param samples: the number of data samples to be considered as one instant
        :return:
        """

        if len(data) < sampleSize:
            return

        points: list[InstantEfficiencyDataPoint] = []

        for i in range(sampleSize, len(data), sampleSize):
            start = data[i - sampleSize]
            middle = data[i - int(sampleSize / 2)]
            end = data[i]

            points.append(
                InstantEfficiencyDataPoint(
                    timestamp=middle.timestamp,
                    instant_efficiency=inst_efficiency(
                        start.voltage * start.current,
                        start.speed,
                        end.voltage * end.current,
                        end.speed,
                        start.timestamp,
                        end.timestamp,
                    ),
                )
            )

        return points


#     def efficiency_v_speed(self, samples, start=self.start, stop=self.stop):
#         # TODO: correct logical error since speed and efficiency don't have matching time coordinates/pairs hence
#         #  weird graph -> actually no
#         inst_eff = self.get_inst_efficiency(samples, start, stop)[1]
#         speed = self.data["gps_speed"]

#         plt.figure(figsize=(14, 9))
#         plt.xlabel("Speed")
#         plt.ylabel("Efficiency")
#         plt.ylim([0, 100])
#         plt.plot(
#             speed[0 : 7319 - 2535], inst_eff[0 : 7319 - 2535], "o", markersize=2
#         )  # TODO: bounds from where?
#         plt.title("Efficiency vs speed")
#         plt.show()
#         return

#     def current_v_speed(self):
#         current = self.data["jm3_current"] / 1000
#         speed = self.data["gps_speed"]

#         plt.plot(speed[0:1149], current[0:1149], "o", markersize=2)
#         plt.title("Current vs speed")
#         plt.show()
#         return


# class SemTelemetry:
#     def __init__(self, file, start, stop):
#         # TODO: perhaps we can read the file to determine start and stop

#         self.file = file
#         self.start = start
#         self.stop = stop
#         try:
#             self.data = pd.read_csv(file, delimiter=";", index_col=0)
#         except FileNotFoundError:
#             print("File Not Found. Ensure it is in the current directory")

#     # TODO: determine desired functions
#     # TODO: make functions that will execute the desired analysis for given run, optional parameters i.e steps

#     # TODO: separate into their own functions or establish case for each type of graph

#     # TODO: plot acceleration vs speed
