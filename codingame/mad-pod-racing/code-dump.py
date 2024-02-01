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

# ---------------------------------- CALCULATOR ------------------------------------------------------

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

    new_speed = max(MIN_SPEED, min(round(new_speed), MAX_SPEED))

    return new_speed


def navigate_through_checkpoint(x, y, checkpoint_x, checkpoint_y, checkpoint_radius):
    angle_to_checkpoint = math.atan2(checkpoint_y - y, checkpoint_x - x)
    target_x = checkpoint_x - checkpoint_radius * math.cos(angle_to_checkpoint)
    target_y = checkpoint_y - checkpoint_radius * math.sin(angle_to_checkpoint)
    return target_x, target_y


# ----------------- Collision Handlers -------------------------
def simple_deceleration(current_speed):
    deceleration_rate = 0.2  # Adjust
    new_speed = max(MIN_SPEED, current_speed - deceleration_rate)
    return new_speed


def quick_evasion(current_speed, steering_angle):
    evasion_steering_angle = 30  # Adjust
    new_steering_angle = min(steering_angle + evasion_steering_angle, 90)
    return current_speed, new_steering_angle


def dynamic_speed_adjustment(current_speed, distance_to_opponent):
    # Decrease speed when close to the opponent, increase otherwise
    if distance_to_opponent < 100:  # Adjust
        new_speed = max(MIN_SPEED, current_speed - 50)
    else:
        new_speed = min(MAX_SPEED, current_speed + 10)
    return new_speed


def change_trajectory(current_steering_angle):
    # Adjust the pod's steering angle to follow a new trajectory
    new_steering_angle = current_steering_angle + 45  # Adjust
    return new_steering_angle


def random_evasion(current_steering_angle):
    # Periodically choose a random direction to move away from the opponent
    if random.random() < 0.2:  # Adjust
        random_angle = random.uniform(-45, 45)  # Adjust
        new_steering_angle = current_steering_angle + random_angle
        return new_steering_angle
    else:
        return current_steering_angle


def boost_away(boost_available):
    # If BOOST is available, use it to quickly accelerate away from the opponent
    if boost_available:
        return "BOOST"
    else:
        return "NORMAL"


def combination(current_speed, steering_angle, distance_to_opponent, boost_available):
    # Combine multiple avoidance strategies based on the specific situation
    if distance_to_opponent < 50:
        new_speed = simple_deceleration(current_speed)
        new_steering_angle = random_evasion(steering_angle)
    else:
        new_speed = dynamic_speed_adjustment(current_speed, distance_to_opponent)
        new_steering_angle = steering_angle

    # Optionally, incorporate BOOST strategy
    boost_strategy = boost_away(boost_available)

    return new_speed, new_steering_angle, boost_strategy


# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in
                                                                                               input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    # ---------------------------------- THRUST MANAGEMENT ------------------------------------
    current_angle = calculate_angle(x, y)

    angle_diff = calculate_angle_difference(current_angle, next_checkpoint_angle)

    dynamic_thrust = int(control_algorithm(current_angle, next_checkpoint_angle, 100))

    # ---------------------------------- /THRUST MANAGEMENT ------------------------------------

    # ---------------------------------- COLLISION MANAGEMENT ------------------------------------
    distance_to_opponent = math.sqrt((opponent_x - x) ** 2 + (opponent_y - y) ** 2)
    # ---------------------------------- /COLLISION MANAGEMENT ------------------------------------

    # ---------------------------------- MAIN  ------------------------------------

    # if next_checkpoint_angle == 0 and (next_checkpoint_x & next_checkpoint_y) < 50:
    #     thrust = MAX_SPEED
    # else:
    #     thrust = dynamic_thrust

    # if (opponent_x & opponent_y) < next_checkpoint_x & next_checkpoint_y:
    #     if next_checkpoint_dist > 4500 and next_checkpoint_angle <= 15:
    #         thrust = "BOOST"

    if distance_to_opponent < COLLISION_THRESHOLD:
        # Choose an avoidance strategy based on your game's dynamics
        # Example: Slowing down and random evasion
        thrust = simple_deceleration(next_checkpoint_dist)
        new_steering_angle = random_evasion(next_checkpoint_angle)
    else:
        # Choose a targeting strategy based on your game's dynamics
        # Example: Predictive strategy with slowdown
        thrust = int(dynamic_speed_adjustment(MAX_SPEED, distance_to_opponent))

    # ---------------------------------- /MAIN ------------------------------------
    print(str(next_checkpoint_x) + " " + str(next_checkpoint_y) + " " + str(thrust))
#   print("Debug messages...", file=sys.stderr, flush=True)
