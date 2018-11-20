#!/usr/bin/env python

# use stdin to process the environment
def buildEnv():
    colors = {0: 1}
    count = int(input())
    env = [[0]*(count+2)]
    for i in range(0, count):
        line = input()
        line = [int(i) if int(i) != 0 else None for i in line.split(' ') if i != '']
        line = [0] + line + [0]
        env += [line]
        for i in line:
            colors[i] = 1
    env += [[0]*(count+2)]
    return env, (len(colors)-1)

env, num_colors = buildEnv()
var_count = 0
def new_var():
    global var_count
    var_count += 1
    return var_count

class Tile():

    def __init__(self, defined_color=None):
        if defined_color != None:
            # endpoint
            self.vars = [new_var() for i in range(0, num_colors)]
            self.constraints = []
            self.color = defined_color
            # make clauses where each color is false if it isn't the valid color
            for i, var in enumerate(self.vars):
                self.constraints += [[var if i == defined_color else -var]]
        else:
            # colorless
            self.vars = [new_var() for i in range(0, num_colors)]
            self.constraints = []
            self.color = None

            # handle mutex constraint
            # add case where all true
            self.constraints += [[i for i in self.vars]]

            # n choose 2 permutation
            for i in range(0, len(self.vars)):
                for j in range(i+1, len(self.vars)):
                    # permute
                    self.constraints += [[-self.vars[i], -self.vars[j]]]
        return

    def add_constraint_endpoint(self, t1, t2, t3, t4):
        if self.color == 0:
            return
        else:
            # a SINGLE neighboring tile will have the same color as an endpoint tile
            self.constraints += [[t1.vars[self.color], t2.vars[self.color], t3.vars[self.color], t4.vars[self.color]],
                    [-t1.vars[self.color], -t2.vars[self.color]],
                    [-t1.vars[self.color], -t3.vars[self.color]],
                    [-t1.vars[self.color], -t4.vars[self.color]],
                    [-t2.vars[self.color], -t3.vars[self.color]],
                    [-t2.vars[self.color], -t4.vars[self.color]],
                    [-t3.vars[self.color], -t4.vars[self.color]]]
        return

    def add_constraint_point(self, t1, t2, t3, t4):
        # this tile can only have the same color as a single other or just colorless (just OR every clause with Colorless)
        for i in range(1, num_colors):
            self.constraints  += [    
                [-self.vars[i], t1.vars[i], t2.vars[i], t3.vars[i], t4.vars[i]],
                [-self.vars[i], t1.vars[i], t2.vars[i], t3.vars[i]],
                [-self.vars[i], t1.vars[i], t2.vars[i], t4.vars[i]],
                [-self.vars[i], t1.vars[i], t3.vars[i], t4.vars[i]],
                [-self.vars[i], t2.vars[i], t3.vars[i], t4.vars[i]],

                [-self.vars[i], -t1.vars[i], -t2.vars[i], -t3.vars[i]],
                [-self.vars[i], -t1.vars[i], -t2.vars[i], -t4.vars[i]],
                [-self.vars[i], -t1.vars[i], -t3.vars[i], -t4.vars[i]],
                [-self.vars[i], -t2.vars[i], -t3.vars[i], -t4.vars[i]],

                [-self.vars[i], -t1.vars[i], -t2.vars[i], -t3.vars[i], -t4.vars[i]]
            ]
        return

    def num_constraints(self):
        return len(self.constraints)

    def num_vars(self):
        return len(self.vars)

    def print_constraints(self):
        for clause in self.constraints:
            for variable in clause:
                print(variable, end=' ')
            print(0)
        return
tiles = env
for i, line in enumerate(env):
    for j, tile in enumerate(line):
        tiles[i][j] = Tile() if tile == None else Tile(tile)


for i in range(1, len(tiles)-1):
    for j in range(1, len(tiles)-1):
        if tiles[i][j].color == 0:
            pass
        elif tiles[i][j].color == None:
            tiles[i][j].add_constraint_point(tiles[i+1][j], tiles[i-1][j], tiles[i][j+1], tiles[i][j-1])
        else:
            tiles[i][j].add_constraint_endpoint(tiles[i+1][j], tiles[i-1][j], tiles[i][j+1], tiles[i][j-1])


# compute the number of clauses
num_constraints = 0
for i in range(0, len(tiles)):
    for j in range(0, len(tiles)):
        num_constraints += tiles[i][j].num_constraints()

# compute the number of variables
num_vars = 0
for i in range(0, len(tiles)):
    for j in range(0, len(tiles)):
        num_vars += tiles[i][j].num_vars()
print('c %d %d' % (num_colors, len(env)-2))
print('p cnf %d %d' % (num_vars, num_constraints))

# dump all constraints
for i in range(0, len(tiles)):
    for j in range(0, len(tiles)):
        tiles[i][j].print_constraints()
