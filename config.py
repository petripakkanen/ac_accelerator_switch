# some MPU6050 Registers and their Address
# https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47
ACCEL_CONFIG = 0x1C
DEVICE_ADDRESS = 0x68  # MPU6050 device address
DATA_SAVE_PATH = "/mnt/common/accsw/data/"
OCTAVE_TCP_IP = "192.168.0.20"
OCTAVE_TCP_PORT = 12345
BUFFER_SIZE = 512
NUM_OF_SAMPLES = 128
ACHOST = "192.168.0.20"
ACPORT = 1880
