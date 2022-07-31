import struct
import numpy as np

class BinaryConverter:
  BITS_COUNT = 16
  BIAS_UNITS = 1

  def float_to_bin(self, num):
    binary_string = bin(np.float16(num).view('H'))[2:].zfill(16)
    return self.string_to_int_array(binary_string)

  def bin_to_float(self, binary):
    string_binary = "".join(str(x) for x in binary)
    y = struct.pack("H", int(string_binary, 2))
    return np.frombuffer(y, dtype =np.float16)[0]

  def string_to_int_array(self, binary_string):
    return [int(d) for d in binary_string]
