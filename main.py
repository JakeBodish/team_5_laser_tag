import pygame
from controller import Controller
from View import Screen
from model import Model

def main():
    pygame.init()
    model = Model()
    view = Screen(model)
    controller = Controller(view, model)
    clock = pygame.time.Clock()

    while controller.running:
        view.update()
        events = pygame.event.get()
        controller.process_events(events)
        model.update()
        pygame.display.flip()
        clock.tick(25)
    pygame.quit()

if __name__ == "__main__":
    main()
