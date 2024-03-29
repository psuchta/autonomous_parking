import struct
import numpy as np
import math
from genetic.settings import settings

class BinaryConverter:
  def __init__(self):
    self.bits_count = settings['binary_number_bits']

  # Using Two's Complement Numbers/U2 for binary representation
  def int_to_bin(self, num):
    s = bin(num & int("1"*self.bits_count, 2))[2:]
    binary_string =  ("{0:0>%s}" % (self.bits_count)).format(s)
    return self.string_to_int_array(binary_string)

  # Using Two's Complement Numbers/U2 for binary representation
  def bin_to_int(self, binary):
    string_binary = "".join(str(x) for x in binary)
    val = int(string_binary, 2)

    if (val & (1 << (self.bits_count - 1))) != 0:
        val = val - (1 << self.bits_count)
    return val

  # Using IEEE574 for binary representation
  def float_to_bin(self, num):
    binary_string = bin(np.float16(num).view('H'))[2:].zfill(16)
    return self.string_to_int_array(binary_string)

  # Using IEEE574 for binary representation
  def bin_to_float(self, binary):
    string_binary = "".join(str(x) for x in binary)
    y = struct.pack("H", int(string_binary, 2))
    r = np.frombuffer(y, dtype =np.float16)[0]
    if math.isnan(r):
      print(r)
    if r == 0:
      print(r)
      print(binary)
    return r

  def string_to_int_array(self, binary_string):
    return [int(d) for d in binary_string]
