#!/usr/bin/env python

"""
These are the steps to generate a fractal according to
Cartwright & Whitworth (2004):

1) Place node at the center of a cube.

2) Divide cube into ndiv**3 subcubes and place child nodes at the
   centres of these subcubes with probability ndiv**(FD-3).

3) Delete the parent node which was created at 1) if not all subcubes
   from 2) have a child node.

4) repeat steps 1,2,3 for the child nodes, until the system is
   sufficiently large.
"""

import numpy

class FractalCluster(object):
    def __init__(self, nstars, fdim, ndiv=2, dim=3):
        self.nstars = nstars
        self.fdim = fdim
        self.ndiv = ndiv
        self.dim = dim
        self.nsubs = ndiv**dim
        self.probability = ndiv**(fdim-dim)
        self.mkfractal()
        self.positions = self.get_positions()

    def mkfractal(self):

        self.tree = Node(None, 1)
        self.size = 1
        self.generations = 0
        last_generation = [self.tree]

        #add generations till sufficient
        while self.size < 2*self.nstars:
            self.generations += 1
            next_generation = []

            for parent in last_generation:
                new_children = self.add_children(parent)
                next_generation.extend([c for c in new_children if c.value == 1 ])
                values = [c.value for c in new_children]
                nr_children = sum(values)
                self.size += nr_children

                if nr_children < self.nsubs:
                    parent.value = 0
                    self.size -= 1

            last_generation = next_generation

            if len(last_generation) == 0:
                print('No descendants, redrawing fractal')
                self.mkfractal()


    def add_children(self, parent):
        """
        Adds children to parent node with maturation probability p.
        """
        sample = numpy.random.random(self.nsubs)
        bools = sample < self.probability
        children = [Node(parent, 1) if b else Node(parent, 0) for b in bools]
        parent.children = children
        return children

    def tree_to_nodes(self, node, path, index):
        nextpath = path + [index]

        if node.value == 1:
            self.nodes.append(nextpath)

        for i, n in enumerate(node.children):
            self.tree_to_nodes(n, nextpath, i)

    def get_positions(self):
        self.nodes = []
        self.tree_to_nodes(self.tree, self.nodes, 0)

        sides = [1.0/(self.ndiv**i) for i in range(self.generations)]
        centers = [self.get_centers(s) for s in sides]

        # tuple -> ndarray
        def node_to_point(node, centers):
            point = numpy.zeros(self.dim)
            for generation, nr in enumerate(node[1:]):
                indices = self.nr_to_indices(nr)
                p = numpy.array([centers[generation][index] for index in indices])
                point = point + p
            return point

        pos = numpy.array([node_to_point(n, centers) for n in self.nodes])*2

        #Take a subset from points
        selection = numpy.random.choice(len(pos), size=self.nstars)
        pos = pos.take(selection, axis=0)
        return pos


    def get_centers(self, side):
        """
        >>> get_centers(1, ndiv=2)
        array([-0.25,  0.25])
        >>> get_centers(1, ndiv=3)
        array([-0.33333333,  0.        ,  0.33333333])
        >>> get_centers(1, ndiv=4)
        array([-0.375, -0.125,  0.125,  0.375])

        Illustrated example with ndiv=3
        -------------------------------

        -side/2       0         +side/2

          |           |           |
          |           |           |
          v           v           v

          -------------------------
          |   |   |   |   |   |   |
          |   c   |   c   |   c   |
          |   |   |   |   |   |   |
          -------------------------
              ^       ^       ^
              |       |       |
              |       |       |
             [0]     [1]     [2]  <--- centers

        """
        assert self.ndiv > 1
        arr = numpy.linspace(-side/2.0, side/2.0, 2*self.ndiv + 1)
        centers = arr[1::2] #slice of uneven indices
        return centers

    # int int int -> (ints)
    def nr_to_indices(self, nr):
        indices = []
        subspace = self.dim
        while subspace > 0:
            subspace -= 1
            q, rem = divmod(nr, self.ndiv**subspace)
            indices.append(q)
            nr = rem
        return indices

class Node(object):
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value
        self.children = []

