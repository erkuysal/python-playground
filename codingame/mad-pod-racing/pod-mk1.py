import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# Define constants
MAX_ACCELERATION = 10  # Maximum acceleration
MAX_DECELERATION = 100  # Maximum deceleration
TARGET_ANGLE_THRESHOLD = 45  # Threshold to consider alignment with the target
MIN_SPEED = 0.1  # Minimum allowable speed
MAX_SPEED = 100  # Maximum allowable speed


def calculate_angle(x, y):
    # Calculate the angle in radians
    angle_rad = math.atan2(y, x)

    # Convert the angle to degrees
    angle_deg = math.degrees(angle_rad)

    # Ensure the angle is in the range [0, 360)
    angle_deg = (angle_deg + 360) % 360

    return angle_deg


# Function to calculate angle difference between current angle and target angle
def calculate_angle_difference(current_angle, target_angle):
    angle_difference = target_angle - current_angle
    return (angle_difference + 180) % 360 - 180  # Ensure angle difference is in the range [-180, 180]


# Function to control acceleration and deceleration based on angle alignment
def control_algorithm(current_angle, target_angle, current_speed):
    # Calculate angle difference
    angle_difference = calculate_angle_difference(current_angle, target_angle)

    # Check if the object is aligned with the target angle
    if abs(angle_difference) < TARGET_ANGLE_THRESHOLD:
        # Accelerate when aligned with the target angle
        acceleration = MAX_ACCELERATION
    else:
        # Decelerate when making turns to align with the target
        acceleration = -MAX_DECELERATION * (angle_difference / 180.0)

    # Update speed based on acceleration
    new_speed = current_speed + acceleration

    # Ensure speed is within bounds
    new_speed = max(MIN_SPEED, min(new_speed, MAX_SPEED))

    return new_speed


# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in
                                                                                               input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    current_angle = calculate_angle(x, y)

    angle_diff = calculate_angle_difference(current_angle, next_checkpoint_angle)

    dynamic_thrust = int(control_algorithm(current_angle, next_checkpoint_angle, 100))

    if next_checkpoint_angle == 0 and (next_checkpoint_x & next_checkpoint_y) < 50:
        thrust = MAX_SPEED
    else:
        thrust = dynamic_thrust

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # if (opponent_x & opponent_y) and (x & y) < 200:
    #     thrust = 25

    if (opponent_x & opponent_y) < next_checkpoint_x & next_checkpoint_y:
        if next_checkpoint_dist > 4500 and next_checkpoint_angle <= 15:
            thrust = "BOOST"

    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"

    print(str(next_checkpoint_x) + " " + str(next_checkpoint_y) + " " + str(thrust))

