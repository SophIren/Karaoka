import pygame
from driver import Controller


def main():
    pygame.init()
    pygame.display.set_caption("Karaoka")

    app = Controller()
    app.main()


if __name__ == "__main__":
    main()
