from ROBOT_ACTIONS import *
from time import *

min_distance = 0
max_distance = 232
max_angle = 135

# Smoothing factor for filtering (between 0 and 1)
smoothing_factor = 0.05  # lower = smoother
filtered_angle = 0

def distance_to_angle(distance):
    if distance == -1:
        return None  # Skip if invalid
    distance = min(max(distance, min_distance), max_distance)
    angle = (distance / max_distance) * max_angle
    return int(angle)

while True:
    raw_distance = obstacle_distance()
    target_angle = distance_to_angle(raw_distance)

    if target_angle is None:
        print("No object detected.")
        continue

    # Apply smoothing
    filtered_angle = int(filtered_angle + smoothing_factor * (target_angle - filtered_angle))

    print(f"Distance: {raw_distance:.2f} cm | Target Angle: {target_angle} | Filtered Angle: {filtered_angle}")
    move_servo(0, filtered_angle)

    sleep(0.005)  # Adjust for responsiveness


