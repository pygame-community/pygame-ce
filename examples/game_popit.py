"""
PopIt

About
A beginner pygame example about clicking on balls.

Features
* No external resources
    Makes it easy to share and copy/paste.
* Lots of comments
    The beginner can read every step in detail.
* Game in a class
    The main game is contained inside a class.
* Frame independent movement
    Balls moves the same speed at different frame rates.
* Hit detection
    Click on balls to "destroy" them.
* Random colors
    The color of the balls are set with random RGB-values.
* Random movement
    Balls moves at random speed towards a random target.
* Random placement
    Place ball at random position inside a specific area.
* Object pooling
    Balls are not repeatedly created and destroyed but reset.
    
Features that can be added as practice
* Move the Ball-class to another file.
* Add sine-movement to the ball.
"""

# The randrange-module is needed for random-functions.
from random import randrange

# The pygame-package is the reason we are here.
import pygame


class Ball:
    """A colored ball that moves towards a target."""

    def __init__(self) -> None:
        """Setup the ball-object and finish with a reset."""
        # The ball variables. Color, radius, speed, etc.
        self.screen = pygame.display.get_surface()
        """A reference to the display-surface."""
        self.color = (0, 0, 0)
        """The color of the ball."""
        self.radius = 0
        """The radius of the ball."""
        self.speed = 0
        """The speed the ball moves towards the target."""
        self.target = pygame.Vector2()
        """The position of the target."""
        self.position = pygame.Vector2()
        """The position of the ball."""

        # Time to reset all the variables.
        self.reset()

    def reset(self):
        """Reset everything. Position, color, etc."""
        self.reset_color()
        self.reset_radius()
        self.reset_speed()
        self.reset_target()
        self.reset_position()

    def reset_color(self):
        """Reset the color to a random color."""
        # Randomize red, green and blue.
        r = randrange(0, 255)
        g = randrange(0, 255)
        b = randrange(0, 255)

        # Set the color with the randomized values.
        self.color = pygame.Color(r, g, b)

    def reset_radius(self):
        """Reset 'radius' to random value within a set range."""
        self.radius = randrange(16, 32)

    def reset_target(self):
        """Reset 'target' to random value within a set range."""
        # Calculate x.
        x_min = self.radius
        x_max = self.screen.get_width() - self.radius
        # Pick a random value within set range.
        x = randrange(x_min, x_max)

        # Calculate y.
        # Place it over the screen-surface top.
        y = -self.radius

        # Set target's new position.
        self.target.x = x
        self.target.y = y

    def reset_speed(self):
        """Reset 'speed' to random value within a set range."""
        self.speed = randrange(20, 40)

    def reset_position(self):
        """Reset 'position' to random value within a set range."""
        # Calculate x.
        # Place it inside the screen-surface width.
        x_min = self.radius
        x_max = self.screen.get_width() - self.radius
        # Pick a random value within set range.
        x = randrange(x_min, x_max)

        # Calculate y.
        # Place it under the screen-surface bottom.
        y = self.screen.get_height() + self.radius

        # Set position with new values.
        self.position.x = x
        self.position.y = y

    def update(self, dt):
        """Update ball with the delta time value."""
        # Move the ball towards target. Does not overshoot.
        # The speed is multiplied with delta time to achieve
        # frame independent movement speed.
        self.position.move_towards_ip(self.target, self.speed * dt)

        # Check if the ball has reached the target.
        if self.position == self.target:
            # If the target is reached the ball is reset.
            self.reset()

    def is_over(self, position):
        """Return True if position is over the ball-object."""
        # Because the ball is circle, the hit detection is done with
        # a distance check.
        if self.position.distance_to(position) < self.radius:
            return True

        return False

    def blit(self):
        """Blit(draw) a circle on the screen-surface."""
        pygame.draw.circle(self.screen, self.color, self.position, self.radius)


class Game:
    """The game-class. Object's and logic is in here."""

    def __init__(self) -> None:
        # Pygame needs to init() before it will work.
        pygame.init()

        # Game variables.
        self.clock = pygame.Clock()
        """Keep track of time."""
        self.size = (640, 480)
        """Display size."""
        self.caption = "PopIt"
        """Name of the game."""
        self.frame_rate = 30
        """Desiered frame rate for the game."""
        self.num_balls = 10
        """Number of balls in the game."""
        self.color_background = "cadetblue"
        """The color used to fill the background."""
        self.dt = 1
        """Delta time is used to achieve frame rate independence."""
        self.screen = pygame.display.set_mode(self.size)
        """The screen-surface that is used for drawing."""

        # Set the caption for the game.
        pygame.display.set_caption(self.caption)

        self.balls = [Ball() for i in range(self.num_balls)]
        """Balls in the game."""

        self.running = True
        """Is the game running?"""

        # Time to run the game.
        self.run()

    def input(self):
        """Handle events and inputs."""
        for event in pygame.event.get():
            # If pygame calls it a quit the game-loop stops.
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Order needs to be reversed for depth sorting.
                # Starts with the ball closet to the player.
                for b in reversed(self.balls):
                    # Check if mouse is clicked on a ball.
                    if b.is_over(pygame.mouse.get_pos()):
                        # If a ball is clicked reset the ball.
                        b.reset()
                        # One click = one ball. Break the loop.
                        break

    def run(self):
        """Main game-loop. This is where the game runs."""
        while self.running:
            # Check for input and events.
            self.input()

            # Update all the balls.
            for b in self.balls:
                b.update(self.dt)

            # Fill the screen-surface with the background-color.
            self.screen.fill(self.color_background)

            # Blit all the balls on screen-surface.
            for b in self.balls:
                b.blit()

            # Display the balls on a solid background-color.
            pygame.display.flip()

            # Control the frame rate with pygame.
            self.dt = self.clock.tick(self.frame_rate) / 1000

        # Tell pygame it is time to quit.
        pygame.quit()


# Run the game when script is executed.
if __name__ == "__main__":
    print("Start the game.")

    # The variable 'game' is set and everything happens after.
    game = Game()

    print("Game over.")
