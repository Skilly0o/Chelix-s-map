import sys
import pygame
import requests
from io import BytesIO
from string import ascii_letters

# Инициализация Pygame
pygame.init()
# Константы
API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'
WIDTH, HEIGHT = 600, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT + 80))

font = pygame.font.Font(None, 30)

map_button = pygame.Rect(150, 3, 100, 24)
pygame.draw.rect(screen, (0, 255, 0), map_button)
map_text = font.render("Схема", True, (255, 255, 255))
screen.blit(map_text, (map_button.x + 20, map_button.y + 3))

sat_button = pygame.Rect(300, 3, 100, 24)
pygame.draw.rect(screen, (0, 0, 255), sat_button)
sat_text = font.render("Спутник", True, (255, 255, 255))
screen.blit(sat_text, (sat_button.x + 12, sat_button.y + 3))

skl_button = pygame.Rect(450, 3, 100, 24)
pygame.draw.rect(screen, (255, 0, 0), skl_button)
skl_text = font.render("Гибрид", True, (255, 255, 255))
screen.blit(skl_text, (skl_button.x + 15, skl_button.y + 3))

text = font.render("Вид карты", True, (255, 255, 255))
screen.blit(text, (0, 5))

input_fon = pygame.Rect(0, 480, 600, 50)
pygame.draw.rect(screen, (255, 255, 255), input_fon)

input_box = pygame.Rect(10, 490, 490, 30)
pygame.draw.rect(screen, (0, 0, 0), input_box, 1)

search_button = pygame.Rect(510, 490, 80, 30)
pygame.draw.rect(screen, (199, 208, 204), search_button)
input_label = font.render('Искать', True, (0, 0, 0))
screen.blit(input_label, (515, 495))
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
        self.L = 'map'
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
            'l': self.L
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

    def change_input_text(self, text=""):
        input_box = pygame.Rect(10, 490, 490, 30)
        pygame.draw.rect(screen, (255, 255, 255), input_box)
        pygame.draw.rect(screen, (0, 0, 0), input_box, 1)
        input_text = font.render(text, True, (0, 0, 0))
        screen.blit(input_text, (20, 495))

    def get_toponym_coords(self, toponym_to_find):
        request = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            'apikey': API_KEY,
            'geocode': toponym_to_find
        }
        response = requests.get(request, params=params)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        # шаблон для переменной coords
        coords = f'{str(self.x)},{str(self.y)}'
        self.load_map(coords, self.zoom)


def main():
    yandex_api = Yandex_API()
    input_text = ""
    search_flag = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if map_button.collidepoint(mouse_pos):
                    yandex_api.L = "map"
                    search_flag = False
                elif sat_button.collidepoint(mouse_pos):
                    yandex_api.L = "sat"
                    search_flag = False
                elif skl_button.collidepoint(mouse_pos):
                    yandex_api.L = "skl"
                    search_flag = False
                elif input_box.collidepoint(mouse_pos):
                    search_flag = True
                elif search_button.collidepoint(mouse_pos):
                    yandex_api.get_toponym_coords(input_text)
                    search_flag = False
                    input_text = ""
                    yandex_api.change_input_text()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    if yandex_api.zoom < 20:
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
                if event.key == pygame.K_CAPSLOCK:
                    upper = not upper
                elif search_flag:
                    key = pygame.key.name(event.key)
                    input_text += key
                    yandex_api.change_input_text(input_text)

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

        if yandex_api.L == "skl":
            yandex_api.L = "sat"
            coords = f'{str(yandex_api.x)},{str(yandex_api.y)}'
            map_data = yandex_api.load_map(coords, yandex_api.zoom)
            map_image = pygame.image.load_extended(BytesIO(map_data))
            screen.blit(map_image, (0, 30))
            yandex_api.L = "skl"
            coords = f'{str(yandex_api.x)},{str(yandex_api.y)}'
            map_data = yandex_api.load_map(coords, yandex_api.zoom)
            map_image = pygame.image.load_extended(BytesIO(map_data))
            screen.blit(map_image, (0, 30))
        else:
            coords = f'{str(yandex_api.x)},{str(yandex_api.y)}'
            map_data = yandex_api.load_map(coords, yandex_api.zoom)
            map_image = pygame.image.load_extended(BytesIO(map_data))
            screen.blit(map_image, (0, 30))
        pygame.display.flip()


if __name__ == "__main__":
    main()
