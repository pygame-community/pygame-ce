import pygame
import sys

pygame.init()

screen = pygame.display.set_mode([500,700])

def indent(text, indentation_level=0):
    return ("    " * indentation_level) + text

joysticks = {}

font = pygame.font.SysFont(None, 25)
wraplength = 480

while True:

    screen.fill("white")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        
        elif event.type == pygame.JOYDEVICEADDED:

            joystick = pygame.Joystick(event.device_index)

            joysticks[joystick.get_instance_id()] = joystick

            print(f"Joystick \"{joystick.get_name()}\" connected")
        
        elif event.type == pygame.JOYDEVICEREMOVED:

            if event.instance_id in joysticks.keys():
                joysticks[joystick.get_instance_id()] = joystick

                print(f"Joystick \"{joystick.get_name()}\" removed")
            
            print(f"Tried to remove device with id : {event.instance_id}, but couldn't find it")
    
    indentation = 0
    lines = []

    # Get count of joysticks.
    joystick_count = pygame.joystick.get_count()
    lines.append(indent("Number of joysticks: {joystick_count}", indentation))
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
    
    pygame.display.flip()