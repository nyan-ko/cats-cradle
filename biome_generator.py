from __future__ import annotations
from constants import Biome
import random


class _BiomeNode:
    """ Representation of the biome of an individual scenario within a quest.

    Instance Attributes:
        - biome: the Biome associated with the given node
        - count: the number of times the user has encountered a given biome
        - repeat_weight: the weight associated with the node, to see if the biome should be swapped for another or not
        - weights: a mapping of each biome and their associated weights

    Representation Invariants:
        - 0.0 <= self.repeat_weights <= 1.0
    """

    biome: Biome
    count: int
    repeat_weight: float
    weights: dict[Biome, _Weight]

    def __init__(self, biome: Biome) -> None:
        """ Initializes a new node with the associated biome.
        """
        self.biome = biome
        self.count = 0
        self.repeat_weight = 0.0
        self.weights = {}


class _Weight:
    """ Representation of the edge between two _BiomeNodes, with an associated weight value for the chance of swapping
    to a new biome.

    Instance Attributes:
        - endpoints: a collection of _BiomeNodes that would be the associated biomes with the given weight
        - weight: the value associated with the weighting between the two given biomes

    Representation Invariants:
        - len(self.endpoints) == 2
        - 0.0 <= self.weight <= 1.0
    """

    endpoints: set[_BiomeNode]
    weight: float

    def __init__(self, biome1: _BiomeNode, biome2: _BiomeNode) -> None:
        """ Initializes the connection between the two given biomes and weight.
        """

        biome1.weights[biome2.biome] = self
        biome2.weights[biome1.biome] = self

        self.endpoints = {biome1, biome2}
        self.weight = 0.0

    def get_other_endpoint(self, biome: _BiomeNode) -> _BiomeNode:
        """ Returns the opposite endpoint that is not the given _BiomeNode.
        """

        return (self.endpoints - {biome}).pop()


class BiomeGenerator:
    """ Representation of the connections between all the Biomes in a given quest line.

    Instance Attributes:
        - _biomes: a private attribute for the mapping of a Biome to its respective _BiomeNodes
        - _current: a private attribute for the current Biome
        - _streak: a private attribute for the number of consecutive times a user has been in a given Biome

    Representation Invariants:
        - self._streak >= 0
    """

    _biomes: dict[Biome, _BiomeNode]
    _current: Biome
    _streak: int

    def __init__(self) -> None:
        """ Initializes the biomes and connections between each of them.
        """

        self._biomes = {}
        self._streak = 0
        self._current = Biome.ARID

        for biome1 in Biome:
            for biome2 in Biome:
                if biome1 != biome2:
                    self._add_weight(biome1, biome2)

    def update_traversal(self, biome: Biome) -> None:
        """ Checks which Biome the user is currently at, and updates the streak and weights accordingly for the Biome.
        """

        if biome == self._current:
            self._streak += 1
        else:
            self._current = biome
            self._streak = 1

        biome_node = self._biomes[biome]
        biome_node.count += 1

        self._update_weights()

    def get_next_biome(self) -> Biome:
        """ Returns the new Biome for the next situation, based on the previous biomes and associated weights.
        """

        biomes, weights = self._get_biomes_and_weights()

        return random.choices(biomes, weights, k=1)[0]

    def _get_biomes_and_weights(self) -> tuple[list[Biome], list[float]]:
        """ Return a tuple of the biomes the user has encountered and the weights associated with each biome.

        Preconditions:
            - self._current in self._biomes
        """

        biome_node = self._biomes[self._current]

        biomes_so_far = [self._current]
        weights_so_far = [biome_node.repeat_weight]

        for biome in biome_node.weights:
            biomes_so_far.append(biome)
            weights_so_far.append(biome_node.weights[biome].weight)

        return (biomes_so_far, weights_so_far)

    def _update_weights(self) -> None:
        """ Update the weights for the current biome, based on the amount of consecutive times the user has been in a
        given Biome.

        Preconditions:
            - self._current in self._biomes
        """

        REPEAT_THRESHOLD = 5
        DECAY_MULTIPLIER = 2

        biome_node = self._biomes[self._current]

        if self._streak <= REPEAT_THRESHOLD:
            biome_node.repeat_weight = 1.0 - (0.1 * self._streak)
        else:
            biome_node.repeat_weight = max(0.5 - (0.1 * (self._streak - REPEAT_THRESHOLD) * DECAY_MULTIPLIER), 0.0)

        remaining_weight = 1.0 - biome_node.repeat_weight
        total_weight = sum(1 / (self._biomes[biome].count + 1) for biome in biome_node.weights)

        for biome in biome_node.weights:
            neighbour = self._biomes[biome]
            neighbour_weight = ((neighbour.count + 1) / total_weight) * remaining_weight
            biome_node.weights[biome].weight = neighbour_weight

    def _add_biome(self, biome: Biome) -> None:
        """ Add a given biome to the pre-existing mapping of biomes.
        """

        self._biomes[biome] = _BiomeNode(biome)

    def _add_weight(self, biome1: Biome, biome2: Biome) -> None:
        """ Adds the given Biomes to the mapping if they are not already in it, before connecting the two and giving
        them an associated weight.
        """

        if biome1 not in self._biomes:
            self._add_biome(biome1)
        if biome2 not in self._biomes:
            self._add_biome(biome2)

        node1 = self._biomes[biome1]
        node2 = self._biomes[biome2]

        _Weight(node1, node2)
