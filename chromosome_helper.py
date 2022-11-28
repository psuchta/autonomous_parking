from cars.controlled_car import ControlledCar
from binary_converter import BinaryConverter
from genetic.settings import settings
import numpy as np

class ChromosomeHelper:
  def __init__(self):
    self.binary_converter = BinaryConverter()
    self.bits_per_number = settings['binary_number_bits']
    self.chromosome_type_options = settings['chromosome_representation_options']
    self.set_chromosome_type(settings['chromosome_representation'])

  def set_chromosome_type(self, type):
    if type not in self.chromosome_type_options: raise Exception("Unknown chromosome type")
    self.chromosome_type = type

  def genome_to_decimals(self, chromosome):
    if self.chromosome_type == 'real':
      return chromosome

    chromosome_length = len(chromosome)
    decimals = []

    if chromosome_length % self.bits_per_number != 0:
      raise Exception("Length of passed chromosome is not correct")

    for idx in range(0, chromosome_length, self.bits_per_number):
      binary_part = self.binary_converter.bin_to_int(chromosome[idx:idx + self.bits_per_number])
      decimals.append(binary_part)

    return decimals

  def init_binary_number_randomly(self):
    return np.random.randint(2, size=self.bits_per_number).tolist()

  def init_real_number_randomly(self):
    return np.random.randint(10)

  def init_randomly(self, numbers_to_generate):
    chromosome = []
    random_number_func = None
    if self.chromosome_type == 'binary':
      random_number_func = self.init_binary_number_randomly
    else:
      random_number_func = self.init_real_number_randomly


    for _ in range(numbers_to_generate):
      chromosome.extend(random_number_func())
    return chromosome
