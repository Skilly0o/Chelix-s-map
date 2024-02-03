import sys
import pygame
import requests
from io import BytesIO

# Инициализация Pygame
pygame.init()
# Константы
API_KEY = 'a6e1c83e-1309-4086-aea3-902653631436'
WIDTH, HEIGHT = 600, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# шаблон запроса
'''https://static-maps.yandex.ru/v1
  ? apikey=<string>
  & ll=<float,float>
  & [spn=<float>]
  & [bbox=<float,float~float,float>]
  & [z=<integer>]
  & [size=<integer,integer>]
  & [scale=<float>]
  & [pt=<string>]
  & [pl=<string>]
  & [lang=<string>]
'''


class Yandex_API:
    def __init__(self):
        self.x = 37.617635
        self.y = 55.755814
        self.zoom = 14
        self.left = False
        self.right = False
        self.up = False
        self.down = False

    def load_map(self, coords, zoom):
        # Формируем запрос для статической карты
        map_request = f"https://static-maps.yandex.ru/1.x/"
        params = {
            'll': coords,
            'size': ",".join(map(str, [WIDTH, HEIGHT])),
            'z': self.zoom,
            'l': 'map'
        }
        response = requests.get(map_request, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        return response.content

    def move_map(self, side):
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        if side == 'left':
            self.left = True
        elif side == 'right':
            self.right = True
        elif side == "up":
            self.up = True
        else:
            self.down = True

    def stop_map(self, side):
        if side == 'left':
            self.left = False
        elif side == 'right':
            self.right = False
        elif side == "up":
            self.up = False
        else:
            self.down = False


def main():
    yandex_api = Yandex_API()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    if yandex_api.zoom < 21:
                        yandex_api.zoom += 1
                elif event.key == pygame.K_PAGEDOWN:
                    if yandex_api.zoom > 0:
                        yandex_api.zoom -= 1
                if event.key == pygame.K_LEFT:
                    yandex_api.move_map('left')
                elif event.key == pygame.K_RIGHT:
                    yandex_api.move_map('right')
                elif event.key == pygame.K_UP:
                    yandex_api.move_map('up')
                elif event.key == pygame.K_DOWN:
                    yandex_api.move_map('down')
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    yandex_api.stop_map('left')
                elif event.key == pygame.K_RIGHT:
                    yandex_api.stop_map('right')
                elif event.key == pygame.K_UP:
                    yandex_api.stop_map('up')
                elif event.key == pygame.K_DOWN:
                    yandex_api.stop_map('down')
        if yandex_api.left and yandex_api.x > -180:
            yandex_api.x -= 0.002
        if yandex_api.right and yandex_api.x < 180:
            yandex_api.x += 0.002
        if yandex_api.up and yandex_api.y < 85:
            yandex_api.y += 0.002
        if yandex_api.down and yandex_api.y > -85:
            yandex_api.y -= 0.002
        coords = f'{str(yandex_api.x)},{str(yandex_api.y)}'
        map_data = yandex_api.load_map(coords, yandex_api.zoom)
        map_image = pygame.image.load_extended(BytesIO(map_data))
        screen.blit(map_image, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    main()
