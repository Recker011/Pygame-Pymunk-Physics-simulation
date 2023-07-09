# Pygame Pymunk Simulation

This is a simple simulation using Pygame and Pymunk. The program creates a simulation of nodes connected by strings, with the ability to reset the simulation, spawn new nodes, and drag nodes around with the mouse.

## About

This program uses Pygame to create a graphical user interface and Pymunk to simulate physics. The simulation consists of nodes, which are represented as circles, connected by strings, which are represented as lines. The nodes are affected by gravity and can be dragged around with the mouse. The strings connect the nodes and apply tension to keep them at a fixed distance from each other. The simulation can be reset to its initial state, and new nodes can be spawned at random positions.

## Requirements

- Python 3.x
- Pygame
- Pymunk

## Installation

1. Install Python 3.x from [python.org](https://www.python.org/)
2. Install Pygame and Pymunk using pip:

```
pip install pygame pymunk
```

## Usage

1. Run the program using Python:

```
python <filename>.py
```

2. Use the left mouse button to drag nodes around.
3. Use the right mouse button to connect two nodes with a string.
4. Click the "Reset" button to reset the simulation.
5. Click the "Spawn" button to spawn a new node at a random position.
