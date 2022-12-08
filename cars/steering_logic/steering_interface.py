class SteeringInterface:
  def set_neural_weights(self, weights):
    pass

  def convert_to_movment_signal(self, sigmoid_value, margin = 0.4):
    if sigmoid_value > (0.9):
      return 1
    else:
      return 0

  def map_steering(self, outputs):
    up = outputs[0]
    down = outputs[1]
    left = outputs[2]
    right = outputs[3]

    steering_dict = {
      'up': False,
      'down': False,
      'brake': False,
      'right': False,
      'left': False
    }

    if up == 1:
      steering_dict['up'] = True
    if down == 1:
      steering_dict['down'] = True

    if left == 1:
      steering_dict['left'] = True
    if right == 1:
      steering_dict['right'] = True
    return steering_dict


  def get_steering_dict(self, sensors_input):
    pass

