import pygame

pygame.init()


def indent(text, indentation_level=0):
    return ("    " * indentation_level) + text


def main():
    # Set the size of the screen (width, height), and name the window.
    size = (500, 700)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Joystick example")

    # Used to manage how fast the screen updates.
    clock = pygame.Clock()

    # Get ready to print.
    font = pygame.font.SysFont(None, 25)
    wraplength = size[0] - 20

    # This dict can be left as-is, since pygame-ce will generate a
    # pygame.JOYDEVICEADDED event for every joystick connected
    # at the start of the program.
    joysticks = {}

    done = False
    while not done:
        # Event processing step.
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.

            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
                if event.button == 0:
                    joystick = joysticks[event.instance_id]
                    if joystick.rumble(0, 0.7, 500):
                        print(f"Rumble effect played on joystick {event.instance_id}")

            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connected")

            if event.type == pygame.JOYDEVICEREMOVED:
                if event.instance_id in joysticks:
                    del joysticks[event.instance_id]
                    print(f"Joystick {event.instance_id} disconnected")
                else:
                    print(
                        f"Tried to disconnect Joystick {event.instance_id}, "
                        "but couldn't find it in the joystick list"
                    )

        # Drawing step
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill((255, 255, 255))
        indentation = 0
        lines = []

        # Get count of joysticks.
        joystick_count = pygame.joystick.get_count()
        lines.append(indent(f"Number of joysticks: {joystick_count}", indentation))
        indentation += 1

        # For each joystick:
        for joystick in joysticks.values():
            jid = joystick.get_instance_id()

            lines.append(indent(f"Joystick {jid}", indentation))
            indentation += 1

            # Get the name from the OS for the controller/joystick.
            name = joystick.get_name()
            lines.append(indent(f"Joystick name: {name}", indentation))

            guid = joystick.get_guid()
            lines.append(indent(f"GUID: {guid}", indentation))

            power_level = joystick.get_power_level()
            lines.append(indent(f"Joystick's power level: {power_level}", indentation))

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other. Triggers count as axes.
            axes = joystick.get_numaxes()
            lines.append(indent(f"Number of axes: {axes}", indentation))
            indentation += 1

            for i in range(axes):
                axis = joystick.get_axis(i)
                lines.append(indent(f"Axis {i} value: {axis:>6.3f}", indentation))
            indentation -= 1

            buttons = joystick.get_numbuttons()
            lines.append(indent(f"Number of buttons: {buttons}", indentation))
            indentation += 1

            for i in range(buttons):
                button = joystick.get_button(i)
                lines.append(indent(f"Button {i:>2} value: {button}", indentation))
            indentation -= 1

            hats = joystick.get_numhats()
            lines.append(indent(f"Number of hats: {hats}", indentation))
            indentation += 1

            # Hat position. All or nothing for direction, not a float like
            # get_axis(). Position is a tuple of int values (x, y).
            for i in range(hats):
                hat = joystick.get_hat(i)
                lines.append(indent(f"Hat {i} value: {str(hat)}", indentation))
            indentation -= 2

        # draw the accumulated text
        screen.blit(
            font.render("\n".join(lines), True, "black", "white", wraplength), (10, 10)
        )

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 30 frames per second.
        clock.tick(30)


if __name__ == "__main__":
    main()
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()
