import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sky Cloud Game")

# Colors
BLUE = (135, 206, 235)
WHITE = (255, 255, 255)

# Asset paths
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, "assets")

# Ensure assets directory exists
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)
    os.makedirs(os.path.join(assets_dir, "images"))

# For the actual game, you would save the sky and cloud images to these paths
sky_image_path = os.path.join(assets_dir, "images", "sky_background.jpg")
cloud_image_path = os.path.join(assets_dir, "images", "cloud.png")

# Load images if they exist, otherwise use placeholders
try:
    background = pygame.image.load(sky_image_path).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    use_bg_image = True
except:
    use_bg_image = False
    print("Sky background image not found. Using color fill.")

try:
    cloud_img = pygame.image.load(cloud_image_path).convert_alpha()
    use_cloud_image = True
except:
    use_cloud_image = False
    print("Cloud image not found. Using procedural clouds.")

class Cloud:
    def __init__(self):
        self.width = random.randint(100, 200)
        self.height = random.randint(60, 100)
        self.x = random.randint(-200, SCREEN_WIDTH)
        self.y = random.randint(50, 300)
        self.speed = random.uniform(0.5, 1.5)
        
        if use_cloud_image:
            self.image = pygame.transform.scale(cloud_img, (self.width, self.height))
        
    def update(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH:
            self.x = -200
            self.y = random.randint(50, 300)
            
    def draw(self, surface):
        if use_cloud_image:
            surface.blit(self.image, (self.x, self.y))
        else:
            # Draw a procedural cloud
            pygame.draw.ellipse(surface, WHITE, (self.x, self.y, self.width, self.height))
            pygame.draw.ellipse(surface, WHITE, (self.x + self.width * 0.2, self.y - self.height * 0.2, self.width * 0.6, self.height * 0.6))
            pygame.draw.ellipse(surface, WHITE, (self.x + self.width * 0.4, self.y + self.height * 0.2, self.width * 0.6, self.height * 0.6))

# Create a list of clouds
clouds = [Cloud() for _ in range(8)]

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update clouds
    for cloud in clouds:
        cloud.update()
    
    # Draw everything
    if use_bg_image:
        screen.blit(background, (0, 0))
    else:
        screen.fill(BLUE)  # Fill the screen with sky blue
    
    # Draw clouds
    for cloud in clouds:
        cloud.draw(screen)
    
    # Add a simple instruction text
    font = pygame.font.SysFont('Arial', 24)
    text = font.render('Sky Cloud Scene', True, (0, 0, 0))
    screen.blit(text, (20, 20))
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()