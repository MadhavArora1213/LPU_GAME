import pygame
import os

# Initialize pygame
pygame.init()

# Create assets directory if it doesn't exist
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, "assets", "images")
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

def save_sky_background():
    """
    Creates a sky background similar to the image and saves it
    """
    # Create a surface for the sky
    width, height = 800, 600
    sky = pygame.Surface((width, height))
    
    # Fill with gradient blue (simple version)
    sky_top = (100, 150, 255)  # Lighter blue at top
    sky_bottom = (135, 206, 235)  # Sky blue at bottom
    
    for y in range(height):
        # Calculate color for this row (simple linear gradient)
        r = sky_top[0] + (sky_bottom[0] - sky_top[0]) * y / height
        g = sky_top[1] + (sky_bottom[1] - sky_top[1]) * y / height
        b = sky_top[2] + (sky_bottom[2] - sky_top[2]) * y / height
        
        # Draw a line of this color
        pygame.draw.line(sky, (r, g, b), (0, y), (width, y))
    
    # Save the sky image
    pygame.image.save(sky, os.path.join(assets_dir, "sky_background.jpg"))
    print(f"Sky background saved to {os.path.join(assets_dir, 'sky_background.jpg')}")

def create_cloud():
    """
    Creates a simple cloud image and saves it
    """
    width, height = 200, 100
    cloud = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw cloud shapes
    pygame.draw.ellipse(cloud, (255, 255, 255, 230), (0, 20, 100, 60))
    pygame.draw.ellipse(cloud, (255, 255, 255, 230), (30, 10, 80, 50))
    pygame.draw.ellipse(cloud, (255, 255, 255, 230), (80, 15, 90, 70))
    pygame.draw.ellipse(cloud, (255, 255, 255, 230), (50, 30, 70, 50))
    
    # Save the cloud image
    pygame.image.save(cloud, os.path.join(assets_dir, "cloud.png"))
    print(f"Cloud image saved to {os.path.join(assets_dir, 'cloud.png')}")

# Generate and save the images
save_sky_background()
create_cloud()

print("Images created successfully! You can now run the main game.")