# -*- coding: utf-8 -*-
#  Copyright (c) 2020. Distributed under the terms of the MIT License.
import numpy as np
import pytest
from pymatgen import Structure, IStructure, Lattice

from pydefect.analyzer.defect_structure_analyzer import \
    symmetrize_defect_structure, \
    DefectStructureAnalyzer


@pytest.fixture
def structure_analyzer():
    cu2o_perfect = IStructure(Lattice.cubic(5),
                              species=["Cu"] * 4 + ["O"] * 2,
                              coords=[[0.25, 0.25, 0.25],
                                      [0.25, 0.75, 0.75],
                                      [0.75, 0.75, 0.25],
                                      [0.75, 0.25, 0.75],
                                      [0, 0, 0],
                                      [0.5, 0.5, 0.5]])
    cu2o_defect = IStructure(Lattice.cubic(5),
                             species=["Cu"] * 3 + ["O"] * 2,
                             coords=[[0.25, 0.5, 0.5],
                                     [0.76, 0.73, 0.24],
                                     [0.75, 0.25, 0.73],
                                     [0.1, -0.1, 0],
                                     [0.5, 0.5, 0.5]])

    return DefectStructureAnalyzer(defective_structure=cu2o_defect,
                                   perfect_structure=cu2o_perfect)


def test_atom_mapping_to_perfect(structure_analyzer):
    assert structure_analyzer.atom_mapping == {1: 2, 2: 3, 3: 4, 4: 5}
    assert structure_analyzer.vacancy_indices == [0, 1]
    assert structure_analyzer.inserted_indices == [0]


def test_defect_structure_analyzer(structure_analyzer):
    expected = np.array([0.25, 0.5, 0.5])
    assert (structure_analyzer.defect_center_coord == expected).all()


def test_symmetrize_defect_structure():
    structure = Structure.from_str(fmt="POSCAR", input_string="""Mg4 O3
1.00000000000000
5 0 0
0 5 0
0 0 5
Mg   O
4     3
Direct
0.0051896248240553  0.9835077947659414  0.9945137498637422
0.0047282952713914  0.4827940046010823  0.4942929782542009
0.5040349492352973  0.9821499237428384  0.4944941755970405
0.5058945352747628  0.4828206016032297  0.9940420309511140
0.5045613848356609  0.4811103128264023  0.4933877756337353
0.0013796816599694  0.9829379087234287  0.4953360299212051
0.0083465288988691  0.4848714537370853  0.9941122597789658""")
    actual = symmetrize_defect_structure(structure=structure,
                                         anchor_atom_idx=1,
                                         anchor_atom_coord=[0.0, 0.5, 0.5])
    expected = Structure.from_str(fmt="POSCAR", input_string="""Mg4 O3
1.00000000000000
5 0 0
0 5 0
0 0 5
Mg   O
4     3
Direct
0.0 0.0 0.0
0.0 0.5 0.5
0.5 0.0 0.5
0.5 0.5 0.0
0.5 0.5 0.5
0.0 0.0 0.5
0.0 0.5 0.0""")
    assert actual == expected


"""
TODO
- Add anchor_atom_index

DONE
"""