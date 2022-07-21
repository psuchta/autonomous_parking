import pygame
from world.settings import tile_size
from world.utils import import_csv_map, import_cut_graphics
from world.tile import Tile, StaticTile
class Level:
  def __init__(self, level_data):
    self.raw_map = import_csv_map(level_data['path'])
    self.level_objects = self.__create_tiles()

  def __create_tiles(self):
    spreadsheet_tiles = import_cut_graphics('assets/Other.png')
    sprites = pygame.sprite.Group()
    for row_index, row in enumerate(self.raw_map):
      for col_index, val in enumerate(row):
        x = col_index * tile_size
        y = row_index * tile_size

        tile_surface = spreadsheet_tiles[int(val)]
        tile_sprite = StaticTile(tile_size, x, y, tile_surface)
        sprites.add(tile_sprite)
    return sprites



