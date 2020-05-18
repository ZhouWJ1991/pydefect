# -*- coding: utf-8 -*-
#  Copyright (c) 2020. Distributed under the terms of the MIT License.

import pytest
from pymatgen import IStructure, Lattice

from pydefect.input_maker.defect_entry import DefectEntry
from pydefect.defaults import defaults
from pydefect.tests.helpers.assertion import assert_msonable

# "H" at [0.0, 0.0, 0.0] is removed here.
coords = \
    [[0.5, 0.5, 0.0], [0.5, 0.0, 0.5], [0.0, 0.5, 0.5],
     [0.0, 0.0, 0.5], [0.0, 0.5, 0.0], [0.5, 0.0, 0.0], [0.5, 0.5, 0.5]]
perturbed_coords = \
    [[0.5, 0.5, 0.0], [0.5, 0.0, 0.5], [0.0, 0.5, 0.5],
     [0.0, 0.0, 0.501], [0.0, 0.501, 0.0], [0.501, 0.0, 0.0], [0.5, 0.5, 0.5]]

rocksalt = IStructure(
    Lattice.cubic(10.0), ["H"] * 3 + ["He"] * 4, coords)
perturbed_rocksalt = IStructure(
    Lattice.cubic(10.0), ["H"] * 3 + ["He"] * 4, perturbed_coords)


@pytest.fixture
def defect_entry():
    return DefectEntry(name="Va_O1",
                       charge=1,
                       structure=rocksalt,
                       perturbed_structure=perturbed_rocksalt,
                       site_symmetry="m-3m")


def test_msonable(defect_entry):
    assert_msonable(defect_entry)


def test_hashable(defect_entry):
    d = {defect_entry: 1}


def test_perturbed_site_indices(defect_entry):
    assert defect_entry.perturbed_site_indices == [3, 4, 5]


"""
TODO
- Store basic info for a single input defect initial structure.
- create prior_info
- from structure
DONE
"""