import math
import numpy as np
from functools import reduce

class AutonomousSteeringLogic:
  def __init__(self):

  def linearPolynomial(self, coefficients, sensors_input):
    if len(coefficients) != (len(sensors_input) + 1):
      raise Exception("Coefficients or sensors_input size is incompatibile")
    
    multiply_result = [x * y for z, y in zip(coefficients, sensors_input)]
    result = sum(mulriply_result) +  coefficients[-1]
    return result

  def convertToMovmentSignal(self, sigmoid_value, margin = 0.4):
    if sigmoid_value > (0.5 + margin):
      return 1
    elif sigmoid_value < (0.5 - margin):
      return 0
    return 0


  def sigmoid(self, x):
    return 1 / (1 + math.e ** -x)
  def 
