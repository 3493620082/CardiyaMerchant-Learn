import pygame

pygame.init()

pygame.display.set_mode((1, 1), pygame.NOFRAME)

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            print(pygame.key.name(event.key))
