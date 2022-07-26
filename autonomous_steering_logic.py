import math
from functools import reduce
import struct
import numpy as np

class AutonomousSteeringLogic:

  def __init__(self):
    self.binary_converter = BinaryConverter()

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