import pygame
import pymunk
import pymunk.pygame_util
import random

# Setting up some constants
WIDTH, HEIGHT = 800, 600
GRAVITY = (0.0, 900.0)  # Changed gravity direction
STRING_TENSION = 50.0
NODE_MASS = 10.0
NODE_SIZE = 20  # New constant for the size of the nodes

# Pygame init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Pymunk init
space = pymunk.Space()
space.gravity = GRAVITY
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Function to create a node (a circle)


def create_node(position, shape_type='circle'):
    # Inverting y-coordinate
    position = pymunk.Vec2d(position[0], HEIGHT - position[1])
    body = pymunk.Body(NODE_MASS, pymunk.moment_for_circle(
        NODE_MASS, 0, NODE_SIZE), body_type=pymunk.Body.DYNAMIC)
    body.position = position
    if shape_type == 'circle':
        shape = pymunk.Circle(body, NODE_SIZE)
    elif shape_type == 'box':
        shape = pymunk.Poly.create_box(body, (NODE_SIZE * 2, NODE_SIZE * 2))
    elif shape_type == 'triangle':
        shape = pymunk.Poly(
            body, [(0, 0), (NODE_SIZE * 2, 0), (NODE_SIZE, NODE_SIZE * 2)])
    shape.elasticity = 0.9
    space.add(body, shape)
    return body

# Function to create a string (a Segment)


def create_string(node1, node2):
    joint = pymunk.DampedSpring(
        node1, node2, (0, 0), (0, 0), rest_length=100, stiffness=STRING_TENSION, damping=0.5)
    space.add(joint)

# Define the initial setup


def reset_simulation():
    for shape in space.shapes:
        # Just remove the shape, the body will be removed automatically if not used by another shape
        space.remove(shape)
    for constraint in space.constraints:
        space.remove(constraint)

# Define the edges of the screen to keep objects inside


def create_screen_edges():
    edge_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    edges = [
        pymunk.Segment(edge_body, (0, 0), (0, HEIGHT), 1),  # Left edge
        pymunk.Segment(edge_body, (0, 0), (WIDTH, 0), 1),  # Bottom edge
        pymunk.Segment(edge_body, (WIDTH, HEIGHT),
                       (WIDTH, 0), 1),  # Right edge
        pymunk.Segment(edge_body, (WIDTH, HEIGHT), (0, HEIGHT), 1)  # Top edge
    ]
    for edge in edges:
        edge.elasticity = 0.9
    space.add(edge_body, *edges)


reset_simulation()
create_screen_edges()  # Create the edges

# Create some nodes
node1 = create_node((100, 100))
node2 = create_node((200, 100))
node3 = create_node((150, 200))

# Create some strings between the nodes
create_string(node1, node2)
create_string(node2, node3)
create_string(node3, node1)

# Mouse body for dragging nodes
mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
# Last clicked body for linking nodes with a string
last_clicked_body = None

# Define the position and size of the reset button
reset_button = pygame.Rect(10, 10, 100, 50)

# Define the position and size of the spawn button
spawn_button = pygame.Rect(120, 10, 100, 50)

# Mouse body for dragging nodes
mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
# Last clicked body for linking nodes with a string
last_clicked_body = None

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = event.pos
            if event.button == 1:  # Left mouse button
                if reset_button.collidepoint(mouse_position):
                    reset_simulation()
                    create_screen_edges()
                    node1 = create_node((100, 100))
                    node2 = create_node((200, 100))
                    node3 = create_node((150, 200))
                    create_string(node1, node2)
                    create_string(node2, node3)
                    create_string(node3, node1)
                elif spawn_button.collidepoint(mouse_position):
                    x = random.randint(NODE_SIZE, WIDTH - NODE_SIZE)
                    y = random.randint(NODE_SIZE, HEIGHT - NODE_SIZE)
                    create_node((x, y))
                else:
                    hit = space.point_query_nearest(pymunk.pygame_util.from_pygame(
                        mouse_position, screen), NODE_SIZE, pymunk.ShapeFilter())
                    if hit:
                        shape = hit.shape
                        joint = pymunk.PivotJoint(mouse_body, shape.body, (0, 0), shape.body.world_to_local(
                            pymunk.pygame_util.from_pygame(mouse_position, screen)))
                        space.add(joint)
            elif event.button == 3:  # Right mouse button
                hit = space.point_query_nearest(pymunk.pygame_util.from_pygame(
                    mouse_position, screen), NODE_SIZE, pymunk.ShapeFilter())
                if hit and last_clicked_body:
                    create_string(last_clicked_body, hit.shape.body)
                last_clicked_body = hit.shape.body if hit else None
        elif event.type == pygame.MOUSEBUTTONUP:
            for joint in list(mouse_body.constraints):
                if joint in space.constraints:
                    space.remove(joint)
        elif event.type == pygame.MOUSEMOTION:
            mouse_body.position = pymunk.pygame_util.from_pygame(
                event.pos, screen)

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the reset button
    pygame.draw.rect(screen, (255, 0, 0), reset_button)
    font = pygame.font.Font(None, 24)
    text = font.render("Reset", True, (255, 255, 255))
    text_rect = text.get_rect(center=reset_button.center)
    screen.blit(text, text_rect)

    # Draw the spawn button
    pygame.draw.rect(screen, (0, 255, 0), spawn_button)
    font = pygame.font.Font(None, 24)
    text = font.render("Spawn", True, (255, 255, 255))
    text_rect = text.get_rect(center=spawn_button.center)
    screen.blit(text, text_rect)

    # Step the physics
    space.step(1/60.0)

    # Draw everything
    for shape in space.shapes:
        if isinstance(shape, pymunk.Circle):
            pos_x, pos_y = pymunk.pygame_util.to_pygame(
                shape.body.position, screen)
            pygame.draw.circle(screen, (0, 0, 255), (int(
                pos_x), int(pos_y)), int(shape.radius), 1)
        elif isinstance(shape, pymunk.Segment):
            a = pymunk.pygame_util.to_pygame(
                shape.a+shape.body.position, screen)
            b = pymunk.pygame_util.to_pygame(
                shape.b+shape.body.position, screen)
            pygame.draw.lines(screen, (0, 255, 0), False, [a, b], 1)
        elif isinstance(shape, pymunk.Poly):
            vertices = [pymunk.pygame_util.to_pygame(
                v+shape.body.position, screen) for v in shape.get_vertices()]
            pygame.draw.polygon(screen, (255, 0, 0), vertices, 1)

    # Draw the strings
    for constraint in space.constraints:
        if isinstance(constraint, pymunk.DampedSpring):
            a = pymunk.Vec2d(
                *pymunk.pygame_util.to_pygame(constraint.a.position, screen))
            b = pymunk.Vec2d(
                *pymunk.pygame_util.to_pygame(constraint.b.position, screen))
            delta = (b - a) / 10
            points = [a + i * delta for i in range(11)]
            for i in range(5):
                offset = 10 * ((-1) ** i) * delta.cross((0, 0)) / delta.length
                points[2 * i + 1] += pymunk.Vec2d(offset, offset)
            pygame.draw.lines(screen, (0, 255, 0), False, points, 1)

    # Flip the screen
    pygame.display.flip()

    # Tick the clock
    clock.tick(60)
