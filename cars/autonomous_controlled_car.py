from cars.controlled_car import ControlledCar

class AutonomousControlledCar(ControlledCar):
  def __init__(self, pos_x, pos_y, screen, game):
    ControlledCar.__init__(self, pos_x, pos_y, screen, game)

  def get_steering_dict(self):
    sensor_input = map(lambda s: s['sensor'].actual_length_in_meter(), self.sensors)

    return super().get_steering_dict()
