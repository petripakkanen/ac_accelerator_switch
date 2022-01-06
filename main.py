from config import DATA_SAVE_PATH, ACCEL_XOUT_H, ACCEL_YOUT_H, ACCEL_ZOUT_H
import time
import os
import errno
from aclSignal.aclSignal import AclSignalPoint as aclsp
from aclSignal.aclSignal import AclSignalGroup as aclsg
from aclSignal.aclSignal import AclCalibrationGroup as aclcg
from aclSampler.aclSampler import aclSampler as acls
from aclSampler.aclSampler import read_raw_data

# from controllers.mped import CmpdPlayer
import threading
from mpd import MPDClient

WAIT_TIME_SECONDS = 1.0
TRIGGER_G_LEVEL_MULTIPLIER = 0.4  # convert m/s2 => 1.2*9.81
NOISE_LEVEL_MULTIPLIER = 0.1

lastActivatedAx = 0
index = 0
triggered = False
triggeredIndex = 0
triggerCounter = 0
triggeredTime = 0
PlotArray = []
fullPlotArray = []
timestampBuffer = []
sampleBufferSize = 2048

triggerStopIndex = 0
saveSample = False
sGroup = aclsg(DATA_SAVE_PATH)

trigger_resolutions_ns = [500000, 1000000, 5000000]
first_trigger = True
ts_store = 0
client = MPDClient()
client.timeout = 10
client.idletimeout = None
start_time = time.clock_gettime_ns(time.CLOCK_REALTIME)
last_sample_time_ns = 0
firstTime = 0
count = 0
lastPrintTime = 0
sampling_frequency = 10  # Hz

d = acls(1, "accelo_00", sGroup)
# d.readSample()
d.start()
lastWriteTime = 0

try:
    os.makedirs(DATA_SAVE_PATH)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise


def calibrate(num_of_samples):
    cal = aclcg()
    for i in range(num_of_samples):
        s = aclsp(
            time.clock_gettime_ns(time.CLOCK_REALTIME),
            read_raw_data(ACCEL_XOUT_H),
            read_raw_data(ACCEL_YOUT_H),
            read_raw_data(ACCEL_ZOUT_H),
        )
        cal.addSinglePoint(s)
        if i % 25 == 0:
            print(".")
    return cal


ticker = threading.Event()
while not ticker.wait(WAIT_TIME_SECONDS):
    pass
    # writeplot(lastWriteTime)
