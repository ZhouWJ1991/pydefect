# -*- coding: utf-8 -*-
#  Copyright (c) 2020. Distributed under the terms of the MIT License.

import pytest
from pymatgen import Element
from pydefect.input_maker.supercell_info import Site, SupercellInfo
from pydefect.tests.helpers.assertion import assert_msonable
from vise.util.structure_symmetrizer import StructureSymmetrizer


@pytest.fixture
def site():
    return Site(wyckoff_letter="a",
                site_symmetry="m3m",
                equivalent_atoms=[0, 1, 2, 3])


def test_site(site):
    assert_msonable(site)


@pytest.fixture
def supercell_info(ortho_conventional):
    sites = {"H1": Site(wyckoff_letter="a", site_symmetry="mmm",
                        equivalent_atoms=[0, 1, 2, 3]),
             "He1": Site(wyckoff_letter="b", site_symmetry="mmm",
                         equivalent_atoms=[4, 5, 6, 7])}
    return SupercellInfo(ortho_conventional,
                         "Fmmm",
                         [[1, 0, 0], [0, 1, 0], [0, 0, 1]], sites)

def test(ortho_conventional):
    print(StructureSymmetrizer(ortho_conventional).spglib_sym_data)



def test_supercell_info(supercell_info):
    assert_msonable(supercell_info)


def test_supercell_info_distances(supercell_info):
    coords = supercell_info.coords
    assert coords["H1"] == {"H": [3.91], "He": [2.5, 3.0, 3.5]}
    assert coords["He1"] == {"H": [2.5, 3.0, 3.5], "He": [3.91]}


def test_supercell_info_str(supercell_info):
    expected = """  Space group: Fm-3m

Transformation matrix: 1 0 0  0 1 0  0 0 1
Cell multiplicity: 1

   Irreducible element: H1
        Wyckoff letter: a
         Site symmetry: mmm
         Cutoff radius: 2.76
          Coordination: O: 2.12 2.12 2.12 2.12 2.12 2.12
      Equivalent atoms: 0..26
Fractional coordinates: 0.0000000  0.0000000  0.0000000
     Electronegativity: 1.31
       Oxidation state: 2

   Irreducible element: O1
        Wyckoff letter: b
         Site symmetry: m-3m
         Cutoff radius: 2.76
          Coordination: Mg: 2.12 2.12 2.12 2.12 2.12 2.12
      Equivalent atoms: 27..53
Fractional coordinates: 0.1666667  0.1666667  0.1666667
     Electronegativity: 3.44
       Oxidation state: -2
"""
    assert str(supercell_info) == expected


"""
TODO
- Add spacegroup to Supercell Info
- Implement print info
- Generate default defect.in

DONE
- Evaluate coords at Site
"""