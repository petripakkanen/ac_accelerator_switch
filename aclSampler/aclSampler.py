from time import clock_gettime_ns, CLOCK_REALTIME
import threading
from aclSignal.aclSignal import AclSignalPoint as aclsp
from config import (
    DEVICE_ADDRESS,
    SMPLRT_DIV,
    PWR_MGMT_1,
    CONFIG,
    GYRO_CONFIG,
    INT_ENABLE,
    ACCEL_CONFIG,
    ACCEL_XOUT_H,
    ACCEL_YOUT_H,
    ACCEL_ZOUT_H,
)
import smbus


class aclSampler(threading.Thread):
    def __init__(self, threadID, name, sGroup):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.sGroup = sGroup
        self.bus = smbus.SMBus(1)

        self.MPU_Init()

    def run(self):
        while True:
            self.readSample()

    def readSample(self):
        self.sGroup.addSinglePoint = aclsp(
            clock_gettime_ns(CLOCK_REALTIME),
            self.read_raw_data(ACCEL_XOUT_H),
            self.read_raw_data(ACCEL_YOUT_H),
            self.read_raw_data(ACCEL_ZOUT_H),
        )

    def MPU_Init(self):
        # write to sample rate register
        self.bus.write_byte_data(DEVICE_ADDRESS, SMPLRT_DIV, 7)
        # Write to power management register
        self.bus.write_byte_data(DEVICE_ADDRESS, PWR_MGMT_1, 1)
        # Write to Configuration register
        self.bus.write_byte_data(DEVICE_ADDRESS, CONFIG, 0)
        # Write to Gyro configuration register
        self.bus.write_byte_data(DEVICE_ADDRESS, GYRO_CONFIG, 24)
        # Write to interrupt enable register
        self.bus.write_byte_data(DEVICE_ADDRESS, INT_ENABLE, 1)
        # Write to ACCEL_CONFIG register
        self.bus.write_byte_data(DEVICE_ADDRESS, ACCEL_CONFIG, 0xFF)

    @staticmethod
    def read_raw_data(self, addr):
        # Accelero and Gyro value are 16-bit
        high = self.bus.read_byte_data(DEVICE_ADDRESS, addr)
        low = self.bus.read_byte_data(DEVICE_ADDRESS, addr + 1)
        # concatenate higher and lower value
        value = (high << 8) | low
        # to get signed value from mpu6050
        if value > 32768:
            value = value - 65536
        return value
