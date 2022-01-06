from config import DATA_SAVE_PATH
import time
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
from config import ACHOST, ACPORT


class AclSignalPoint:
    timestamp_ns = 0
    acc_x = 0.0
    acc_y = 0.0
    acc_z = 0.0
    g_div = 0.0
    trig = {}
    trig["x"] = False
    trig["y"] = False
    trig["z"] = False

    def __init__(self, _ns, _ax, _ay, _az, _g_div=2048.0):
        self.timestamp_ns = _ns
        self.acc_x = _ax / _g_div
        self.acc_y = _ay / _g_div
        self.acc_z = _az / _g_div
        self.g_div = _g_div


class AclSignalGroup:
    avgs = {"acc_x": 0, "acc_y": 0, "acc_z": 0}
    # samplePoints = []
    file_store_path = DATA_SAVE_PATH
    file_store_enabled = False
    calibrated_avg_level = 0.0
    trigger_level_add_to_avg_g = 0.0
    amount_triggered_points = 0

    fft_enabled = True

    acc_fft = 0.0

    send_to_server_enabled = False

    def __init__(self, c=0, t=0.8):
        self.calibrated_avg_level = c
        self.trigger_level_add_to_avg_g = t
        self.samplePoints = []
        self.session = requests.Session()

    def setPath(self, path):
        self.file_store_path = path

    def set_avg_lvl(self, obj):
        self.calibrated_avg_level = obj.avgs["acc_x"]

    def subSampleTimeRange(self, begin, end):
        pass

    def subSampleTimePast(self, begin):
        pass

    def signalSampleToPlotRange(self, path, range_ns, startTime):
        print(
            "Get signal plot:",
            path,
            "frame time:",
            range_ns,
            ",startTime:",
            startTime,
        )
        loop_times = len(self.samplePoints) - 1
        t = []
        index = -1
        for i in range(loop_times):
            if startTime + range_ns <= self.samplePoints[index].timestamp_ns:
                t.append(self.samplePoints[index])
            index -= 1
        if len(t) != 0:
            print("size of t:", len(t))
            return t
        print("return 0")
        return 0

    def signalSampleToPlot(self, path, ns):
        print("Write signal to", path)
        t = []
        time_now_ns = time() * 1000000
        index = -1
        for i in range(len(self.samplePoints) - 1):
            if ns >= time_now_ns - self.samplePoints[index].timestamp_ns:
                t.append(self.samplePoints[index])
            else:
                break
            index -= 1
        self.samplePointsToPlot(path, t)

    def samplePointsToPlot(self, filepath=None):
        if len(self.samplePoints) != 0:
            print(
                "Sample size",
                str(len(self.samplePoints)),
                "type",
                type(self.samplePoints),
            )

            data_xyzfft_axis = [[], [], [], [], [], [], []]
            for i in range(len(self.samplePoints)):
                data_xyzfft_axis[0].append(self.samplePoints[i].timestamp_ns)
                data_xyzfft_axis[1].append(self.samplePoints[i].acc_x)
                data_xyzfft_axis[2].append(self.samplePoints[i].acc_y)
                data_xyzfft_axis[3].append(self.samplePoints[i].acc_z)
                if self.fft_enabled:
                    data_xyzfft_axis[4].append(
                        self.calcFFT(data_xyzfft_axis[1])
                    )
                    data_xyzfft_axis[5].append(
                        self.calcFFT(data_xyzfft_axis[2])
                    )
                    data_xyzfft_axis[6].append(
                        self.calcFFT(data_xyzfft_axis[3])
                    )

            time_now_ns = time.clock_gettime_ns(time.CLOCK_REALTIME)
            if self.file_store_enabled and filepath is not None:
                plt.figure(figsize=(7, 7))
                plt.plot(data_xyzfft_axis[0], data_xyzfft_axis[1], "o-r")
                plt.title(
                    "Acceleration (g) vs Time (ns)\nSamplepoints: \
                    %i\nMIN: %f  MAX: %f\nTriggered points: %i"
                    % (
                        len(data_xyzfft_axis[1]),
                        min(data_xyzfft_axis[1]),
                        max(data_xyzfft_axis[1]),
                        self.calcTrigPoints(self.samplePoints),
                    ),
                    fontsize=11,
                    fontweight="bold",
                )
                plt.xlabel("Time (ms)", fontweight="bold")
                plt.ylabel("Acceleration (g)", fontweight="bold")

                print(
                    "axhline: ",
                    self.calibrated_avg_level
                    + self.trigger_level_add_to_avg_g,
                )
                print(
                    "axhline: ",
                    self.calibrated_avg_level
                    - self.trigger_level_add_to_avg_g,
                )
                plt.axhline(
                    y=self.calibrated_avg_level
                    + self.trigger_level_add_to_avg_g,
                    xmin=0,
                    xmax=self.samplePoints[-1].timestamp_ns,
                )
                plt.axhline(
                    y=self.calibrated_avg_level
                    - self.trigger_level_add_to_avg_g,
                    xmin=0,
                    xmax=self.samplePoints[-1].timestamp_ns,
                )
                plt.savefig(filepath + "@" + str(time_now_ns) + ".png")
                plt.clf()

                if self.fft_enabled:
                    _fft = data_xyzfft_axis[5]
                    plt.plot(_fft, "o-r")
                    plt.title(
                        "FFT\nMax freq.: %f  @index %i"
                        % (max(_fft), np.argmax(_fft)),
                        fontsize=14,
                        fontweight="bold",
                    )
                    plt.xlabel("Frequency (~Hz)", fontweight="bold")
                    plt.ylabel("Acceleration (g)", fontweight="bold")
                    plt.savefig(filepath + "@" + str(time_now_ns) + "_fft.png")

                plt.clf()
                plt.close("all")

            if self.send_to_server_enabled:
                # self.sendToOctave()
                self.sendToACServer()

            del self.samplePoints[:]

    def sendToACServer(self, _url="data"):
        # Form json data str
        a = '{"data":['
        for i in self.samplePoints:
            # a += '{"x":' + str(_i) + ', "y":' + str(i.acc_x) + '},'
            a += f"{i.acc_x: .5f},"
        a = a[:-1]  # remove last ,
        a += "]}"  # close json

        self.session.post(f"http://{ACHOST}:{ACPORT}/{_url}", json.loads(a))

        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #    s.connect((ACHost, ACPort))

        # t = str(asp.timestamp_ns) + "," + str(asp.acc_x)

        #    s.sendall(bytes(a, "utf-8"))

    def addSinglePoint(self, asp, triggered=False):
        if isinstance(asp, AclSignalPoint):
            self.samplePoints.append(asp)
            # return True
            self.calculateOwnAverages()

            # Selects which axis triggers
            # TODO: add multi-axis trigger
            if (
                self.calibrated_avg_level + self.trigger_level_add_to_avg_g
                <= asp.acc_x
            ) or (
                self.calibrated_avg_level - self.trigger_level_add_to_avg_g
                >= asp.acc_x
            ):
                asp.trig["x"] = True
            if (
                self.calibrated_avg_level + self.trigger_level_add_to_avg_g
                <= asp.acc_y
            ) or (
                self.calibrated_avg_level - self.trigger_level_add_to_avg_g
                >= asp.acc_y
            ):
                asp.trig["y"] = True
            if (
                self.calibrated_avg_level + self.trigger_level_add_to_avg_g
                <= asp.acc_z
            ) or (
                self.calibrated_avg_level - self.trigger_level_add_to_avg_g
                >= asp.acc_z
            ):
                asp.trig["z"] = True

            if asp.trig["x"] or asp.trig["y"] or asp.trig["z"]:
                self.amount_triggered_points += 1

            # self.sendToACServer()
        return False

    def calculateSamplePointGroupAccXYZAverages(self, ln):
        sum = [0, 0, 0]
        try:
            for i in ln:
                sum[0] += i.acc_x
                sum[1] += i.acc_y
                sum[2] += i.acc_z
            return {
                "acc_x": sum[0] / len(ln),
                "acc_y": sum[1] / len(ln),
                "acc_z": sum[2] / len(ln),
            }
        except Exception as e:
            print(e)

    def calculateOwnAverages(self):
        self.avgs = self.calculateSamplePointGroupAccXYZAverages(
            self.samplePoints
        )

    def calcTrigPoints(self, arr):
        sum = 0
        if len(arr) > 0:
            for i in arr:
                if i.trig:
                    sum += 1
        return sum

    def calcFFT(self, y, absolute=True):
        _fft = np.fft.fft(y) / len(y)
        if absolute:
            _fft = abs(_fft)
        return _fft

    def signalToPlot(self, path):
        self.samplePointsToPlot(path)


class AclCalibrationGroup(AclSignalGroup):
    minMax = {
        "x": {"min": 1, "max": -1},
        "y": {"min": 1, "max": -1},
        "z": {"min": 1, "max": -1},
    }

    def __init__(self):
        pass

    def addPoint(self, asp):
        if isinstance(asp, AclSignalPoint):
            self.samplePoints.append(asp)
            if asp.acc_x > self.minMax["x"]["max"]:
                self.minMax["x"]["max"] = asp.acc_x
            if asp.acc_x < self.minMax["x"]["min"]:
                self.minMax["x"]["min"] = asp.acc_x
            self.calculateOwnAverages()
