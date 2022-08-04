from cars.controlled_car import ControlledCar

class AutonomousControlledCar(ControlledCar):
  def __init__(self, pos_x, pos_y, screen, game):
    ControlledCar.__init__(self, pos_x, pos_y, screen, game)

  def reset(self, pos_x, pos_y):
    self.init_moving(pos_x, pos_y)
    self.alive = True

  def get_steering_dict(self):
    sensor_input = map(lambda s: s['sensor'].actual_length_in_meter(), self.sensors)

    return super().get_steering_dict()
