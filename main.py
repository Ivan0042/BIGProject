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
    pts = ''
    params = {"ll": ",".join([lon, lat]),
              "z": delta,
              "l": mode,
              'pt': pts}
    response = requests.get("http://static-maps.yandex.ru/1.x/", params=params)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    
    pygame.init()
    
    font = pygame.font.Font(None, 30)
    text = font.render("Схема", True, 'black')
    s_t = ''
    search_text = font.render(s_t, True, 'black')
    
    map_sprites = pygame.sprite.Group()
    Map(pygame.image.load(map_file), map_sprites)
    
    screen = pygame.display.set_mode((600, 480))
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] < 150 and event.pos[1] > 450:
                    if mode == 'map':
                        mode = 'sat'
                        text = font.render("Спутник", True, 'black')
                    elif mode == 'sat':
                        mode = 'sat,skl'
                        text = font.render("Гибрид", True, 'black')
                    else:
                        mode = 'map'
                        text = font.render("Схема", True, 'black')
                elif event.pos[0] > 570 and event.pos[1] > 450:
                    par = {'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                           'geocode': s_t,
                           'format': 'json'}
                    pos = requests.get("http://geocode-maps.yandex.ru/1.x/", params=par)
                    pos = pos.json()["response"]["GeoObjectCollection"]["featureMember"]
                    if len(pos) > 0:
                        pos = pos[0]["GeoObject"]["Point"]["pos"]
                    lon, lat = tuple(pos.split())
                    pts = lon + ',' + lat
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEDOWN:
                    if float(delta) + 1 <= 17:
                        delta = str(int(delta) + 1)
                elif event.key == pygame.K_PAGEUP:
                    if float(delta) - 1 >= 0:
                        delta = str(int(delta) - 1)
                elif event.key == pygame.K_RIGHT:
                    lon = str(float(lon) + 15)
                    if float(lon) > 180:
                        lon = '-180.0'
                elif event.key == pygame.K_LEFT:
                    lon = str(float(lon) - 15)
                    if float(lon) < -180:
                        lon = '180.0'            
                elif event.key == pygame.K_DOWN:
                    lat = str(float(lat) - 15)
                    if float(lat) < -90:
                        lat = '85.0'            
                elif event.key == pygame.K_UP:
                    lat = str(float(lat) + 15)
                    if float(lat) > 90:
                        lat = '-85.0'
                elif event.key == pygame.K_BACKSPACE:
                    s_t = s_t[:-1]
                else:
                    s_t += event.unicode
                search_text = font.render(s_t, True, 'black')
            
        clock.tick(120)
        params = {"ll": ",".join([lon, lat]),
                  "z": delta,
                  "l": mode,
                  'pt': pts}
        screen.fill((255, 255, 255))
        map_sprites.update(params)        
        map_sprites.draw(screen)
        pygame.draw.rect(screen, 'black', (0, 450, 150, 30), 1)
        pygame.draw.rect(screen, 'black', (570, 450, 30, 30), 1)
        pygame.draw.lines(screen, 'black', True, ((575, 475), (585, 465)), 2)
        pygame.draw.circle(screen, 'black', (590, 460), 7, 2)
        pygame.draw.rect(screen, 'black', (150, 450, 420, 30), 1)
        screen.blit(text, (30, 455))
        screen.blit(search_text, (155, 455))
        pygame.display.flip()
        
    pygame.quit()
    os.remove(map_file)
