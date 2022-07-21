from csv import reader
from world.settings import tile_size
import pygame

def import_csv_map(path):
  map_list = []
  with open(path) as content:
    lvl = reader(content, delimiter = ',')
    for row in lvl:
      map_list.append(row)
    return map_list

def import_cut_graphics(path):
  surface = pygame.image.load(path).convert_alpha()
  tile_num_x = int(surface.get_size()[0] / 64)
  tile_num_y = int(surface.get_size()[1] / 64)

  cut_tiles = []
  for row in range(tile_num_y):
    for col in range(tile_num_x):
      x = col * 64
      y = row * 64
      new_surf = pygame.Surface((64,64),flags = pygame.SRCALPHA)
      new_surf.blit(surface,(0,0),pygame.Rect(x,y,64,64))
      cut_tiles.append(new_surf)

  return cut_tiles
