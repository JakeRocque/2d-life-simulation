"""
File: life_simulation.py
Description: A simple artificial life simulation.

"""
import random as rnd
import copy
import numpy as np
import matplotlib.pyplot as plt


class Animal:
    """ An animal is a rabbit or fox that has a certain amount of energy,
    can reproduce, and must eat to survive """

    def __init__(self, size=100, energy=None, wrap=False):

        # randomly generate x and y position for a certain size
        self.x = rnd.randrange(0, size)
        self.y = rnd.randrange(0, size)
        self.size = size

        self.energy = energy

        self.eaten = False  # used to determine if animal will reproduce

        self.wrap = wrap

    def hunger(self):
        """ Hunger depletes by 1 every generation """
        self.energy += -1

    def move(self):
        """ Animals move randomly with option to enable movement to wrap around the edges of the field """
        if self.wrap:
            self.x = (self.x + rnd.choice([-1, 0, 1])) % self.size
            self.y = (self.y + rnd.choice([-1, 0, 1])) % self.size
        else:
            self.x = min(self.size - 1, max(0, (self.x + rnd.choice([-1, 0, 1]))))
            self.y = min(self.size - 1, max(0, (self.y + rnd.choice([-1, 0, 1]))))


class Rabbit(Animal):
    def __init__(self, size=100, k=1, offspring=2, wrap=False):
        super().__init__(size, energy=k, wrap=wrap)

        self.animal = 'rabbit'

        # Set k, number of generations animal can survive without food
        self.k = k

        self.offspring = offspring

        self.energy = self.k

    def reproduce(self):
        """ Rabbits reproduce by returning a deep copy of themselves and have energy lowered """
        self.energy = 0

        self.eaten = False

        return copy.deepcopy(self)

    def eat_grass(self, amount):
        """ Eating grass adds 0 or 1 energy depending on if grass is grown
        and if grass is grown change eaten to True """
        self.energy += amount
        self.energy = min(self.energy, self.k)  # ensure energy does not exceed limit

        if amount != 0:
            self.eaten = True


class Fox(Animal):
    """ Initialize fox class """
    def __init__(self, size=100, k=20, movement=1, offspring=1, energy_transfer=True, wrap=False):
        super().__init__(size, energy=k, wrap=wrap)

        self.animal = 'fox'

        self.k = k
        self.movement = movement
        self.energy_transfer = energy_transfer

        self.offspring = offspring

        self.energy = self.k

    def reproduce(self):
        """ Foxes reproduce by returning a deep copy of themselves and have energy lowered """
        self.energy = self.k // 2

        self.eaten = False

        return copy.deepcopy(self)

    def eat_rabbit(self, amount):
        """ Eating a rabbit adds 0 or 10 energy depending on if grass is grown
        and if grass is grown change eaten to True """
        if self.energy_transfer:
            if amount == 3:  # Fat rabbit
                energy_gain = 12
            elif amount == 2:  # Skinny rabbit
                energy_gain = 6
            else:
                energy_gain = 0  # No energy gain if the rabbit is not present
        else:
            if amount != 0:
                energy_gain = 10  # if energy transfer is off, all rabbits give 10 energy
            else:
                energy_gain = 0  # No energy gain if the rabbit is not present

        self.energy += energy_gain

        if energy_gain != 0:
            self.eaten = True

        self.energy = min(self.energy, self.k)  # ensure energy does not exceed limit


class Wolf(Animal):
    """ Initialize wolf class """
    def __init__(self, size=100, k=30, movement=1, offspring=1, energy_transfer=True, wrap=False):
        super().__init__(size, energy=k, wrap=wrap)

        self.animal = 'wolf'

        self.k = k
        self.movement = movement
        self.energy_transfer = energy_transfer

        self.offspring = offspring

        self.energy = self.k

    def reproduce(self):
        """ Foxes reproduce by returning a deep copy of themselves and have energy lowered """
        self.energy = self.k // 2

        self.eaten = False

        return copy.deepcopy(self)

    def eat_rabbit(self, amount):
        """ Eating a rabbit adds 0 or 10 energy depending on if grass is grown
        and if grass is grown change eaten to True """
        if self.energy_transfer:
            if amount == 3:  # Fat rabbit
                energy_gain = 12
            elif amount == 2:  # Skinny rabbit
                energy_gain = 6
            else:
                energy_gain = 0  # No energy gain if the rabbit is not present
        else:
            if amount != 0:
                energy_gain = 10  # if energy transfer is off, all rabbits give 10 energy
            else:
                energy_gain = 0  # No energy gain if the rabbit is not present

        self.energy += energy_gain

        if energy_gain != 0:
            self.eaten = True

        self.energy = min(self.energy, self.k)  # ensure energy does not exceed limit

    def eat_fox(self, amount):
        """ Eating a rabbit adds 0 or 10 energy depending on if grass is grown
        and if grass is grown change eaten to True """
        if self.energy_transfer:
            if amount == 5:  # Fat fox
                energy_gain = 20
            elif amount == 4:  # Skinny fox
                energy_gain = 10
            else:
                energy_gain = 0  # No energy gain if the rabbit is not present
        else:
            if amount != 0:
                energy_gain = 15  # if energy transfer is off, all rabbits give 10 energy
            else:
                energy_gain = 0  # No energy gain if the rabbit is not present

        self.energy += energy_gain

        self.energy = min(self.energy, self.k)  # ensure energy does not exceed limit

        if energy_gain != 0:
            self.eaten = True


class Field:
    """ A field is a patch of grass with a specified number of
    rabbits looking for grass and foxes hunting rabbits """

    def __init__(self, size=100, grass_rate=0.04):

        self.generation_num = 0
        self.rabbit_count = []
        self.fox_count = []
        self.wolf_count = []

        self.rabbit_locs = None  # array for rabbit locations
        self.fox_locs = None
        self.array = None  # array for all animal locations for final visualization

        self.rabbits = []
        self.foxes = []
        self.wolves = []

        self.field = np.ones(shape=(size, size), dtype=int)
        self.size = size

        self.grass_rate = grass_rate  # set random rate that grass grows on dirt

    def add_rabbit(self, rabbit):
        self.rabbits.append(rabbit)

    def add_fox(self, fox):
        self.foxes.append(fox)

    def add_wolf(self, wolf):
        self.wolves.append(wolf)

    def move(self):
        for r in self.rabbits:
            r.move()

        for f in self.foxes:
            for _ in range(rnd.randint(1, f.movement)):
                f.move()
                f.hunger()

        for w in self.wolves:
            for _ in range(rnd.randint(1, w.movement)):
                w.move()
                w.hunger()

    def eat(self):
        """ All rabbits try to eat grass and foxes try to eat rabbits at their current location """
        self.get_array()  # update rabbit and fox locations

        # if grass is present at a rabbit's location, eat the value (1) and set it to 0
        for r in self.rabbits:
            r.eat_grass(self.field[r.x, r.y])
            self.field[r.x, r.y] = 0

        # if grass is present at a rabbit's location, eat the value (2 * 5) and set it to 0
        for f in self.foxes:
            f.eat_rabbit(self.rabbit_locs[f.x, f.y])
            self.rabbit_locs[f.x, f.y] = 0

        for w in self.wolves:
            w.eat_rabbit(self.rabbit_locs[w.x, w.y])
            self.rabbit_locs[w.x, w.y] = 0

            w.eat_fox(self.fox_locs[w.x, w.y])
            self.fox_locs[w.x, w.y] = 0

    def survive(self):
        """ Rabbits and foxes that have 0 energy die
        Otherwise they hunger and lose 1 energy """
        self.rabbits = [r for r in self.rabbits if r.energy > 0]
        self.foxes = [f for f in self.foxes if f.energy > 0]
        self.wolves = [w for w in self.wolves if w.energy > 0]

        for r in self.rabbits:
            r.hunger()

        for f in self.foxes:
            f.hunger()

        for w in self.wolves:
            w.hunger()
            w.hunger()

    def reproduce(self):
        """ If an animal has eaten in the last generation
        animals will reproduce based on their specified number of offspring"""
        born_r = []
        for r in self.rabbits:
            if r.eaten:
                for _ in range(rnd.randint(1, r.offspring)):
                    born_r.append(r.reproduce())
        self.rabbits += born_r

        born_f = []
        for f in self.foxes:
            if f.eaten:
                for _ in range(rnd.randint(1, f.offspring)):
                    born_f.append(f.reproduce())
        self.foxes += born_f

        born_w = []
        for w in self.wolves:
            if w.eaten and w.energy > w.k // 6:
                for _ in range(rnd.randint(1, w.offspring)):
                    born_w.append(w.reproduce())
        self.wolves += born_w

    def grow(self):
        """ Grow grass randomly based on grass growth rate """
        grow_loc = (np.random.rand(self.size, self.size) < self.grass_rate) * 1
        self.field = np.maximum(self.field, grow_loc)

    def generation(self):
        """ Run one generation of animal actions """
        self.move()
        self.eat()
        self.get_array()
        self.survive()
        self.reproduce()
        self.grow()

        self.generation_num += 1

        self.rabbit_count.append(len(self.rabbits))
        self.fox_count.append(len(self.foxes))
        self.wolf_count.append(len(self.wolves))

    def get_array(self):
        """ Return an array representing grass/dirt, rabbits, and foxes
        with priority foxes > rabbits > grass/dirt """
        fat_rabbits = []
        skinny_rabbits = []
        for r in self.rabbits:
            if r.eaten:
                fat_rabbits.append((r.x, r.y))
            else:
                skinny_rabbits.append((r.x, r.y))

        # Initialize the rabbit_locs array with zeros
        rabbit_locs = np.zeros((self.size, self.size), dtype=int)

        # Fill in the array with 2s for skinny rabbits and 3s for fat rabbits
        if skinny_rabbits:
            rabbit_locs[tuple(np.array(skinny_rabbits).T)] = 2

        if fat_rabbits:
            rabbit_locs[tuple(np.array(fat_rabbits).T)] = 3

        fat_foxes = []
        skinny_foxes = []
        for f in self.foxes:
            if f.eaten:
                fat_foxes.append((f.x, f.y))
            else:
                skinny_foxes.append((f.x, f.y))

        # Initialize the rabbit_locs array with zeros
        fox_locs = np.zeros((self.size, self.size), dtype=int)

        # Fill in the array with 2s for skinny rabbits and 3s for fat rabbits
        if skinny_foxes:
            fox_locs[tuple(np.array(skinny_foxes).T)] = 4

        if fat_foxes:
            fox_locs[tuple(np.array(fat_foxes).T)] = 5

        wolves = [(w.x, w.y) for w in self.wolves]
        wolf_locs = np.zeros((self.size, self.size), dtype=int)
        if wolves:
            fox_locs[tuple(np.array(wolves).T)] = 6

        total = np.maximum(wolf_locs, np.maximum(fox_locs, np.maximum(self.field, rabbit_locs)))

        self.rabbit_locs = rabbit_locs
        self.fox_locs = fox_locs
        self.array = total

    def plot_animals(self):
        plt.plot(range(self.generation_num), self.rabbit_count, color='blue', label='Rabbits')
        plt.plot(range(self.generation_num), self.fox_count, color='red', label='Foxes')
        plt.plot(range(self.generation_num), self.wolf_count, color='gray', label='Wolves')

        plt.title('Animal Count Per Generation')
        plt.xlabel('Generation')
        plt.ylabel('Animal Count')
        plt.legend()

        plt.grid(True, linestyle='--', alpha=0.5)

        plt.legend(fontsize=12)

        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)

        plt.gcf().set_facecolor('#e0f3db')
        plt.gca().set_facecolor('lightgray')

        plt.gca().spines['bottom'].set_color('darkgray')
        plt.gca().spines['left'].set_color('darkgray')
        plt.gca().spines['top'].set_color('darkgray')
        plt.gca().spines['right'].set_color('darkgray')

        plt.show()
