from __future__ import annotations
from constants import Biome
import random


class _BiomeNode:
    """
    """

    biome: Biome
    count: int
    repeat_weight: float
    weights: dict[Biome, _Weight]

    def __init__(self, biome: Biome) -> None:
        self.biome = biome
        self.count = 0
        self.repeat_weight = 0.0
        self.weights = {}


class _Weight:
    """
    """

    endpoints: set[_BiomeNode]
    weight: float

    def __init__(self, biome1: _BiomeNode, biome2: _BiomeNode) -> None:
        """
        """

        biome1.weights[biome2.biome] = self
        biome2.weights[biome1.biome] = self

        self.endpoints = {biome1, biome2}
        self.weight = 0.0

    def get_other_endpoint(self, biome: _BiomeNode) -> _BiomeNode:
        """
        """

        return (self.endpoints - {biome}).pop()


class BiomeGenerator:
    """
    """

    _biomes: dict[Biome, _BiomeNode]
    _current: Biome
    _streak: int

    def __init__(self) -> None:
        """
        """

        self._biomes = {}
        self._streak = 0
        self._current = Biome.ARID

        for biome1 in Biome:
            for biome2 in Biome:
                if biome1 != biome2:
                    self._add_weight(biome1, biome2)

    def update_traversal(self, biome: Biome) -> None:
        """
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
        """
        """

        biomes, weights = self._get_biomes_and_weights()

        return random.choices(biomes, weights, k=1)[0]

    def _get_biomes_and_weights(self) -> tuple[list[Biome], list[float]]:
        """
        """

        biome_node = self._biomes[self._current]

        biomes_so_far = [self._current]
        weights_so_far = [biome_node.repeat_weight]

        for biome in biome_node.weights:
            biomes_so_far.append(biome)
            weights_so_far.append(biome_node.weights[biome].weight)

        return (biomes_so_far, weights_so_far)

    def _update_weights(self) -> None:
        """
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
        """
        """

        self._biomes[biome] = _BiomeNode(biome)

    def _add_weight(self, biome1: Biome, biome2: Biome) -> None:
        """
        """

        if biome1 not in self._biomes:
            self._add_biome(biome1)
        if biome2 not in self._biomes:
            self._add_biome(biome2)

        node1 = self._biomes[biome1]
        node2 = self._biomes[biome2]

        _Weight(node1, node2)
