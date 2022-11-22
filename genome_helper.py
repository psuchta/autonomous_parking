from cars.controlled_car import ControlledCar
from binary_converter import BinaryConverter
import numpy as np

class GenomeHelper:
  GENES_PER_NUMBER = BinaryConverter.BITS_COUNT
  EXPONENT_COUNT = BinaryConverter.EXPONENT_COUNT
  SIGNIFICAND_COUNT = BinaryConverter.SIGNIFICAND_COUNT
  BIAS_UNITS = BinaryConverter.BIAS_UNITS

  def __init__(self):
    self.binary_converter = BinaryConverter()

  def genome_to_decimals(self, binary_genome):
    genome_length = len(binary_genome)
    decimals = []

    if genome_length % self.GENES_PER_NUMBER != 0:
      raise Exception("Length of passed genome is not correct")

    for idx in range(0, genome_length, self.GENES_PER_NUMBER):
      binary_part = self.binary_converter.bin_to_int(binary_genome[idx:idx + self.GENES_PER_NUMBER])
      decimals.append(binary_part)

    return decimals

  def init_number_randomly(self, exponent_count=EXPONENT_COUNT, significand_count=SIGNIFICAND_COUNT):
    sign = np.random.randint(2, size=1).tolist()
    exponent = np.random.randint(2, size=exponent_count).tolist()
    # If all numbers in exponent are set to 1, final number will be converted to inifinity
    # Its one of the rule of IEEE 754
    while all(num == 1 for num in exponent):
      exponent = np.random.randint(2, size=exponent_count).tolist()
    significand = np.random.randint(2, size=significand_count).tolist()
    return sign + exponent + significand

  def init_u2_number_randomly(self, exponent_count=EXPONENT_COUNT, significand_count=SIGNIFICAND_COUNT):
    return np.random.randint(2, size=self.GENES_PER_NUMBER).tolist()

  def init_randomly(self, numbers_per_genome):
    binary_genome = []
    for _ in range(numbers_per_genome):
      binary_genome.extend(self.init_u2_number_randomly())
    return binary_genome

  # If number's exponent part contains only 1s, it means the number is Nan or Infinity
  def check_if_number_forbidden(self, binary_number):
    return False

  def check_if_any_number_forbidden(self, binary_genome):
    return False
