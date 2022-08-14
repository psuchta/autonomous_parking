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

  def get_steering_dict(self, engine_signal, wheels_signal, sensors_input):
    engine_signal = self.linear_polynomial(engine_signal, sensors_input)
    wheels_signal = self.linear_polynomial(wheels_signal, sensors_input)

    normalized_engine = self.sigmoid(engine_signal)
    normalized_wheels = self.sigmoid(wheels_signal)

    engine_run = self.convert_to_movment_signal(normalized_engine)
    wheels_run = self.convert_to_movment_signal(normalized_wheels)
    steering_dict = {
      'up': False,
      'down': False,
      'brake': False,
      'right': False,
      'left': False
    }

    if engine_run == 1:
      steering_dict['up'] = True
    elif engine_run == -1:
      steering_dict['down'] = True

    if wheels_run == 1:
      steering_dict['left'] = True
    elif wheels_run == -1:
      steering_dict['right'] = True
    return steering_dict

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
