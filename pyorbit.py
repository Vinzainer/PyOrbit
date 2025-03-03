import math
import pygame
import random

class point:
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z

class body:
    def __init__(self, location, mass, velocity, size, name = "", color = ""):
        self.location = location
        self.mass = mass
        self.velocity = velocity
        self.size = size
        self.name = name
        self.color = color

def calculate_single_body_acceleration(bodies, body_index):
    G_const = 6.67408e-11 #m3 kg-1 s-2
    acceleration = point(0,0,0)
    target_body = bodies[body_index]
    for index, external_body in enumerate(bodies):
        if index != body_index:
            r = (target_body.location.x - external_body.location.x)**2 + (target_body.location.y - external_body.location.y)**2 + (target_body.location.z - external_body.location.z)**2
            r = math.sqrt(r)
            tmp = G_const * external_body.mass / r**3
            acceleration.x += tmp * (external_body.location.x - target_body.location.x)
            acceleration.y += tmp * (external_body.location.y - target_body.location.y)
            acceleration.z += tmp * (external_body.location.z - target_body.location.z)

    return acceleration

def compute_velocity(bodies, time_step = 1):
    for body_index, target_body in enumerate(bodies):
        acceleration = calculate_single_body_acceleration(bodies, body_index)

        target_body.velocity.x += acceleration.x * time_step
        target_body.velocity.y += acceleration.y * time_step
        target_body.velocity.z += acceleration.z * time_step 


def update_location(bodies, time_step = 1):
    for target_body in bodies:
        target_body.location.x += target_body.velocity.x * time_step
        target_body.location.y += target_body.velocity.y * time_step
        target_body.location.z += target_body.velocity.z * time_step

def compute_gravity_step(bodies, time_step = 1):
    compute_velocity(bodies, time_step = time_step)
    update_location(bodies, time_step = time_step)

def plot_output(bodies, outfile = None):
    fig = plot.figure()
    colours = ['r','b','g','y','m','c']
    ax = fig.add_subplot(1,1,1, projection='3d')
    max_range = 0
    for current_body in bodies: 
        max_dim = max(max(current_body["x"]),max(current_body["y"]),max(current_body["z"]))
        if max_dim > max_range:
            max_range = max_dim
        ax.plot(current_body["x"], current_body["y"], current_body["z"], c = random.choice(colours), label = current_body["name"])        
    
    ax.set_xlim([-max_range,max_range])    
    ax.set_ylim([-max_range,max_range])
    ax.set_zlim([-max_range,max_range])
    ax.legend()        

    if outfile:
        plot.savefig(outfile)
    else:
        plot.show()

def run_simulation(bodies, names = None, time_step = 1, number_of_steps = 10000, report_freq = 100):

    #create output container for each body
    body_locations_hist = []
    for current_body in bodies:
        body_locations_hist.append({"x":[], "y":[], "z":[], "name":current_body.name})
        
    for i in range(1,number_of_steps):
        compute_gravity_step(bodies, time_step = 1000)            
        
        if i % report_freq == 0:
            for index, body_location in enumerate(body_locations_hist):
                body_location["x"].append(bodies[index].location.x)
                body_location["y"].append(bodies[index].location.y)           
                body_location["z"].append(bodies[index].location.z)       

    return body_locations_hist     

def linear_scale(source_value, target_max = 1000, source_min = -2.5e11, source_max = 2.5e11, target_min = 0):
    """
    Linearly scale a value from one range to another.

    Args:
        source_value (float): The value to be scaled.
        source_min (float): The minimum value of the source range.
        source_max (float): The maximum value of the source range.
        target_min (float): The minimum value of the target range.
        target_max (float): The maximum value of the target range.

    Returns:
        float: The scaled value in the target range.
    """
    return (source_value - source_min) * (target_max - target_min) / (source_max - source_min) + target_min   
            
#planet data (location (m), mass (kg), velocity (m/s)
sun = {"location":point(0,0,0), "mass":2e30, "velocity":point(0,0,0), "size":30}
mercury = {"location":point(0,5.7e10,0), "mass":3.285e23, "velocity":point(47000,0,0)}
venus = {"location":point(0,1.1e11,0), "mass":4.8e24, "velocity":point(35000,0,0), "size":5}
earth = {"location":point(0,1.5e11,0), "mass":6e24, "velocity":point(30000,0,0), "size":5}
mars = {"location":point(0,2.2e11,0), "mass":2.4e24, "velocity":point(24000,0,0), "size":3}
jupiter = {"location":point(0,7.7e11,0), "mass":1e28, "velocity":point(13000,0,0)}
saturn = {"location":point(0,1.4e12,0), "mass":5.7e26, "velocity":point(9000,0,0)}
uranus = {"location":point(0,2.8e12,0), "mass":8.7e25, "velocity":point(6835,0,0)}
neptune = {"location":point(0,4.5e12,0), "mass":1e26, "velocity":point(5477,0,0)}
pluto = {"location":point(0,3.7e12,0), "mass":1.3e22, "velocity":point(4748,0,0)}

if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    pygame.font.init() 
    my_font = pygame.font.SysFont('Arial', 30)
    clock = pygame.time.Clock()
    running = True

    #build list of planets in the simulation, or create your own
    bodies = [
        body( location = sun["location"], mass = sun["mass"], velocity = sun["velocity"], size = sun["size"], name = "sun", color = "yellow"),
        body( location = earth["location"], mass = earth["mass"], velocity = earth["velocity"], size = earth["size"], name = "earth", color = "blue"),
        body( location = mars["location"], mass = mars["mass"], velocity = mars["velocity"], size = mars["size"], name = "mars", color = "red"),
        body( location = venus["location"], mass = venus["mass"], velocity = venus["velocity"], size = venus["size"], name = "venus", color = "grey")
        ]

    history = []

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        text_surface = my_font.render("Earth's Mass : " + str(bodies[1].mass) + " kg", False, "white")
        screen.blit(text_surface, (0,0))

        """if len(history) > 5000:
            history = history[500:]"""

        for body, body_pos in history:
            pygame.draw.circle(screen, body.color, body_pos, 1)

        for body in bodies:
            body_pos = pygame.Vector2(linear_scale(body.location.x), linear_scale(body.location.y))
            pygame.draw.circle(screen, body.color, body_pos, body.size)
            history.append([body, body_pos])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            bodies[1].mass *= 1.1
        if keys[pygame.K_DOWN]:
            bodies[1].mass /= 1.1


        # flip() the display to put your work on screen
        pygame.display.flip()

        compute_gravity_step(bodies, time_step = 100000)  

        # limits FPS to 60
        clock.tick(60)

    pygame.quit()   