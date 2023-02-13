import keyboard
from os import system

screen = list() #y and x

def printAsScreen(s):
    for i in s:
        for c in i:
            print(c, end='')
        print()

if __name__ == '__main__':
    player_x = 0
    player_y = 0
    while True:
        real_x = player_x
        real_y = -player_y
        for y in range(5):
            screen.append([])
            for x in list(' ' * 10):
                screen[y].append(x)
        screen[real_y][real_x] = '@'
        system('cls')
        printAsScreen(screen)
        screen = []

        # Wait for the next event.
        event = keyboard.read_event()

        if event.event_type == keyboard.KEY_DOWN and event.name == 'up':
            player_y = player_y + 1
        if event.event_type == keyboard.KEY_DOWN and event.name == 'right':
            player_x = player_x + 1
        if event.event_type == keyboard.KEY_DOWN and event.name == 'down':
            player_y = player_y - 1
        if event.event_type == keyboard.KEY_DOWN and event.name == 'left':
            player_x = player_x - 1


