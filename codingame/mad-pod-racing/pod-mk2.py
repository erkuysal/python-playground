import sys
import math
import random

# Define constants
# ------------------ Adjustables -------------------
MAX_ACCELERATION = 10
MAX_DECELERATION = 100
MIN_SPEED = 0.1
MAX_SPEED = 100
TARGET_ANGLE_THRESHOLD = 45  # Threshold to consider alignment with the target
COLLISION_THRESHOLD = 400
DESIRED_DISTANCE_TO_CHECKPOINT = 500
CHECKPOINT_RADIUS = 600


# ---------------------------------------------------

# ---------------------------------- CALCULATOR ------------------------------------------------------
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_angle(x, y):
    # Calculate the angle in radians
    angle_rad = math.atan2(y, x)

    # Convert the angle to degrees
    angle_deg = math.degrees(angle_rad)

    # Ensure the angle is in the range [0, 360)
    angle_deg = (angle_deg + 360) % 360

    return angle_deg


def calculate_angle_difference(current_angle, target_angle):
    angle_difference = target_angle - current_angle
    return (angle_difference + 180) % 360 - 180  # Ensure angle difference is in the range [-180, 180]


def calculate_opponent_speed(prev_opponent_x, prev_opponent_y, current_opponent_x, current_opponent_y):
    distance_traveled = calculate_distance(prev_opponent_x, prev_opponent_y, current_opponent_x, current_opponent_y)
    return distance_traveled


# ---------------------------------- /CALCULATOR ------------------------------------------------------
def navigate_through_checkpoint(x, y, checkpoint_x, checkpoint_y, checkpoint_radius):
    angle_to_checkpoint = math.atan2(checkpoint_y - y, checkpoint_x - x)
    target_x = checkpoint_x - checkpoint_radius * math.cos(angle_to_checkpoint)
    target_y = checkpoint_y - checkpoint_radius * math.sin(angle_to_checkpoint)
    return target_x, target_y


# Function to control acceleration and deceleration based on angle alignment
def control_unit(current_angle, target_angle, current_speed):
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

    new_speed = max(MIN_SPEED, min(round(new_speed), MAX_SPEED))

    return new_speed


def calculate_thrust(current_distance, desired_distance):
    thrust = MAX_SPEED  # Default to maximum thrust

    # Adjust thrust based on the desired distance to checkpoint
    if current_distance > desired_distance:
        thrust = int(MAX_SPEED * (desired_distance / current_distance))

    # Ensure thrust is within bounds
    return max(MIN_SPEED, min(thrust, MAX_SPEED))


def dynamic_speed_adjustment(current_speed, distance_to_opponent):
    # Decrease speed when close to the opponent, increase otherwise
    if distance_to_opponent < 100:  # Adjust
        new_speed = max(MIN_SPEED, current_speed - 50)
    else:
        new_speed = min(MAX_SPEED, current_speed + 10)
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
    angle_diff = calculate_angle_difference(next_checkpoint_angle, current_angle)
    # VALUE TASK INSTRUCTION : if angle diff is greater than 10 degrees, then slow down and correct

    current_speed = MAX_SPEED
    dynamic_thrust = control_unit(current_angle, next_checkpoint_angle, current_speed)
    target_x, target_y = navigate_through_checkpoint(x, y, next_checkpoint_x, next_checkpoint_y, CHECKPOINT_RADIUS)
    # VALUE TASK INSTRUCTION : slow down if next checkpoint is close

    distance_to_opponent = calculate_distance(x, y, opponent_x, opponent_y)
    # VALUE TASK INSTRUCTION : Avoid collisions

    # Slow down and correct if the angle difference is too large
    if abs(angle_diff) > 10:
        dynamic_thrust = control_unit(current_angle, next_checkpoint_angle, current_speed)
    else:
        dynamic_thrust = MAX_ACCELERATION

    # Adjust speed for close checkpoints
    if next_checkpoint_dist < 200:
        dynamic_thrust = MIN_SPEED

    # Avoid collisions
    distance_to_opponent = calculate_distance(x, y, opponent_x, opponent_y)
    if distance_to_opponent < COLLISION_THRESHOLD:
        dynamic_thrust = dynamic_speed_adjustment(current_speed, distance_to_opponent)

    # Calculate target position inside checkpoint radius
    target_x, target_y = navigate_through_checkpoint(x, y, next_checkpoint_x, next_checkpoint_y, CHECKPOINT_RADIUS)

    # Update speed based on dynamic thrust
    new_speed = int(control_unit(current_angle, next_checkpoint_angle, current_speed))

    # Write an action using print
    print(str(next_checkpoint_x) + " " + str(next_checkpoint_y) + " " + str(new_speed))
#   print("Debug messages...", file=sys.stderr, flush=True)