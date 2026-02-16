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
        #start game
        if controller.request_start:
            controller.start()
            controller.request_start = False
        #wipe database
        if controller.request_wipe:
            controller.request_wipe = False
            controller.end()
            model.wipe_all()

        pygame.display.flip()
        clock.tick(25)
    
    pygame.quit()

if __name__ == "__main__":
    main()
