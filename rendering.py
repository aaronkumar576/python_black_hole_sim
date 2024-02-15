import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def render_grid():
    # Enable blending for transparency
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glColor4f(0.6, 0.6, 0.6, 0.2)  # Set color to white with 50% transparency
    grid_size = 100
    spacing = 10.0

    glBegin(GL_LINES)

    for i in range(-grid_size, grid_size + 1):
        # Draw lines along X-axis
        glVertex3f(i * spacing, -50, -grid_size * spacing)
        glVertex3f(i * spacing, -50, grid_size * spacing)

        # Draw lines along Z-axis
        glVertex3f(-grid_size * spacing, -50, i * spacing)
        glVertex3f(grid_size * spacing, -50, i * spacing)

    glEnd()

    # Disable blending after rendering the grid
    glDisable(GL_BLEND)

def render_black_hole(black_hole):
    # Render the black hole at its position with its specified radius
    glColor3f(1.0, 1.0, 1.0)  # Set color 
    glPushMatrix()
    glutSolidSphere(black_hole.radius, 32, 32)
    glPopMatrix()

def render_asteroid(asteroid):
    # Render the asteroid at its position with its specified radius
    glColor3f(1.0, 0.5, 0.0)  # Set color to grey
    glPushMatrix()
    glTranslatef(*asteroid.position)
    glutSolidSphere(asteroid.radius, 32, 32)
    glPopMatrix()

    # Draw the tail of the asteroid
    glColor3f(0.93, 0.96, 0.26)  # Set color to yellow
    glBegin(GL_LINE_STRIP)
    for pos in asteroid.path[-asteroid.tail_length:]:
        glVertex3f(*pos)
    glEnd()

def render_particles(particles):
    # Render particles
    glColor3f(1.0, 0.0, 0.0)  # Set color to red for particles
    glBegin(GL_POINTS)
    for particle in particles.particles:
        glVertex3f(*particle['position'])
    glEnd()

def generate_stars(num_stars, inner_cube_size=100.0, outer_cube_size=150.0):
    stars = []
    for _ in range(num_stars):
        # Randomly generate star positions within the region between two cubes
        star_pos = [random.uniform(-outer_cube_size, outer_cube_size) for _ in range(3)]
        
        # Check if the star is within the inner cube, if yes, regenerate the position
        while inner_cube_size > max(abs(coord) for coord in star_pos):
            star_pos = [random.uniform(-outer_cube_size, outer_cube_size) for _ in range(3)]
        
        stars.append(star_pos)
    return stars

def render_stars(stars):
    # Render stars in the background
    glColor3f(1.0, 1.0, 1.0)  # Set color to white
    for star in stars:
        # Set a random size for each star (adjust the range as needed)
        star_size = random.uniform(0.5, 2.5)

        # Render the star with the random size
        glPointSize(star_size)
        glBegin(GL_POINTS)
        glVertex3f(*star)
        glEnd()
        