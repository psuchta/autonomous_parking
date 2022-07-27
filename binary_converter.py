import struct
import numpy as np

class BinaryConverter:
  BITS_COUNT = 16
  BIAS_UNITS = 1

  def float_to_bin(self, num):
    return bin(np.float16(num).view('H'))[2:].zfill(16)

  def bin_to_float(self, binary):
    y = struct.pack("H",int(binary,2))
    return np.frombuffer(y, dtype =np.float16)[0]
