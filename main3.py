from pygame.locals import *
import pygame
from PIL import Image

def cyclic_rotation_left(input_str, num_rotations):
    num_rotations = num_rotations % len(input_str)
    return input_str[num_rotations:] + input_str[:num_rotations]


def cyclic_rotation_right(input_str, num_rotations):
    num_rotations = num_rotations % len(input_str)
    return input_str[-num_rotations:] + input_str[:-num_rotations]


word = [str(ord(i)) for i in input('data to generate salt from: ')]

pygame.init()
# scale = random.randint(100,200)
scale = 100
size = width, height = 512, 512
screen = pygame.display.set_mode(size)
xaxis = width / 2
yaxis = height / 2
screen.fill((255, 255, 255))


def mandelbrot(zoom, iterations, scale):
    for iy in range(height):
        for ix in range(width):
            z = 0 + 0j
            c = complex((ix - xaxis) / (scale * zoom), (iy - yaxis) / (scale * zoom))

            for i in range(iterations):
                z = z ** 2 + c
                if abs(z) > 2:
                    v = (1000 * i) / iterations
                    if v > 510:
                        color = (255, 255, v % 255)
                    elif v > 255:
                        color = (255, v % 255, 0)
                    else:
                        color = (v % 255, 0, 0)
                    break
            else:
                color = (0, 0, 0)

            screen.set_at((ix, iy), color)


def julia(x, y, zoom, iterations):
    c = complex(float(x), float(y))
    for iy in range(int(height)):
        for ix in range(int(width)):
            z = complex((ix - xaxis) / (scale * zoom), (iy - yaxis) / (scale * zoom))

            for i in range(iterations):
                z = z ** 2 + c
                if abs(z) > 2:
                    v = (1000 * i) / iterations
                    color = (
                        255 if v > 510 else v % 255,
                        255 if v > 510 else v % 255 if v > 255 else 0,
                        v % 255 if v <= 255 else 0
                    )
                    break
            else:
                color = (0, 0, 0)

            screen.set_at((ix, iy), color)


import sys


def main():
    iterations = 80
    zoom = 2
    j = True
    x = '0.' + cyclic_rotation_right(''.join(word[:len(word) // 2]), 3)
    y = '0.' + cyclic_rotation_left(''.join(word[len(word) // 2:]), 3)

    print(x, y)
    julia(x, y, zoom, iterations)
    pygame.display.update()

    while True:
        global xaxis, yaxis, height, width, scale
        event = pygame.event.poll()

        if event.type == KEYDOWN:
            if event.key == K_j:
                j = True
                julia(zoom, iterations)
            elif event.key == K_m:
                j = False
                mandelbrot(zoom, iterations)
            elif event.key == K_1:
                zoom *= 1.2
            elif event.key == K_2:
                zoom *= 0.8
            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONUP:
            oldzoom = zoom
            pos = pygame.mouse.get_pos()
            posx, posy = pos[0], pos[1]
            xaxis += (posx - width / 2) / 5
            yaxis += (posy - height / 2) / 5
            xaxis = zoom * (posx / width + xaxis) / oldzoom - posx / width
            yaxis = zoom * (posy / height + yaxis) / oldzoom - posy / height

            if j:
                julia(zoom, iterations)
            else:
                mandelbrot(zoom, iterations)
            pygame.display.update()

        def extract_data(image_path):
            image = Image.open(image_path)
            width, height = image.size

            binary_data = ''
            for y in range(height):
                for x in range(width):
                    pixel = image.getpixel((x, y))
                    for i in range(3):
                        binary_data += str(pixel[i] & 1)
            data = ''.join(str(int(binary_data[i:i + 4], 2)) for i in range(0, len(binary_data), 8192))

            return int(data)

        pygame.image.save(screen, 'julia_set_image.png')
        extracted_data = extract_data("julia_set_image.png")

        salt = str(bin(extracted_data))[2:].zfill(512)
        print("Extracted data:", hex(int(salt, 2)))
        print("Extracted data:", salt)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()