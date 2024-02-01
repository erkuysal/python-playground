import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Interactive Angle Calculator")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Function to calculate angle in degrees
def calculate_angle(x, y):
    angle_rad = math.atan2(y, x)
    angle_deg = math.degrees(angle_rad)
    return angle_deg

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Get the coordinates of the mouse click
            click_x, click_y = event.pos

            # Calculate the angle for the clicked point
            rel_x = click_x - width // 2
            rel_y = height // 2 - click_y  # Invert y-coordinate to match the mathematical convention
            angle = calculate_angle(rel_x, rel_y)

            # Display the angle on the console
            print(f"Angle for clicked point: {angle:.2f} degrees")

    # Clear the screen
    screen.fill(white)

    # Draw x-axis
    pygame.draw.line(screen, black, (0, height // 2), (width, height // 2), 2)

    # Draw y-axis
    pygame.draw.line(screen, black, (width // 2, 0), (width // 2, height), 2)

    # Draw grid lines
    for i in range(-5, 6):
        # Vertical lines
        pygame.draw.line(screen, black, (width // 2 + i * (width // 10), 0),
                         (width // 2 + i * (width // 10), height), 1)
        # Horizontal lines
        pygame.draw.line(screen, black, (0, height // 2 + i * (height // 10)),
                         (width, height // 2 + i * (height // 10)), 1)

    # Update the display
    pygame.display.flip()
