import pygame
from driver import Driver


def main():
    pygame.init()
    pygame.display.set_mode((933, 700))
    pygame.display.set_caption("Karaoka")

    app = Driver()
    app.main()


if __name__ == "__main__":
    main()
