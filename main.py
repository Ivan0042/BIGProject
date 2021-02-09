import os

import pygame
import requests

api_server = "http://static-maps.yandex.ru/1.x/"

lon = '0'
lat = '0'
delta = '90.0'

params = {"ll": ",".join([lon, lat]),
          "spn": ",".join([delta, delta]),
          "l": "map"}
response = requests.get(api_server, params=params)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if float(delta) < 80:
                    delta = str(float(delta) + 10)
            if event.key == pygame.K_PAGEDOWN:
                if float(delta) > 10:
                    delta = str(float(delta) - 10)
            if event.key == pygame.K_RIGHT:
                lon = str(float(lon) + 3)
            if event.key == pygame.K_LEFT:
                lon = str(float(lon) - 3)
            if event.key == pygame.K_DOWN:
                lat = str(float(lat) - 3)
            if event.key == pygame.K_UP:
                lat = str(float(lat) + 3)
    params = {"ll": ",".join([lon, lat]),
              "spn": ",".join([delta, delta]),
              "l": "map"}
    response = requests.get(api_server, params=params)
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()
os.remove(map_file)