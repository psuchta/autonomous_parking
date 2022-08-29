from cars.controlled_car import ControlledCar
from binary_converter import BinaryConverter
import numpy as np

class GenomeHelper:
  GENES_PER_NUMBER = BinaryConverter.BITS_COUNT
  EXPONENT_COUNT = BinaryConverter.EXPONENT_COUNT
  SIGNIFICAND_COUNT = BinaryConverter.SIGNIFICAND_COUNT
  BIAS_UNITS = BinaryConverter.BIAS_UNITS

  NUMBERS_PEER_STEER = ControlledCar.CAR_SENSORS_NUM + BIAS_UNITS
  NUMBERS_PEER_GENOME = NUMBERS_PEER_STEER * 2
  PEER_STEER_GENES = NUMBERS_PEER_STEER * GENES_PER_NUMBER;
  # Genes for engine and wheels
  GENOME_LENGTH = PEER_STEER_GENES * 2

  def __init__(self):
    self.binary_converter = BinaryConverter()

  def genome_to_decimals(self, binary_genome):
    genome_length = len(binary_genome)
    decimals = []

    if genome_length % self.GENES_PER_NUMBER != 0:
      raise Exception("Length of passed genome is not correct")

    for idx in range(0, self.GENOME_LENGTH, self.GENES_PER_NUMBER):
      binary_part = self.binary_converter.bin_to_float(binary_genome[idx:idx + self.GENES_PER_NUMBER])
      decimals.append(binary_part)

    return decimals

  def engine_wheels_signal_from_binary(self, binary_genome):
    genome_numbers = self.genome_to_decimals(binary_genome)
    return self.engine_wheels_signal(genome_numbers)

  def engine_wheels_signal(self, genome_numbers):
    engine_signal = genome_numbers[0 : self.NUMBERS_PEER_STEER]
    wheels_signal = genome_numbers[self.NUMBERS_PEER_STEER : self.NUMBERS_PEER_STEER * 2]
    return engine_signal, wheels_signal

  def init_number_randomly(self, exponent_count=EXPONENT_COUNT, significand_count=SIGNIFICAND_COUNT):
    sign = np.random.randint(2, size=1).tolist()
    exponent = np.random.randint(2, size=exponent_count).tolist()
    # If all numbers in exponent are set to 1, final number will be converted to inifinity
    # Its one of the rule of IEEE 754
    while all(num == 1 for num in exponent):
      exponent = np.random.randint(2, size=exponent_count).tolist()
    significand = np.random.randint(2, size=significand_count).tolist()
    return sign + exponent + significand

  def init_randomly(self, numbers_per_genome=NUMBERS_PEER_GENOME):
    binary_genome = []
    for _ in range(numbers_per_genome):
      binary_genome.extend(self.init_number_randomly())
    return binary_genome

  # If number's exponent part contains only 1s, it means the number is Nan or Infinity
  def check_if_number_forbidden(self, binary_number):
    if len(binary_number) != self.GENES_PER_NUMBER: 
      raise Exception("Binary number has wrong length")

    exponent = binary_number[1:self.EXPONENT_COUNT+1]
    if all(num == 1 for num in exponent):
      return True

    return False

  def check_if_any_number_forbidden(self, binary_genome):
    for idx in range(0, len(binary_genome), self.GENES_PER_NUMBER):
      binary_number = binary_genome[idx:idx+self.GENES_PER_NUMBER]
      if self.check_if_number_forbidden(binary_number):
        return True

    return False



