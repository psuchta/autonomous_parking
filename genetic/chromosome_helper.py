from cars.controlled_car import ControlledCar
from genetic.binary_converter import BinaryConverter
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
    if self.chromosome_type != 'binary':
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

  def init_int_number_randomly(self):
    return np.random.randint(settings['int_number_range'][0], settings['int_number_range'][1])

  def init_float_number_randomly(self):
    return np.random.uniform(low=settings['float_number_range'][0], high=settings['float_number_range'][1])

  def init_randomly(self, numbers_to_generate):
    chromosome = []
    if self.chromosome_type == 'binary':
      random_number_func = self.init_binary_number_randomly
    elif self.chromosome_type == 'int':
      random_number_func = self.init_int_number_randomly
    elif self.chromosome_type == 'float':
      random_number_func = self.init_float_number_randomly


    for _ in range(numbers_to_generate):
      if self.chromosome_type == 'binary':
        chromosome.extend(random_number_func())
      else:
        chromosome.append(random_number_func())
    return chromosome

  def mutate_number(self, original_number):
    if self.chromosome_type == 'binary':
      return 1 - original_number

    if self.chromosome_type == 'int':
      mutated_number = original_number + self.random_int_mutation()
      return np.clip(mutated_number, settings['int_number_range'][0], settings['int_number_range'][1])

    elif self.chromosome_type == 'float':
      mutated_number = original_number + self.random_mutate_float()
      return np.clip(mutated_number, settings['float_number_range'][0], settings['float_number_range'][1])

  def random_int_mutation(self):
    if settings['mutation_method'] == 'default':
      return np.random.randint(settings['int_number_range'][0], settings['int_number_range'][1])
    elif settings['mutation_method'] == 'gaussian':
      random = np.random.normal()
      if settings['mutation_scale']:
        random *= settings['mutation_scale']
      return random


  def random_mutate_float(self):
    if settings['mutation_method'] == 'default':
      return np.random.uniform(low=settings['float_number_range'][0], high=settings['float_number_range'][1])
    elif settings['mutation_method'] == 'gaussian':
      random = np.random.normal()
      if settings['mutation_scale']:
        random *= settings['mutation_scale']
      return random


