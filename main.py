import pygame
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from camera import Camera
from physics import BlackHole, Asteroid, Particles
from rendering import render_black_hole, render_asteroid, render_particles, render_grid, generate_stars, render_stars

# Initialize Pygame
pygame.init()

# Initialize GLUT
glutInit()

# Set up display
display = (1280, 720)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Create a Camera instance
camera = Camera()

# Generate stars
stars = generate_stars(num_stars=3000)

# Create a black hole object (solar masses)
black_hole = BlackHole(mass=200.0, age=1000)

# Create an asteroid object
asteroid = Asteroid(mass=10000, radius=0.1)

# Create an instance of Particles
particles = Particles(asteroid)

# Enable depth testing
glEnable(GL_DEPTH_TEST)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                camera.toggle_free_mode()

    # Freeze and hide the mouse
    if not camera.free_mode: 
        pygame.mouse.set_visible(True) 
    else:
        pygame.mouse.set_visible(False) 
        pygame.mouse.set_pos(display[0] // 2, display[1] // 2)  # Center the mouse if in free mode

    # Calculate delta time
    delta_time = pygame.time.get_ticks() / 1000000.0  # Convert milliseconds to seconds

    # Handle user input for camera movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera.move_forward(0.1)
    if keys[pygame.K_s]:
        camera.move_backward(0.1)
    if keys[pygame.K_a]:
        camera.strafe_left(0.1)
    if keys[pygame.K_d]:
        camera.strafe_right(0.1)

    # Handle mouse input for camera rotation
    dx, dy = pygame.mouse.get_rel()
    camera.rotate(dx, dy, sensitivity=0.1)

    # Apply gravity to the asteroid
    asteroid.apply_gravity(black_hole)

    # Update asteroid position based on physics
    asteroid.update_position(delta_time)

    # Apply gravity to the particles
    particles.apply_gravity(black_hole)

    # Update particles positions based on physics
    particles.update_positions(delta_time)

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Set up the camera view
    glLoadIdentity()

    # Dynamic near clipping plane based on camera distance
    near_clip = 0.01  # Set a fixed near clipping plane value
    far_clip = near_clip + 2000

    gluPerspective(45, (display[0] / display[1]), near_clip, far_clip)
    gluLookAt(*camera.position,
              camera.position[0] + math.cos(math.radians(camera.rotation[0])),
              camera.position[1] + math.sin(math.radians(camera.rotation[1])),
              camera.position[2] + math.sin(math.radians(camera.rotation[0])),
              0.0, 1.0, 0.0)

    # Render the grid
    render_grid()

    # Render stars
    render_stars(stars)

    # Render the black hole
    render_black_hole(black_hole)

    # Apply gravity to the particles
    particles.apply_gravity(black_hole)

    # Update particle positions based on physics
    particles.update_positions(delta_time)

    # Add new particles periodically
    particles.add_particles()

    # Render the asteroid 
    render_asteroid(asteroid)

    # Render the particles 
    render_particles(particles)

    # Swap the buffers to display the rendered image
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)