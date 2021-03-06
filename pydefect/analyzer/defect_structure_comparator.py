# -*- coding: utf-8 -*-
#  Copyright (c) 2020 Kumagai group.
import numpy as np
from pydefect.util.structure_tools import Distances
from pymatgen import IStructure


class DefectStructureComparator:
    def __init__(self,
                 defect_structure: IStructure,
                 perfect_structure: IStructure,
                 same_distance_criterion: float = None):
        """
        Atoms in the final structure are shifted such that the farthest atom
        from the defect is placed at the same place with that in the perfect
        supercell.
        """
        self._defect_structure = defect_structure
        self._perfect_structure = perfect_structure
        self.same_distance_criterion = same_distance_criterion
        self.p_to_d = self.make_p_to_d()
        self.d_to_p = self.make_d_to_p()

    @property
    def atom_mapping(self):
        return {d: p for d, p in enumerate(self.d_to_p)
                if d not in self.inserted_indices}

    def make_p_to_d(self):
        result = []
        for site in self._perfect_structure:
            distances = Distances(self._defect_structure,
                                  site.frac_coords,
                                  self.same_distance_criterion)
            result.append(distances.atom_idx_at_center(specie=site.specie))
        return result

    def make_d_to_p(self):
        result = []
        for site in self._defect_structure:
            distances = Distances(self._perfect_structure,
                                  site.frac_coords,
                                  self.same_distance_criterion)
            result.append(distances.atom_idx_at_center(specie=site.specie))
        return result

    @property
    def vacant_indices(self):
        result = []
        for p, d in enumerate(self.p_to_d):
            try:
                if self.d_to_p[d] != p:
                    result.append(p)
            except (IndexError, TypeError):
                result.append(p)
        return sorted(result)

    @property
    def inserted_indices(self):
        result = []
        for d, p in enumerate(self.d_to_p):
            try:
                if self.p_to_d[p] != d:
                    result.append(d)
            except (IndexError, TypeError):
                result.append(d)
        return sorted(result)

    @property
    def defect_center_coord(self):
        coords = []
        for v in self.vacant_indices:
            coords.append(self._perfect_structure[v].frac_coords)
        for i in self.inserted_indices:
            coords.append(self._defect_structure[i].frac_coords)

        lattice = self._perfect_structure.lattice
        repr_coords = coords[0]
        translated_coords = [list(repr_coords)]
        for c in coords[1:]:
            _, trans = lattice.get_distance_and_image(repr_coords, c)
            translated_coords.append([c[i] + trans[i] for i in range(3)])
        return np.average(translated_coords, axis=0) % 1

    def neighboring_atom_indices(self, cutoff_factor=None):
        distances = []
        for v in self.vacant_indices:
            distances.append(Distances(self._defect_structure,
                                       self._perfect_structure[v].frac_coords,
                                       self.same_distance_criterion))
        for i in self.inserted_indices:
            distances.append(Distances(self._defect_structure,
                                       self._defect_structure[i].frac_coords,
                                       self.same_distance_criterion))
        result = set()
        for d in distances:
            result.update(d.coordination(cutoff_factor=cutoff_factor)
                          .neighboring_atom_indices)
        return sorted(list(result))
