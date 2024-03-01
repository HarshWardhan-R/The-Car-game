import pygame
from pygame.locals import QUIT, KEYDOWN, K_a, K_d, K_s, K_w
import random
import csv
import time

pygame.init()

# Game window
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Racing Game ")

# Load images and scale them
car_img = pygame.transform.scale(pygame.image.load("Car.png"), (80, 120))
obstacle_img = pygame.transform.scale(pygame.image.load("Obstacle2.png"), (100, 100))
road_img = pygame.transform.scale(pygame.image.load("Road.png"), (500, height)) 

# Car
car_width, car_height = 50, 80
car_x, car_y = (width - car_width) // 2, height - car_height - 10
car_speed = 8

# Road
road_width = 500
road_x = (width - road_width) // 2

# Obstacles
obstacle_speed = 5
initial_obstacle_frequency = 40
obstacle_frequency = initial_obstacle_frequency
obstacle_min_gap = 200  # Minimum gap between obstacles
obstacles = []



            
# Score
score = 0
highest_score = 0
font = pygame.font.Font(None, 36)







# CSV file
csv_filename = "highest_scores.csv"

def load_highest_score():
    try:
        with open(csv_filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                return int(row['highest_score'])
    except FileNotFoundError:
        return 0


def save_highest_score(new_score):
    with open(csv_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['player_id', 'highest_score'])
        writer.writerow([1, new_score])  # Assuming player_id is 1 for simplicity


# Welcome Screen
screen.fill((255, 255, 255))
welcome_text = font.render("Welcome to Car Racing Game!", True, (0, 0, 0))
screen.blit(welcome_text, ((width - welcome_text.get_width()) // 2, height // 3))
pygame.display.flip()


# Game loop
running = True
clock = pygame.time.Clock()

def draw_obstacles():
    for obstacle in obstacles:
        screen.blit(obstacle_img, obstacle)



# Load initial highest score from CSV
highest_score = load_highest_score()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Move the car
    keys = pygame.key.get_pressed()
    if keys[K_a] and car_x > road_x:
        car_x -= car_speed
    if keys[K_d] and car_x < road_x + road_width - car_width:
        car_x += car_speed
    if keys[K_w] and car_y > 0:
        car_y -= car_speed
    if keys[K_s] and car_y < height - car_height:
        car_y += car_speed

    
    if random.randint(0, obstacle_frequency) == 0:
        obstacle_width = random.randint(50, 100)
        obstacle_gap = obstacle_min_gap + random.randint(0, road_width - obstacle_min_gap - obstacle_width)

        obstacle_x = random.randint(road_x, road_x + road_width - obstacle_width)  # Random obstacle placement
        obstacle_y = -car_height
        obstacles.append(pygame.Rect(obstacle_x, obstacle_y, obstacle_width, car_height))

    for obstacle in obstacles:
        obstacle.y += obstacle_speed + score // 100  # Increase obstacle speed with progress

        # Check for collision with car
        if obstacle.colliderect(pygame.Rect(car_x, car_y, car_width, car_height)):
            running = False

    # Remove obstacles 
    obstacles = [obstacle for obstacle in obstacles if obstacle.y < height]

    # Increase score and adjust obstacle frequency
    score += 1
    if score % 100 == 0:
        obstacle_frequency = max(initial_obstacle_frequency - score // 100, 15)
        car_speed+=1

    

    # Draw everything
    screen.fill((255, 255, 255))  # White background

    # Draw road
    pygame.draw.rect(screen, (169, 169, 169), (road_x, 0, road_width, height))

    # Draw road
    

    # Draw car
    screen.blit(car_img, (car_x, car_y))

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, (255, 0, 0), obstacle)
    draw_obstacles()

    # Display score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Display highest score on the screen
    highest_score_text = font.render(f"Highest Score: {highest_score}", True, (0, 0, 0))
    screen.blit(highest_score_text, (width - highest_score_text.get_width() - 10, 10))

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(30)

#final score
final_score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
screen.blit(final_score_text, ((width - final_score_text.get_width()) // 2, (height - final_score_text.get_height()) // 2))
pygame.display.flip()


# Update highest Score
if score>highest_score:
    highest_score=score


# Save highest score to CSV file
save_highest_score(highest_score)

# Display highest score at the end
print(f"Highest Score: {highest_score}")


time.sleep(3)

# Quit
pygame.quit()
