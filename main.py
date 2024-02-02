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
    coords = '37.617635,55.755814'  # Координаты Московского Кремля
    zoom = 14  # Изначальное приближение карты
    map_data = load_map(coords, zoom)
    map_image = pygame.image.load_extended(BytesIO(map_data))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(map_image, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    main()