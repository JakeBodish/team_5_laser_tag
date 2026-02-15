import pygame
from controller import Controller
from view import Screen
from model import Model

def main():
    pygame.init()
    view = Screen()
    controller = Controller()
    model = Model()
    clock = pygame.time.Clock()

    while controller.running:
        events = pygame.event.get()
        controller.process_events(events)
        #start game
        if controller.request_start:
            controller.start()
            controller.request_start = False
        #add player
        if controller.request_add:
            controller.request_add = False
            model.add_player(1, "Test", "RED")
            controller.broadcast_equipment(1)
        #wipe database
        if controller.request_wipe:
            controller.request_wipe = False
            controller.end()
            model.wipe_all()

        view.update()
        clock.tick(25)

    pygame.quit()

if __name__ == "__main__":
    main()
