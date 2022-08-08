from cars.controlled_car import ControlledCar
from binary_converter import BinaryConverter
import numpy as np

class GenomeHelper:
  GENES_PER_NUMBER = BinaryConverter.BITS_COUNT
  BIAS_UNITS = BinaryConverter.BIAS_UNITS

  NUMBERS_PEER_STEER = ControlledCar.CAR_SENSORS_NUM + BIAS_UNITS
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

  def engine_wheels_signal(self, binary_genome):
    genome_numbers = self.genome_to_decimals(binary_genome)
    engine_signal = genome_numbers[0 : self.NUMBERS_PEER_STEER]
    wheels_signal = genome_numbers[self.NUMBERS_PEER_STEER : self.NUMBERS_PEER_STEER * 2]
    return engine_signal, wheels_signal

  def init_randomly(self, genome_size=GENOME_LENGTH):
    return np.random.randint(2, size=genome_size).tolist()
