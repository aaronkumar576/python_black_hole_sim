import math
import random

G = 6.67430e-11
c = 299792458.0  # Speed of light
particle_mass = 0.001
max_particle_count = 1000 # Set your desired maximum particle count

class BlackHole:
    def __init__(self, mass, age):
        self.mass = mass 
        self.radius = self.calculate_schwarzschild_radius()
        self.age = age
        self.position = [0.0, 0.0, 0.0]  # Initial position at the center

    def calculate_schwarzschild_radius(self):
        # Calculate Schwarzschild radius
        schwarzschild_radius = (2 * G * (self.mass * 1.989e30) / (c ** 2)) / 1e6
        return schwarzschild_radius
    
class Asteroid:
    def __init__(self, mass, radius, tail_length=50):
        self.mass = mass
        self.radius = radius
        self.position = [50.0, 5.0, -50.0]  # Initial position outside the black hole
        self.velocity = [-3.0, 0.0, 1.0]  # Initial velocity
        self.path = []  # List to store the path of the asteroid
        self.tail_length = tail_length

    def calculate_gravitational_force(self, black_hole):
        # Calculate gravitational force on the asteroid
        distance = math.sqrt(sum((self.position[i] - black_hole.position[i]) ** 2 for i in range(3)))
        
        # Schwarzschild metric for the radial coordinate
        g_tt = 1 - (2 * G * (black_hole.mass)) / distance

        # Calculate gravitational force using the Schwarzschild metric
        gravitational_force = (black_hole.mass * self.mass) / (distance ** 2) * g_tt

        # Calculate force components along each axis
        force_components = [(black_hole.position[i] - self.position[i]) / distance * gravitational_force for i in range(3)]
        
        return force_components

    def apply_gravity(self, black_hole):
        # Calculate gravitational force on the asteroid
        force_components = self.calculate_gravitational_force(black_hole)

        # Update asteroid velocity based on gravitational force
        self.velocity = [v + force_components[i] / self.mass for i, v in enumerate(self.velocity)]

    def update_position(self, delta_time):
        # Update position based on velocity
        for i in range(3):
            self.position[i] += self.velocity[i] * delta_time

        # Append the current position to the path
        self.path.append(tuple(self.position))

        # Keep only the last tail_length positions in the path
        self.path = self.path[-self.tail_length:]

class Particles:
    def __init__(self, asteroid, particle_count=5):
        self.asteroid = asteroid
        self.particle_count = particle_count
        self.particles = []  # List to store individual particles

        # Create particles with positions and velocities
        for _ in range(self.particle_count):
            particle = {
                'position': list(asteroid.position),
                'velocity': list(asteroid.velocity),
                'mass': particle_mass,
                'density': 1.0,
            }
            self.particles.append(particle)

    def calculate_gravitational_force(self, black_hole, particle):
        # Calculate distance between particle and black hole
        distance = math.sqrt(sum((particle['position'][i] - black_hole.position[i]) ** 2 for i in range(3)))

        # Schwarzschild metric for the radial coordinate
        g_tt = 1 - (2 * G * black_hole.mass) / distance

        # Calculate gravitational force using the Schwarzschild metric
        gravitational_force = (black_hole.mass * particle_mass) / (distance ** 2) * g_tt

        # Calculate force components along each axis
        force_components = [(black_hole.position[i] - particle['position'][i]) / distance * gravitational_force for i in range(3)]

        return force_components

    def apply_gravity(self, black_hole):
        # Apply gravitational forces to each particle
        for particle in self.particles:
            force_components = self.calculate_gravitational_force(black_hole, particle)
            
            # Update particle velocity based on forces (implement fluid dynamics)
            particle['velocity'] = [v + force_components[i] / particle_mass for i, v in enumerate(particle['velocity'])]
    
    def sph_interaction(self, viscosity_coefficient=0.1, tangential_coefficient=0.05):
        # Implement SPH interactions between particles
        for i in range(self.particle_count):
            for j in range(i + 1, self.particle_count):
                # Calculate distance between particles
                distance = math.sqrt(sum((self.particles[i]['position'][k] - self.particles[j]['position'][k]) ** 2 for k in range(3)))

                # Check for non-zero distance to avoid division by zero
                if distance == 0:
                    continue

                # Calculate relative velocity
                relative_velocity = [self.particles[j]['velocity'][k] - self.particles[i]['velocity'][k] for k in range(3)]

                # Calculate SPH viscosity force
                viscosity_force = [viscosity_coefficient * (self.particles[j]['mass'] * relative_velocity[k]) / (self.particles[i]['density'] * distance) for k in range(3)]

                # Calculate tangential force components
                tangential_force = [tangential_coefficient * (self.particles[j]['velocity'][k] - self.particles[i]['velocity'][k]) / distance for k in range(3)]

                # Update velocities of both particles
                for k in range(3):
                    self.particles[i]['velocity'][k] += (viscosity_force[k] + tangential_force[k]) / self.particles[i]['mass']
                    self.particles[j]['velocity'][k] -= (viscosity_force[k] + tangential_force[k]) / self.particles[j]['mass']

    def update_positions(self, delta_time):
        # Update positions based on velocities
        for particle in self.particles:
            for i in range(3):
                particle['position'][i] += particle['velocity'][i] * delta_time

        # Implement SPH interactions
        self.sph_interaction()

    def add_particles(self):
        # Add new particles periodically (adjust frequency as needed)
        if len(self.particles) < max_particle_count and random.random() < 0.1:
            for _ in range(5):  # Example: Add 5 particles at a time
                particle = {
                    'position': list(self.asteroid.position),
                    'velocity': list(self.asteroid.velocity),
                    'mass': particle_mass,
                    'density': 1.0
                }
                self.particles.append(particle)
                