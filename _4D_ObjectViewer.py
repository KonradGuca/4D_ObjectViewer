import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

print("")
print("4D OcjectViewer")
print("by Konrad Guca")
print("Creator of the GUCA 4D coordinate system")
print("")
print("Controls:")
print("Z - rotate 90 degrees to right")
print("X - rotate 90 degrees to left")
print("W - rotate upwards")
print("S - rotate downwards")
print("A - rotate left")
print("D - rotate right")
print("Q - rotate left - Z axis")
print("E - rotate right - Z axis")
print("Num + zoom in")
print("Num - zoom out")
print("Space - reset camera view")
print("")
print("Axle description:")
print("G axis - blue point")
print("U axis - green point")
print("C axis - yellow point")
print("A axis - red point")
print("0 - purple point")
print("")
print("Enter value:")

# Camera position
x_rot = 45
y_rot = 35
z_rot = 75
z_trans = -20
zoom = 1.0

# OpenGL scene
def setup():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    if zoom < 1.0:
        glOrtho(-20 / zoom, 20 / zoom, -20 / zoom, 20 / zoom, 1, 100)
    else:
        glOrtho(-20, 20, -20, 20, 1, 100)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, z_trans)
    glRotatef(x_rot, 1, 0, 0)
    glRotatef(y_rot, 0, 1, 0)
    glRotatef(z_rot, 0, 0, 1)

# Draw vertex as point
def draw_vertex(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glPointSize(10)
    glBegin(GL_POINTS)
    glVertex3f(0, 0, 0)
    glEnd()
    glPopMatrix()

# Draw edges option
def draw_edges(vertices):
    glEnable(GL_DEPTH_TEST)
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINES)
    for edge in vertices:
        for vertex in edge:
            glVertex3fv(vertex)
    glEnd()
    glDisable(GL_DEPTH_TEST)

# Start pygame and OpenGL
pygame.init()
display = (800, 800)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
setup()

# Input values
g = int(input("Value g (0-10): "))
u = int(input("Value u (0-10): "))
c = int(input("Value c (0-10): "))
a = int(input("Value a (0-10): "))

# Input values range 0-10
g = max(0, min(10, g))
u = max(0, min(10, u))
c = max(0, min(10, c))
a = max(0, min(10, a))

if g == 0:
    vertices = {
        "0": np.array([0, 0, 0]),
        "U": np.array([-u, u, -u]),
        "C": np.array([-c, -c, c]),
        "A": np.array([a, -a, -a]),
        "UC": np.array([-u - c, u - c, -u + c]),
        "CA": np.array([-c + a, -c - a, c - a]),
        "UA": np.array([-u + a, u - a, -u - a]),
        "UCA": np.array([-u - c + a, u - c - a, -u + c - a]),
    }

    edges = [
        ("0", "U"),
        ("0", "C"),
        ("0", "A"),
        ("U", "UC"),
        ("C", "UC"),
        ("C", "CA"),
        ("A", "CA"),
        ("A", "UA"),
        ("U", "UA"),
        ("CA", "UCA"),
        ("UC", "UCA"),
        ("UA", "UCA")
    ]
elif u == 0:
    vertices = {
        "0": np.array([0, 0, 0]),
        "G": np.array([g, g, g]),
        "C": np.array([-c, -c, c]),
        "A": np.array([a, -a, -a]),
        "GC": np.array([g - c, g - c, g + c]),
        "CA": np.array([-c + a, -c - a, c - a]),
        "GA": np.array([g + a, g - a, g - a]),
        "GCA": np.array([g - c + a, g - c - a, g + c - a]),
    }

    edges = [
        ("0", "G"),
        ("0", "C"),
        ("0", "A"),
        ("C", "GC"),
        ("G", "GC"),
        ("C", "CA"),
        ("A", "CA"),
        ("A", "GA"),
        ("CA", "GCA"),
        ("GA", "GCA"),
        ("GC", "GCA"),
        ("G", "GA")
    ]
elif c == 0:
    vertices = {
        "0": np.array([0, 0, 0]),
        "G": np.array([g, g, g]),
        "U": np.array([-u, u, -u]),
        "A": np.array([a, -a, -a]),
        "GU": np.array([g - u, g + u, g - u]),
        "GA": np.array([g + a, g - a, g - a]),
        "UA": np.array([-u + a, u - a, -u - a]),
        "GUA": np.array([g - u + a, g + u - a, g - u - a]),
    }

    edges = [
        ("0", "G"),
        ("0", "U"),
        ("0", "A"),
        ("G", "GU"),
        ("U", "GU"),
        ("A", "UA"),
        ("G", "UA"),
        ("UA", "GUA"),
        ("GU", "GUA"),
        ("GUA", "GUA")
    ]
elif a == 0:
    vertices = {
        "0": np.array([0, 0, 0]),
        "G": np.array([g, g, g]),
        "U": np.array([-u, u, -u]),
        "C": np.array([-c, -c, c]),
        "GU": np.array([g - u, g + u, g - u]),
        "UC": np.array([-u - c, u - c, -u + c]),
        "GC": np.array([g - c, g - c, g + c]),
        "GUC": np.array([g - u - c, g + u - c, g - u + c]),
    }

    edges = [
        ("0", "G"),
        ("0", "U"),
        ("0", "C"),
        ("G", "GU"),
        ("U", "UC"),
        ("C", "UC"),
        ("U", "GU"),
        ("C", "GC"),
        ("G", "GC"),
        ("GU", "GUC"),
        ("GC", "GUC"),
        ("UC", "GUC")
    ]
else:
    vertices = {
        "0": np.array([0, 0, 0]),
        "G": np.array([g, g, g]),
        "U": np.array([-u, u, -u]),
        "C": np.array([-c, -c, c]),
        "A": np.array([a, -a, -a]),
        "GU": np.array([g - u, g + u, g - u]),
        "UC": np.array([-u - c, u - c, -u + c]),
        "GC": np.array([g - c, g - c, g + c]),
        "GUC": np.array([g - u - c, g + u - c, g - u + c]),
        "CA": np.array([-c + a, -c - a, c - a]),
        "GA": np.array([g + a, g - a, g - a]),
        "GCA": np.array([g - c + a, g - c - a, g + c - a]),
        "UA": np.array([-u + a, u - a, -u - a]),
        "UCA": np.array([-u - c + a, u - c - a, -u + c - a]),
        "GUA": np.array([g - u + a, g + u - a, g - u - a]),
        "GUCA": np.array([g - u - c + a, g + u - c - a, g - u + c - a]),
    }

    edges = [
        ("0", "G"),
        ("0", "U"),
        ("0", "C"),
        ("0", "A"),
        ("G", "GU"),
        ("U", "UC"),
        ("C", "UC"),
        ("U", "GU"),
        ("C", "GC"),
        ("G", "GC"),
        ("GU", "GUC"),
        ("GC", "GUC"),
        ("UC", "GUC"),
        ("C", "CA"),
        ("A", "CA"),
        ("A", "GA"),
        ("CA", "GCA"),
        ("GA", "GCA"),
        ("GC", "GCA"),
        ("G", "GA"),
        ("A", "UA"),
        ("U", "UA"),
        ("CA", "UCA"),
        ("UC", "UCA"),
        ("UA", "UCA"),
        ("GA", "GUA"),
        ("UA", "GUA"),
        ("GU", "GUA"),
        ("GUA", "GUCA"),
        ("GCA", "GUCA"),
        ("UCA", "GUCA"),
        ("GUC", "GUCA")
    ]

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                x_rot += 1
            elif event.key == pygame.K_s:
                x_rot -= 1
            elif event.key == pygame.K_a:
                y_rot += 1
            elif event.key == pygame.K_d:
                y_rot -= 1
            elif event.key == pygame.K_q:
                z_rot -= 1
            elif event.key == pygame.K_e:
                z_rot += 1
            elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                zoom -= 1.1
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                zoom += 1.1
            elif event.key == pygame.K_SPACE:
                x_rot = 45
                y_rot = 35
                z_rot = 75
                z_trans = -20
                zoom = 1.0
            elif event.key == pygame.K_z:
                z_rot += 90
            elif event.key == pygame.K_x:
                z_rot -= 90

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    setup()

    # Draw edges
    edge_vertices = [(vertices[edge[0]], vertices[edge[1]]) for edge in edges]
    draw_edges(edge_vertices)

    # Draw vertices as color points
    glPointSize(10)
    glBegin(GL_POINTS)
    for vertex_name, vertex_coords in vertices.items():
        if vertex_name == "0":
            glColor3f(1.0, 0.0, 1.0)  # Purple
        elif vertex_name == "G":
            glColor3f(0.0, 0.0, 1.0)  # Blue 
        elif vertex_name == "U":
            glColor3f(0.0, 1.0, 0.0)  # Green
        elif vertex_name == "C":
            glColor3f(1.0, 1.0, 0.0)  # Yellow
        elif vertex_name == "A":
            glColor3f(1.0, 0.0, 0.0)  # Red
        elif vertex_name == "GU":
            glColor3f(1.0, 1.0, 1.0)  # White
        elif vertex_name == "UC":
            glColor3f(1.0, 1.0, 1.0)  # White
        elif vertex_name == "GC":
            glColor3f(1.0, 1.0, 1.0)  # White
        elif vertex_name == "GUC":
            glColor3f(1.0, 1.0, 1.0)  # White
        elif vertex_name == "CA":
            glColor3f(1.0, 1.0, 1.0)  # White
        elif vertex_name == "GA":
            glColor3f(1.0, 1.0, 1.0)  # White
        elif vertex_name == "GCA":
            glColor3f(1.0, 1.0, 1.0)  # White
        elif vertex_name == "UA":
            glColor3f(1.0, 1.0, 1.0)  # White
        elif vertex_name == "UCA":
            glColor3f(1.0, 1.0, 1.0)  # White
        elif vertex_name == "GUA":
            glColor3f(1.0, 1.0, 1.0)  # White
        elif vertex_name == "GUCA":
            glColor3f(1.0, 1.0, 1.0)  # White

        glVertex3fv(vertex_coords)
    glEnd()

    pygame.display.flip()
    pygame.time.wait(10)
    
