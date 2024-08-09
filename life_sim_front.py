"""
File: alife.py
Description: Animation of a simple life simulation

"""
import random as rnd
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import argparse
from life_simulation import Animal, Rabbit, Fox, Wolf, Field


SIZE = 250  # x/y dimensions of the field
WRAP = True  # When moving beyond the border, do we wrap around to the other size
R_OFFSPRING = 2  # Number of offspring a rabbit may have (between 1 and this number)
F_OFFSPRING = 1  # Fox offspring
W_OFFSPRING = 3  # Wolf offspring
GRASS_RATE = 0.1  # Probability of grass growing at any given location, e.g., 2%
INIT_RABBITS = 50  # Number of starting rabbits
INIT_FOXES = 200  # Starting foxes
INIT_WOLVES = 0  # Starting wolves
RABBIT_K = 1  # Number of generations foxes can live without food
FOX_K = 40  # Rabbit k
WOLF_K = 40  # Wolf k - wolves get hungry at double the rate of rabbits and foxes
FOX_MOVEMENT = 1  # Number of times a fox may move randomly per generation (between 1 and this number)
WOLF_MOVEMENT = 2  # Number of wolf movements possible
ENERGY_TRANSFER = True  # Determines if full prey is worth more energy than hungry prey
SPEED = 1  # Number of generations per frame
GENERATIONS = 1000  # Number of generations to simulate


def animate(i, field, im):
    for _ in range(SPEED):
        field.generation()
    im.set_array(field.array)
    plt.title("Generation: " + str(i * SPEED) +
              " Rabbits: " + str(len(field.rabbits)) +
              " Foxes: " + str(len(field.foxes)) +
              " Wolves: " + str(len(field.wolves)))
    return im


def main():
    # Create parser
    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument('-GR', '--GRASS_RATE', help='The rate of the grass being grown', type=float, default=0.1)
    parser.add_argument('-RK', '--RABBIT_K', help='Generations Rabbits can live without food', type=int, default=40)
    parser.add_argument('-FK', '--FOX_K', help='Generations Foxes can live without food', type=int, default=40)
    parser.add_argument('-WK', '--WOLF_K', help='Generations Wolfs can live without food', type=int, default=40)
    parser.add_argument('-SZ', '--SIZE', help='Dimensions of field', type=int, default=250)
    parser.add_argument('-IR', '--INIT_RABBITS', help='Number of starting rabbits', type=int, default=50)
    parser.add_argument('-IF', '--INIT_FOXES', help='Number of starting Foxes', type=int, default=200)
    parser.add_argument('-IW', '--INIT_WOLVES', help='Number of starting wolves', type=int, default=100)
    parser.add_argument('-WR', '--WRAP', help='Does movement wrap around', type=bool, default=True)

    # Parse command line
    args = parser.parse_args()

    # Update variables with values from args
    SIZE = args.SIZE
    WRAP = args.WRAP
    GRASS_RATE = args.GRASS_RATE
    INIT_RABBITS = args.INIT_RABBITS
    INIT_FOXES = args.INIT_FOXES
    INIT_WOLVES = args.INIT_WOLVES
    RABBIT_K = args.RABBIT_K
    FOX_K = args.FOX_K
    WOLF_K = args.WOLF_K

    # Create the ecosystem
    field = Field(size=SIZE, grass_rate=GRASS_RATE)

    # Initialize with some rabbits
    for _ in range(INIT_RABBITS):
        field.add_rabbit(Rabbit(size=SIZE, k=RABBIT_K, offspring=R_OFFSPRING, wrap=WRAP))

    for _ in range(INIT_FOXES):
        field.add_fox(Fox(size=SIZE, k=FOX_K, offspring=F_OFFSPRING,
                          movement=FOX_MOVEMENT, energy_transfer=ENERGY_TRANSFER, wrap=WRAP))

    for _ in range(INIT_WOLVES):
        field.add_wolf(Wolf(size=SIZE, k=WOLF_K, offspring=W_OFFSPRING,
                            movement=WOLF_MOVEMENT, energy_transfer=ENERGY_TRANSFER, wrap=WRAP))

    # Set up the image object
    field.get_array()
    array = field.array

    custom_colors = ['tan', 'green', 'lightblue', 'blue', 'red', 'darkred', 'gray']
    custom_cmap = colors.ListedColormap(custom_colors)

    fig = plt.figure(figsize=(10, 10))
    im = plt.imshow(array, cmap=custom_cmap, aspect='auto', vmin=0, vmax=6)
    anim = animation.FuncAnimation(fig, animate, fargs=(field, im), frames=1000 // SPEED, interval=1, repeat=False)
    plt.show()

    field.plot_animals()


if __name__ == '__main__':
    main()
