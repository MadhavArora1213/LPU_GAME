import pygame
import sys
import random
import os
import math
from pygame import gfxdraw
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

# Initialize Pygame and OpenGL
pygame.init()
SCREEN_WIDTH = 800  # Default size before getting display info
SCREEN_HEIGHT = 600

# Force true fullscreen
pygame.display.init()
display_info = pygame.display.Info()
SCREEN_WIDTH = display_info.current_w
SCREEN_HEIGHT = display_info.current_h

# Set display mode with hardware acceleration
screen = pygame.display.set_mode((0, 0), pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN | pygame.HWSURFACE)
pygame.display.set_caption("Realistic Sky Scene with 3D Road")

# Initialize OpenGL
def init_gl():
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (SCREEN_WIDTH / SCREEN_HEIGHT), 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # Set clear color to transparent instead of black
    glClearColor(0.0, 0.0, 0.0, 0.0)

# Create a pygame surface for 2D rendering
pygame_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame_texture = None
texture_id = None

# Set up texture for pygame surface in OpenGL
def setup_pygame_surface_texture():
    global pygame_texture, texture_id
    
    # Create a new texture ID
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    # Set texture parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    # Create empty texture
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 
                GL_RGBA, GL_UNSIGNED_BYTE, None)

# Update the pygame surface as a texture
def update_pygame_texture():
    # Get pygame surface data
    data = pygame.image.tostring(pygame_surface, "RGBA", True)
    
    # Update texture with new surface data
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 
                   GL_RGBA, GL_UNSIGNED_BYTE, data)

# Render a quad with the pygame surface texture
def render_pygame_surface_background():
    # Save current matrices and settings
    glPushMatrix()
    glLoadIdentity()
    
    # Switch to orthographic projection for rendering the 2D background
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 1, 0, 1, -1, 1)
    
    glMatrixMode(GL_MODELVIEW)
    glDisable(GL_DEPTH_TEST)
    
    # Enable texturing and bind our texture
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    # Draw a quad covering the entire screen with the pygame surface
    glColor4f(1.0, 1.0, 1.0, 1.0)  # Full opacity for the background
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
    glTexCoord2f(1, 0); glVertex3f(1, 0, 0)
    glTexCoord2f(1, 1); glVertex3f(1, 1, 0)
    glTexCoord2f(0, 1); glVertex3f(0, 1, 0)
    glEnd()
    
    # Restore original settings
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    
    # Restore projection matrix
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

# 2. Update the 3D road positioning to better align with horizontal road
# Function to create OpenGL texture from pygame surface
def create_texture_from_surface(surface):
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    # Set texture parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    # Get the surface data and create texture
    data = pygame.image.tostring(surface, "RGBA", True)
    width, height = surface.get_size()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, 
                GL_RGBA, GL_UNSIGNED_BYTE, data)
    
    return texture_id

# Function to initialize the gate texture - call this after pygame init
def setup_gate_texture():
    global gate_texture_id
    if gate_image is not None:
        gate_texture_id = create_texture_from_surface(gate_image)

def draw_3d_vertical_road():
    # Reset any lingering matrix state to prevent stack accumulation
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Road parameters
    road_width = 16.0
    road_length = 100.0
    
    # Move gate to center position (adjust from 70.0)
    gate_distance = 50.0  # More centered on the visible road
    
    # Position the road and camera for better gate visibility
    # Adjust the lookAt for better centering of the gate
    gluLookAt(0, 5, 10,   # Raised eye position for better view of gate
              0, 0, -40,  # Look further down the road
              0, 1, 0)    # Up vector
    
    # Save current matrix - ONLY ONE PUSH at the beginning
    glPushMatrix()
    
    # IMPROVED POSITIONING - move road to better show gate
    glTranslatef(0, -12, -10)  # Moved up in view
    glRotatef(85, 1, 0, 0)    # Keep same angle
    
    # Draw road surface
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex3f(-road_width/2, 0, 0)
    glVertex3f(road_width/2, 0, 0)
    glVertex3f(road_width/2, road_length, 0)
    glVertex3f(-road_width/2, road_length, 0)
    glEnd()
    
    # Add junction texture at the bottom
    glColor3f(0.18, 0.18, 0.18)
    glBegin(GL_QUADS)
    glVertex3f(-road_width/2, -2, 0)
    glVertex3f(road_width/2, -2, 0)
    glVertex3f(road_width/2, 2, 0)
    glVertex3f(-road_width/2, 2, 0)
    glEnd()
    
    # ENHANCED WHITE LINES
    glColor3f(1.0, 1.0, 1.0)
    line_width = 1.2
    dash_length = 6.0
    gap_length = 4.0
    
    # Draw center and side lines - existing code here...
    for z in range(-2, int(road_length), int(dash_length + gap_length)):
        if z + dash_length <= road_length:
            glBegin(GL_QUADS)
            glVertex3f(-line_width/2, z, 0.05)  # Raised slightly above road
            glVertex3f(line_width/2, z, 0.05)
            glVertex3f(line_width/2, z + dash_length, 0.05)
            glVertex3f(-line_width/2, z + dash_length, 0.05)
            glEnd()
    
    # Draw side lines (solid white) - made more visible
    line_edge_width = 1.0  # Wider edge lines
    glBegin(GL_QUADS)
    # Left side line
    glVertex3f(-road_width/2, -2, 0.05)  # Extended below road for better connection
    glVertex3f(-road_width/2 + line_edge_width, -2, 0.05)
    glVertex3f(-road_width/2 + line_edge_width, road_length, 0.05)
    glVertex3f(-road_width/2, road_length, 0.05)
    
    # Right side line
    glVertex3f(road_width/2 - line_edge_width, -2, 0.05)
    glVertex3f(road_width/2, -2, 0.05)
    glVertex3f(road_width/2, road_length, 0.05)
    glVertex3f(road_width/2 - line_edge_width, road_length, 0.05)
    glEnd()
    
    # SIMPLIFIED GATE DRAWING - avoid nested matrix pushes
    glTranslatef(0, gate_distance, 0.2)  # Raised higher above road (0.2 instead of 0.1)
    glRotatef(-90, 1, 0, 0)
    
    gate_height = 18.0  # Taller gate (was 15.0)
    gate_width = 24.0   # Wider gate (was 20.0)
    
    # Draw textured gate - with enhanced size and visibility
    if gate_image is not None and gate_texture_id is not None:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, gate_texture_id)
        
        # Full brightness for better visibility
        glColor4f(1.0, 1.0, 1.0, 1.0)
        
        # Draw a larger textured quad for the gate
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(-gate_width/2, -0.5, 0)
        glTexCoord2f(1, 0); glVertex3f(gate_width/2, -0.5, 0) 
        glTexCoord2f(1, 1); glVertex3f(gate_width/2, -0.5, gate_height)
        glTexCoord2f(0, 1); glVertex3f(-gate_width/2, -0.5, gate_height)
        glEnd()
        
        glDisable(GL_TEXTURE_2D)
    else:
        # Draw manual gate with simpler geometry
        glColor3f(0.8, 0.75, 0.7)
        glBegin(GL_QUADS)
        # Front face of left pillar
        glVertex3f(-gate_width/2, -0.5, 0)
        glVertex3f(-gate_width/2 + 2.0, -0.5, 0)
        glVertex3f(-gate_width/2 + 2.0, -0.5, gate_height)
        glVertex3f(-gate_width/2, -0.5, gate_height)
        
        # Right pillar
        glVertex3f(gate_width/2 - 2.0, -0.5, 0)
        glVertex3f(gate_width/2, -0.5, 0)
        glVertex3f(gate_width/2, -0.5, gate_height)
        glVertex3f(gate_width/2 - 2.0, -0.5, gate_height)
        glEnd()
        
        # Top bar/archway
        glColor3f(0.7, 0.6, 0.5)
        glBegin(GL_QUADS)
        glVertex3f(-gate_width/2, -0.5, gate_height - 2.0)
        glVertex3f(gate_width/2, -0.5, gate_height - 2.0)
        glVertex3f(gate_width/2, -0.5, gate_height)
        glVertex3f(-gate_width/2, -0.5, gate_height)
        glEnd()
        
        # Add a sign board in the middle
        glColor3f(0.9, 0.85, 0.7)
        glBegin(GL_QUADS)
        glVertex3f(-gate_width/4, -0.4, gate_height/2)
        glVertex3f(gate_width/4, -0.4, gate_height/2)
        glVertex3f(gate_width/4, -0.4, gate_height/2 + gate_height/4)
        glVertex3f(-gate_width/4, -0.4, gate_height/2 + gate_height/4)
        glEnd()
    
    # ONLY ONE POP at the end to balance the push
    glPopMatrix()

# Colors - Enhanced palette for realistic sky and road
WHITE = (255, 255, 255)
DEEP_BLUE = (30, 60, 160)
ROYAL_BLUE = (65, 105, 225)
SKY_BLUE = (135, 206, 235)
LIGHT_BLUE = (173, 216, 235)
HORIZON_BLUE = (200, 230, 255)
HORIZON_PINK = (255, 210, 230)
SUN_COLOR = (255, 240, 180)
SUN_GLOW = (255, 255, 200, 100)
SUN_CORE = (255, 255, 220)
MOUNTAIN_COLOR = (80, 90, 100)
MOUNTAIN_SHADOW = (50, 60, 70)
DISTANT_MOUNTAIN = (100, 120, 150, 180)
ROAD_DARK = (50, 50, 50)
ROAD_LIGHT = (70, 70, 70)
ROAD_LINE = (240, 240, 240)
GRASS_DARK = (30, 80, 10)
GRASS_LIGHT = (60, 120, 20)
GATE_COLOR = (120, 110, 100)
GATE_DARK = (90, 80, 70)
GATE_PILLAR = (150, 140, 130)

# Asset paths
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, "assets")

# Ensure assets directory exists
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)
    os.makedirs(os.path.join(assets_dir, "images"))

# Image paths
sky_image_path = os.path.join(assets_dir, "images", "sky_background.jpg") 
cloud_image_path = os.path.join(assets_dir, "images", "cloud.webp")
gate_image = None
try:
    gate_image_path = os.path.join(assets_dir, "images", "gate.jpg")
    print(f"Attempting to load gate image from: {gate_image_path}")
    gate_image = pygame.image.load(gate_image_path).convert_alpha()
    gate_texture_id = None
    print("Gate image loaded successfully!")
except Exception as e:
    print(f"Error loading gate image: {e}")
    # Will fall back to drawn gate if image fails to load

# Create enhanced realistic sky gradient background
def create_enhanced_sky_gradient(width, height):
    sky_surface = pygame.Surface((width, height))
    
    # More complex gradient with color bands
    for y in range(height):
        # Calculate ratio (0 at top, 1 at bottom)
        ratio = y / height
        
        if ratio < 0.3:  # Upper sky - deep to royal blue
            # Transition from deep blue to royal blue
            factor = ratio / 0.3
            r = DEEP_BLUE[0] + (ROYAL_BLUE[0] - DEEP_BLUE[0]) * factor
            g = DEEP_BLUE[1] + (ROYAL_BLUE[1] - DEEP_BLUE[1]) * factor
            b = DEEP_BLUE[2] + (ROYAL_BLUE[2] - DEEP_BLUE[2]) * factor
            
        elif ratio < 0.5:  # Mid-upper sky - royal to sky blue
            # Transition from royal blue to sky blue
            factor = (ratio - 0.3) / 0.2
            r = ROYAL_BLUE[0] + (SKY_BLUE[0] - ROYAL_BLUE[0]) * factor
            g = ROYAL_BLUE[1] + (SKY_BLUE[1] - ROYAL_BLUE[1]) * factor
            b = ROYAL_BLUE[2] + (SKY_BLUE[2] - ROYAL_BLUE[2]) * factor
            
        elif ratio < 0.7:  # Mid-lower sky - sky to light blue
            # Transition from sky blue to light blue
            factor = (ratio - 0.5) / 0.2
            r = SKY_BLUE[0] + (LIGHT_BLUE[0] - SKY_BLUE[0]) * factor
            g = SKY_BLUE[1] + (LIGHT_BLUE[1] - SKY_BLUE[1]) * factor
            b = SKY_BLUE[2] + (LIGHT_BLUE[2] - SKY_BLUE[2]) * factor
            
        elif ratio < 0.85:  # Lower sky - light blue to horizon blue
            # Transition from light blue to horizon blue
            factor = (ratio - 0.7) / 0.15
            r = LIGHT_BLUE[0] + (HORIZON_BLUE[0] - LIGHT_BLUE[0]) * factor
            g = LIGHT_BLUE[1] + (HORIZON_BLUE[1] - LIGHT_BLUE[1]) * factor
            b = LIGHT_BLUE[2] + (HORIZON_BLUE[2] - LIGHT_BLUE[2]) * factor
            
        else:  # Horizon - horizon blue to pink tint
            # Transition from horizon blue to horizon pink (very subtle)
            factor = (ratio - 0.85) / 0.15
            r = HORIZON_BLUE[0] + (HORIZON_PINK[0] - HORIZON_BLUE[0]) * factor * 0.3
            g = HORIZON_BLUE[1] + (HORIZON_PINK[1] - HORIZON_BLUE[1]) * factor * 0.3
            b = HORIZON_BLUE[2] + (HORIZON_PINK[2] - HORIZON_BLUE[2]) * factor * 0.3
        
        color = (int(r), int(g), int(b))
        pygame.draw.line(sky_surface, color, (0, y), (width, y))
    
    return sky_surface

# Create distant mountains for a sense of depth
def draw_mountains(surface):
    # Far mountain range
    mountain_height = SCREEN_HEIGHT * 0.1
    mountain_y = SCREEN_HEIGHT * 0.85
    
    # Create a surface for the mountains with alpha
    mountain_surface = pygame.Surface((SCREEN_WIDTH, int(mountain_height)), pygame.SRCALPHA)
    
    # Generate multiple mountain peaks
    num_peaks = 10
    points = [(0, mountain_height)]  # Start at bottom left
    
    peak_width = SCREEN_WIDTH / (num_peaks - 1)
    
    for i in range(num_peaks):
        x = i * peak_width
        # Random height with constraints to make some mountains taller
        if i % 3 == 0:  # Make every 3rd mountain taller
            y = random.uniform(0.3, 0.6) * mountain_height
        else:
            y = random.uniform(0.5, 0.9) * mountain_height
        points.append((x, y))
    
    # Add bottom right corner
    points.append((SCREEN_WIDTH, mountain_height))
    
    # Draw the mountain polygon
    pygame.draw.polygon(mountain_surface, DISTANT_MOUNTAIN, points)
    
    # Blend the mountain range onto the main surface
    surface.blit(mountain_surface, (0, int(mountain_y)))

# Enhanced sun with better glow and rays
def draw_enhanced_sun(surface, x, y, radius):
    # Draw multiple glow layers with decreasing opacity
    for i in range(10):
        glow_radius = radius + (i * 10)
        glow_alpha = 100 - (i * 10)
        if glow_alpha < 0:
            glow_alpha = 0
            
        glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (255, 255, 200, glow_alpha), (glow_radius, glow_radius), glow_radius)
        surface.blit(glow_surface, (x - glow_radius, y - glow_radius))
    
    # Draw the core sun with a gradient
    for i in range(radius, 0, -1):
        # Calculate color based on distance from center
        factor = i / radius
        r = SUN_CORE[0] * (1 - factor) + SUN_COLOR[0] * factor
        g = SUN_CORE[1] * (1 - factor) + SUN_COLOR[1] * factor
        b = SUN_CORE[2] * (1 - factor) + SUN_COLOR[2] * factor
        
        color = (int(r), int(g), int(b))
        gfxdraw.filled_circle(surface, int(x), int(y), i, color)
    
    # Draw light rays - longer, more varied rays
    for i in range(16):
        angle = math.radians(i * 22.5)  # 16 rays around the sun
        ray_length = random.randint(radius + 60, radius + 120)
        end_x = x + math.cos(angle) * ray_length
        end_y = y + math.sin(angle) * ray_length
        
        # Create a surface for the ray with transparency
        ray_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Draw the ray with varying thickness and alpha
        ray_alpha = random.randint(30, 60)
        ray_width = random.randint(2, 4)
        pygame.draw.line(ray_surface, (255, 255, 200, ray_alpha), (x, y), (end_x, end_y), ray_width)
        
        # Add a subtle glow to the ray
        for w in range(1, 4):
            pygame.draw.line(ray_surface, (255, 255, 220, ray_alpha//2), 
                            (x, y), (end_x, end_y), ray_width + w*2)
        
        surface.blit(ray_surface, (0, 0))

# Function to draw a horizontal road at the bottom
def draw_road(surface):
    # Road parameters
    road_height = SCREEN_HEIGHT * 0.15  # Road takes up 15% of screen height
    road_y = SCREEN_HEIGHT * 0.85  # Position at 85% down the screen
    
    # Draw road base (asphalt)
    road_surface = pygame.Surface((SCREEN_WIDTH, int(road_height)))
    
    # Create asphalt texture with subtle variations
    for y in range(int(road_height)):
        for x in range(0, SCREEN_WIDTH, 10):  # Create texture in 10px blocks
            # Randomize the asphalt color slightly for realism
            color_variation = random.randint(-5, 5)
            if (x // 10 + y // 10) % 2 == 0:
                color = (ROAD_DARK[0] + color_variation, 
                         ROAD_DARK[1] + color_variation, 
                         ROAD_DARK[2] + color_variation)
            else:
                color = (ROAD_LIGHT[0] + color_variation, 
                         ROAD_LIGHT[1] + color_variation, 
                         ROAD_LIGHT[2] + color_variation)
            
            pygame.draw.rect(road_surface, color, (x, y, 10, 1))
    
    # Create road edge curves for realism
    road_edge = 10  # Edge width in pixels
    for x in range(SCREEN_WIDTH):
        # Top edge shading gradient
        for i in range(road_edge):
            alpha = 128 - (i * 128 // road_edge)
            pygame.draw.line(road_surface, (20, 20, 20, alpha), 
                           (x, i), (x, i), 1)
        
        # Bottom edge highlight gradient
        for i in range(road_edge):
            alpha = 100 - (i * 100 // road_edge)
            pygame.draw.line(road_surface, (90, 90, 90, alpha), 
                           (x, road_height - i - 1), (x, road_height - i - 1), 1)
    
    # Draw center line markings (dashed white lines)
    line_width = int(road_height * 0.05)  # Line width relative to road height
    line_length = int(SCREEN_WIDTH * 0.05)  # Each dash is 5% of screen width
    line_gap = int(SCREEN_WIDTH * 0.03)    # Gap between dashes is 3% of width
    line_y = road_height // 2 - line_width // 2  # Vertical center of road
    
    # Draw dashed lines across the road, but skip the middle section for the vertical road
    vertical_road_width = SCREEN_WIDTH * 0.15
    vertical_road_half_width = vertical_road_width / 2
    
    for x in range(0, SCREEN_WIDTH, line_length + line_gap):
        # Skip drawing the center lines where the vertical road connects
        if x < (SCREEN_WIDTH/2 - vertical_road_half_width) or x > (SCREEN_WIDTH/2 + vertical_road_half_width):
            pygame.draw.rect(road_surface, ROAD_LINE, (x, line_y, line_length, line_width))
    
    # Draw road edge lines (solid)
    edge_line_width = max(2, int(road_height * 0.02))
    pygame.draw.rect(road_surface, ROAD_LINE, (0, 0, SCREEN_WIDTH, edge_line_width))
    pygame.draw.rect(road_surface, ROAD_LINE, (0, road_height - edge_line_width, SCREEN_WIDTH, edge_line_width))
    
    # REMOVED: No more grass on sides of the horizontal road
    
    # Create connection at the vertical road intersection
    vertical_road_width = SCREEN_WIDTH * 0.15
    connection_width = vertical_road_width * 1.1  # Slightly wider than the vertical road
    
    # Draw a darker patch at the connection point
    connection_rect = pygame.Rect(
        SCREEN_WIDTH/2 - connection_width/2,
        0,  # Start from the top of the road surface
        connection_width,
        road_height * 0.3  # Cover the top portion of the road
    )
    
    # Draw connection with a slightly darker color
    connection_color = (ROAD_DARK[0] - 5, ROAD_DARK[1] - 5, ROAD_DARK[2] - 5)
    pygame.draw.rect(road_surface, connection_color, connection_rect)
    
    # Draw the road onto the main surface
    surface.blit(road_surface, (0, int(road_y)))

# Enhanced cloud class with more realistic appearance and modified positioning
class EnhancedCloud:
    def __init__(self, use_image=False, cloud_img=None):
        # Clouds only at the top 20% of the screen per user request
        self.width = random.randint(200, 400)  # Wider clouds for better horizontal coverage
        self.height = random.randint(80, 150)
        
        # Position clouds to cover the entire width but only top 20%
        self.x = random.randint(-300, SCREEN_WIDTH)
        self.y = random.randint(10, int(SCREEN_HEIGHT * 0.2))  # Only top 20% of screen
        
        # Slower movement for more stability
        self.speed = random.uniform(0.2, 0.5)
        
        # Cloud shape parameters
        self.segments = random.randint(5, 8)  # More segments for fuller clouds
        self.segment_sizes = []
        
        # Generate varied segment sizes for procedural clouds
        for _ in range(self.segments):
            self.segment_sizes.append({
                'width': random.uniform(0.3, 0.7) * self.width,
                'height': random.uniform(0.6, 0.9) * self.height,
                'x_offset': random.uniform(0, 0.8) * self.width,
                'y_offset': random.uniform(0, 0.3) * self.height
            })
        
        self.use_image = use_image
        if self.use_image and cloud_img:
            self.image = pygame.transform.scale(cloud_img, (self.width, self.height))
    
    def update(self):
        # Smoother movement
        self.x += self.speed
        if self.x > SCREEN_WIDTH + 100:  # Move clouds further off screen before resetting
            self.x = -self.width - random.randint(0, 200)  # Add randomness to re-entry
            self.y = random.randint(10, int(SCREEN_HEIGHT * 0.2))  # Maintain top 20% position
    
    def draw(self, surface):
        if self.use_image:
            surface.blit(self.image, (self.x, self.y))
        else:
            # Enhanced procedural cloud with multiple segments for more natural appearance
            cloud_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            
            # Base cloud shape
            for segment in self.segment_sizes:
                x_pos = segment['x_offset']
                y_pos = segment['y_offset']
                width = segment['width']
                height = segment['height']
                
                # Draw each cloud segment with a soft edge
                pygame.draw.ellipse(cloud_surface, (255, 255, 255, 210), 
                                   (x_pos, y_pos, width, height))
                
                # Add highlight to top of cloud
                highlight_height = height * 0.6
                highlight_width = width * 0.8
                pygame.draw.ellipse(cloud_surface, (255, 255, 255, 230), 
                                   (x_pos + width*0.1, y_pos, highlight_width, highlight_height))
            
            # Add a subtle shadow at the bottom
            for segment in self.segment_sizes:
                x_pos = segment['x_offset']
                y_pos = segment['y_offset'] + segment['height'] * 0.7
                width = segment['width']
                height = segment['height'] * 0.3
                
                pygame.draw.ellipse(cloud_surface, (220, 220, 230, 100), 
                                   (x_pos, y_pos, width, height))
            
            surface.blit(cloud_surface, (self.x, self.y))

# Generate the sky
custom_sky = create_enhanced_sky_gradient(SCREEN_WIDTH, SCREEN_HEIGHT)

# Load images if they exist, otherwise use procedural generation
use_bg_image = False
try:
    print(f"Attempting to load sky background from: {sky_image_path}")
    background = pygame.image.load(sky_image_path).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    use_bg_image = True
    print("Sky background loaded successfully!")
except Exception as e:
    use_bg_image = False
    print(f"Error loading sky background: {e}")
    print("Using custom gradient sky instead.")

use_cloud_image = False
cloud_img = None
try:
    print(f"Attempting to load cloud image from: {cloud_image_path}")
    cloud_img = pygame.image.load(cloud_image_path).convert_alpha()
    use_cloud_image = True
    print("Cloud image loaded successfully!")
except Exception as e:
    use_cloud_image = False
    print(f"Error loading cloud image: {e}")
    print("Using procedural clouds instead.")

# Initialize OpenGL settings
init_gl()

# Set up textures
setup_pygame_surface_texture()
setup_gate_texture()  # Add this line to initialize the gate texture

# Create clouds
clouds = [EnhancedCloud(use_cloud_image, cloud_img) for _ in range(25)]

# Sun position
sun_x = SCREEN_WIDTH * 0.8
sun_y = SCREEN_HEIGHT * 0.15
sun_radius = int(SCREEN_HEIGHT * 0.05)

# Game loop
clock = pygame.time.Clock()
running = True

pygame.mouse.set_visible(False)

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
    
    # Update clouds
    for cloud in clouds:
        cloud.update()
    
    # Clear pygame surface
    pygame_surface.fill((0, 0, 0))
    
    # Draw everything on pygame surface
    if use_bg_image:
        pygame_surface.blit(background, (0, 0))
    else:
        pygame_surface.blit(custom_sky, (0, 0))
        draw_mountains(pygame_surface)
        draw_enhanced_sun(pygame_surface, int(sun_x), int(sun_y), sun_radius)
    
    # Draw ONLY the horizontal road at the bottom of the screen
    draw_road(pygame_surface)
    
    # Draw clouds
    for cloud in clouds:
        cloud.draw(pygame_surface)
    
    # Clear the OpenGL buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Update texture from pygame surface
    update_pygame_texture()
    
    # First render the pygame surface as background
    render_pygame_surface_background()
    
    # Then render ONLY the 3D vertical road with proper positioning
    glLoadIdentity()
    draw_3d_vertical_road()
    
    # Display everything
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Cleanup
pygame.mouse.set_visible(True)
pygame.quit()
sys.exit()