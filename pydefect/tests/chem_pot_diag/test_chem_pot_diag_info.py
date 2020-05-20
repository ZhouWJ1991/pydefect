# -*- coding: utf-8 -*-
#  Copyright (c) 2020. Distributed under the terms of the MIT License.

from pymatgen import Composition, Element

from pydefect.chem_pot_diag.chem_pot_diag_info import ChemPotDiagInfo

# When same keys are inserted, only the latter one is accepted.
energies = {Composition("H"): 0.0,
            Composition("O"): 0.5,
            Composition("O"): 1.0,
            Composition("H2O"): -2.0}


def test_chem_pot_diag_info():
    cpd_info = ChemPotDiagInfo(energies)
    assert cpd_info.vertex_elements == [Element("H"), Element("O")]
    assert cpd_info.offset_to_abs == [0.0, 1.0]
    assert cpd_info.rel_energies[Composition("H2O")] == (-2.0 - 1.0) / 3
    assert cpd_info.vertex_coords == [[-0.5, 0.0], [0.0, -1.0]]

"""
TODO
- Return the formation energy of a compound
- Return the absolute energy of a compound
- 

DONE
"""