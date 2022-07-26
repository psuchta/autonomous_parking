from car import ControllerCar
from binary_converter import BinaryConverter

class Genome:
  GENES_PER_NUMBER = BinaryConverter.BITS_COUNT
  BIAS_UNITS = BinaryConverter.BIAS_UNITS

  STEER_FORMULA_GENES_NUM = (ControllerCar.CAR_SENSORS_NUM + BIAS_UNITS) * GENES_PER_NUMBER;
  # Genes for engine and wheels
  GENOME_LENGTH = STEER_FORMULA_GENES_NUM * 2

  def __init__(self):
    self.binary_converter = BinaryConverter()

  def binary_to_decimals(self, binary_genome):
    genome_length = len(binary_genome)
    decimals = []

    if genome_length != self.GENOME_LENGTH:
      raise Exception("Length of passed genome is not correct")

    for idx in range(0, self.GENOME_LENGTH, self.GENES_PER_NUMBER):
      binary_part = self.binary_converter.bin_to_float(binary_genome[idx:idx + self.GENES_PER_NUMBER])
      decimals.append(binary_part)

    return decimals






