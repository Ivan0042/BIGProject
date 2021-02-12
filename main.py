import os
import pygame
import requests

class Map(pygame.sprite.Sprite):
    def __init__(self, img, group):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(group)
        self.image = img
        self.rect = self.image.get_rect()
        
    def update(self, params):
        pygame.init()
        response = requests.get("http://static-maps.yandex.ru/1.x/", params=params)
        with open(map_file, "wb") as file:
            file.write(response.content)
        self.image = pygame.image.load(map_file)
        self.rect = self.image.get_rect()


if __name__ == '__main__':
    lon = '0'
    lat = '0'
    delta = '1'
    mode = 'map'
    params = {"ll": ",".join([lon, lat]),
              "z": delta,
              "l": mode}
    response = requests.get("http://static-maps.yandex.ru/1.x/", params=params)
    
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    
    pygame.init()
    map_sprites = pygame.sprite.Group()
    Map(pygame.image.load(map_file), map_sprites)
    screen = pygame.display.set_mode((600, 450))
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_PAGEUP]:
            if float(delta) + 1 <= 17:
                delta = str(int(delta) + 1)
        if keys[pygame.K_PAGEDOWN]:
            if float(delta) - 1 >= 0:
                delta = str(int(delta) - 1)
        if keys[pygame.K_RIGHT]:
            lon = str(float(lon) + 5)
            if float(lon) > 180:
                lon = '-180'
        if keys[pygame.K_LEFT]:
            lon = str(float(lon) - 5)
            if float(lon) < -180:
                lon = '180'            
        if keys[pygame.K_DOWN]:
            lat = str(float(lat) - 1)
            if float(lat) <= -90:
                lat = '89.9'            
        if keys[pygame.K_UP]:
            lat = str(float(lat) + 1)
            if float(lat) >= 90:
                lat = '-89.9'
            
        params = {"ll": ",".join([lon, lat]),
                  "z": delta,
                  "l": "map"}
        screen.fill((255, 255, 255))
        map_sprites.update(params)        
        map_sprites.draw(screen)
        clock.tick(120)
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)