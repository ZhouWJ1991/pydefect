# -*- coding: utf-8 -*-
#  Copyright (c) 2020. Distributed under the terms of the MIT License.
from copy import deepcopy
from dataclasses import dataclass
from itertools import groupby
from typing import List

import numpy as np
from pymatgen import Element
from scipy.spatial import HalfspaceIntersection


@dataclass
class SingleDefectEnergy:
    name: str
    charge: int
    energy: float
    correction: float


@dataclass
class DefectEnergy:
    name: str
    charges: List[int]
    energies: List[float]
    corrections: List[float]

    def cross_points(self, ef_min, ef_max, base_ef=0.0):
        large_minus_number = -1e4
        half_spaces = []
        for charge, energy, correction in zip(self.charges, self.energies, self.corrections):
            corrected_energy = energy + correction
            half_spaces.append([-charge, 1, -corrected_energy])

        half_spaces.append([-1, 0, ef_min])
        half_spaces.append([1, 0, -ef_max])
        half_spaces.append([0, -1, large_minus_number])

        feasible_point = np.array([(ef_min + ef_max) / 2, -1e3])

        hs = HalfspaceIntersection(np.array(half_spaces), feasible_point)
        boundary_points = []
        inner_cross_points = []
        for intersection in hs.intersections:
            x, y = np.round(intersection, 8)
            if ef_min + 0.001 < x < ef_max - 0.001:
                inner_cross_points.append([x - base_ef, y])
            elif y > large_minus_number + 1:
                boundary_points.append([x - base_ef, y])

        return CrossPoints(inner_cross_points, boundary_points)

    def __str__(self):
        lines = []
        for charge, energy, correction in zip(self.charges, self.energies, self.corrections):
            lines.append(f"{self.name:>10} {charge:>4} {energy:12.4f} {correction:12.4f}")
        return "\n".join(lines)


@dataclass
class CrossPoints:
    inner_cross_points: List[List[float]]
    boundary_points: List[List[float]]

    @property
    def all_sorted_points(self):
        return sorted(self.boundary_points + self.inner_cross_points,
                      key=lambda v: v[0])

    @property
    def t_all_sorted_points(self):
        return np.transpose(np.array(self.all_sorted_points)).tolist()

    @property
    def t_inner_cross_points(self):
        return np.transpose(np.array(self.inner_cross_points)).tolist()

    @property
    def t_boundary_points(self):
        return np.transpose(np.array(self.boundary_points)).tolist()

    @property
    def charges(self):
        result = []
        for i, j in zip(self.all_sorted_points[:-1], self.all_sorted_points[1:]):
            dx = j[0] - i[0]
            dy = j[1] - i[1]
            result.append(int(round(dy / dx)))
        return result

    @property
    def charge_list(self):
        charges = [None] + self.charges + [None]
        return list(zip(charges[:-1], charges[1:]))

    @property
    def annotated_charge_positions(self):
        result = {}
        for ((x1, y1), (x2, y2)), charge \
                in zip(zip(self.all_sorted_points[:-1],
                           self.all_sorted_points[1:]),
                       self.charges):
            result[charge] = [(x1 + x2) / 2, (y1 + y2) / 2]
        return result

    def __str__(self):
        lines = []
        for point in self.all_sorted_points:
            lines.append(f"{point[0]:12.4f} {point[1]:12.4f}")
        return "\n".join(lines)


def make_defect_energies(single_energies: List[SingleDefectEnergy]
                         ) -> List[DefectEnergy]:
    sorted_energies = sorted(single_energies, key=lambda x: x.name)
    result = []
    for _, grouped_energies in groupby(sorted_energies, lambda x: x.name):
        charges = []
        energies = []
        corrections = []
        for single_energy in grouped_energies:
            charges.append(single_energy.charge)
            energies.append(single_energy.energy)
            corrections.append(single_energy.correction)
        result.append(DefectEnergy(single_energy.name, charges, energies, corrections))
    return result


def remove_digits(name):
    return ''.join([i for i in name if not i.isdigit()])


def only_digits(name):
    return ''.join([i for i in name if i.isdigit()])


elements = [str(e) for e in Element]


def defect_mpl_name(name):
    in_name, out_name = name.split("_")
    if in_name in elements:
        in_name = "{\\rm " + in_name + "}"
    elif in_name == "Va":
        in_name = "V"

    r_out_name = remove_digits(out_name)
    if r_out_name in elements:
        out_name = "{{\\rm " + r_out_name + "}" + only_digits(out_name) + "}"
    else:
        out_name = "{" + out_name + "}"

    return f"${in_name}_{out_name}$"


def sanitize_defect_energies_for_plot(defect_energies: List[DefectEnergy]):
    result = []
    out_names = [e.name.split("_")[1] for e in defect_energies]

    for e in defect_energies:
        ee = deepcopy(e)
        in_name, out_name = e.name.split("_")
        r_out_name = remove_digits(out_name)
        out_name = r_out_name if f"{r_out_name}2" not in out_names else out_name
        ee.name = defect_mpl_name("_".join([in_name, out_name]))
        result.append(ee)

    return result


def slide_energy(defect_energies: List[DefectEnergy], base_level: float):
    result = []
    for e in defect_energies:
        ee = deepcopy(e)
        ee.energies = [e + base_level * c for e, c in zip(e.energies, e.charges)]
        result.append(ee)
    return result
