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


def load_map(coords, zoom):
    # Формируем запрос для статической карты
    map_request = f"https://static-maps.yandex.ru/v1?apikey={API_KEY}&ll={coords}&size={WIDTH},{HEIGHT}&z={zoom}"
    '"https://static-maps.yandex.ru/1.x/?ll=133.7751,-25.2744&spn=20,20&l=sat"'
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    return response.content


def main():
    x = 37.617635
    y = 55.755814
    zoom = 14  # Изначальное приближение карты

    left = False
    right = False
    up = False
    down = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    if zoom < 21:
                        zoom += 1
                elif event.key == pygame.K_PAGEDOWN:
                    if zoom > 0:
                        zoom -= 1
                if event.key == pygame.K_LEFT:
                    left = True
                elif event.key == pygame.K_RIGHT:
                    right = True
                elif event.key == pygame.K_UP:
                    up = True
                elif event.key == pygame.K_DOWN:
                    down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                elif event.key == pygame.K_RIGHT:
                    right = False
                elif event.key == pygame.K_UP:
                    up = False
                elif event.key == pygame.K_DOWN:
                    down = False
        if left and x > -180:
            x -= 0.002
        if right and x < 180:
            x += 0.002
        if up and y < 85:
            y += 0.002
        if down and y > -85:
            y -= 0.002

        coords = f'{str(x)},{str(y)}'
        map_data = load_map(coords, zoom)
        map_image = pygame.image.load_extended(BytesIO(map_data))

        screen.blit(map_image, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    main()