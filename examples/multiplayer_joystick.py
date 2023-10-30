import sys
import pygame


def connect_joystick(index):
    if len(active_players) < len(players):
        joy = pygame.Joystick(index)
        index = players.index(None)
        # player data
        players[index] = {
            "joy": joy,
            "pos": [WIDTH * 0.25 + index * 64, 128],
            "surf_idx": index,
            "surf": colors[index],
            "joined": False,
        }
        active_players[joy.get_instance_id()] = index
        print(f"P{index + 1} Connected")


def disconnect_joystick(instance_id: int):
    index = active_players[instance_id]
    players[index] = None
    del active_players[instance_id]
    print(f"P{index + 1} Disconnected")


def control_player(player):  # move player
    joy = player["joy"]
    if not player["joined"]:
        return
    player["pos"][0] += joy.get_axis(0) * 5
    player["pos"][1] += joy.get_axis(1) * 5


def create_surf(size, color):
    surf = pygame.Surface(size)
    surf.fill(color)
    return surf


pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Joystick example")
clock = pygame.Clock()
font_b = pygame.font.SysFont(None, 25)
font_a = pygame.font.SysFont(None, 16)

players = [None, None]  # two players limit
active_players = {}

colors = [
    create_surf((32, 32), (220, 180, 10)),
    create_surf((32, 32), (60, 230, 170)),
    create_surf((32, 32), (230, 20, 70)),
    create_surf((32, 32), (20, 170, 230)),
]
are_no_controllers_connected = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.JOYDEVICEADDED:
            if len(active_players) < len(players):
                # connect controller
                connect_joystick(event.device_index)
                are_no_controllers_connected = False
        elif event.type == pygame.JOYDEVICEREMOVED:
            # disconnect controller
            if event.instance_id in active_players:
                disconnect_joystick(event.instance_id)
                # check if there is at leat one controller connected
                are_no_controllers_connected = True
                for player in players:
                    if player:
                        are_no_controllers_connected = False
                        break
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.instance_id in active_players:
                # join player
                if event.button == 0:
                    index = active_players[event.instance_id]
                    players[index]["joined"] = True
                    print(f"P{index + 1} joined")
                # leave player
                if event.button == 1:
                    index = active_players[event.instance_id]
                    if players[index]["joined"]:
                        players[index]["joined"] = False
                        players[index]["pos"] = [WIDTH * 0.25 + index * 64, 128]
                        print(f"P{index + 1} leave")
        elif event.type == pygame.JOYAXISMOTION:
            if event.instance_id in active_players:
                # change the color if player still hasn't joined
                if event.axis == 0:
                    index = active_players[event.instance_id]
                    player = players[index]
                    if not player["joined"]:
                        if event.value >= 1.0:
                            player["surf_idx"] += 1
                        elif event.value <= -1.0:
                            player["surf_idx"] -= 1
                        player["surf_idx"] = player["surf_idx"] % len(colors)
                        player["surf"] = colors[player["surf_idx"]]

    screen.fill((30, 30, 30))
    pygame.draw.line(screen, (230, 230, 230), (0, 96), (WIDTH, 96), 2)

    # update and draw players
    for player in players:
        if player:
            control_player(player)
            screen.blit(player["surf"], player["pos"])

    # draw available colors
    for i, surf in enumerate(colors):
        screen.blit(surf, (WIDTH * 0.25 + i * 64, 32))

    # show message for connecting a controller
    if are_no_controllers_connected:
        screen.blit(
            font_b.render(
                "Please connect a controller.", True, (230, 230, 230), None, 500 - 20
            ),
            (WIDTH * 0.3, HEIGHT * 0.5),
        )

    screen.blit(
        font_a.render(
            "A: join    B: leave    Joystick: move / change color",
            True,
            (230, 230, 230),
            None,
            WIDTH - 20,
        ),
        (10, HEIGHT - 20),
    )

    clock.tick(60)
    pygame.display.update()
