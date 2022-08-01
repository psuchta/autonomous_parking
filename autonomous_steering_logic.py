import math
from functools import reduce
import struct
import numpy as np
from binary_converter import BinaryConverter
from genome_helper import GenomeHelper
import random

class AutonomousSteeringLogic:

  def __init__(self):
    self.binary_converter = BinaryConverter()
    self.genome_helper = GenomeHelper()

  def linear_polynomial(self, coefficients, sensors_input):
    if len(coefficients) != (len(sensors_input) + 1):
      raise Exception("Coefficients or sensors_input size is incompatibile")
    
    multiply_result = [x * y for x, y in zip(coefficients, sensors_input)]
    result = sum(multiply_result) +  coefficients[-1]
    return result

  def convert_to_movment_signal(self, sigmoid_value, margin = 0.4):
    if sigmoid_value > (0.5 + margin):
      return 1
    elif sigmoid_value < (0.5 - margin):
      return -1
    return 0


  def sigmoid(self, x):
    return 1 / (1 + math.e ** -x)

  def create_generation(self, generation_size, genome_size = GenomeHelper.GENOME_LENGTH):
    return [self.genome_helper.init_randomly(genome_size) for _ in range(generation_size)]

  def mutate_genome(self, binary_genome, probability=0.1):
    for idx, val in enumerate(binary_genome):
      if random.uniform(0, 1) <= probability:
        # change to opposite binary val
        binary_genome[idx] = 1 - val

