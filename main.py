import pygame
from scripts.driver import Driver


def main():
    pygame.init()
    pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Karaoka")
    icon = pygame.image.load("GUI/icon.png")
    pygame.display.set_icon(icon)

    app = Driver()
    app.main()


if __name__ == "__main__":
    main()
