# -*- coding: utf-8 -*-
#  Copyright (c) 2020. Distributed under the terms of the MIT License.

import pytest
from pymatgen.util.string import latexify

from pydefect.analyzer.defect_energy import DefectEnergy
from pydefect.analyzer.defect_energy_plotter import DefectEnergyPlotter, \
    DefectEnergiesMplSettings
from pydefect.defaults import defaults


def test_defect_energies_mpl_settings():
    mpl_defaults = DefectEnergiesMplSettings()
    assert next(mpl_defaults.colors) == next(defaults.defect_energy_colors)

    mpl_defaults = DefectEnergiesMplSettings(colors=["black"])
    assert next(mpl_defaults.colors) == "black"


@pytest.fixture
def defect_energies():
    va_o = DefectEnergy(name="Va_O1", charges=[0, 1, 2], energies=[6, 3, -4])
    va_mg = DefectEnergy(name="Va_Mg1", charges=[-2, -1, 0], energies=[6, 3, 1])
    mg_i = DefectEnergy(name="Mg_i1", charges=[1], energies=[5])

    return DefectEnergyPlotter(
        title=latexify("MgAl2O4"),
        defect_energies=[va_o, va_mg, mg_i],
        vbm=1.5, cbm=5.5, supercell_vbm=1.0, supercell_cbm=6.0)


def test_defect_energies_actual_plot(defect_energies):
    defect_energies.construct_plot()
    defect_energies.plt.show()


"""
TODO
- Show all energies with thinner lines.
- show_transition_levels

- Add labels with optimize positions
https://github.com/cphyc/matplotlib-label-lines
https://github.com/Phlya/adjustText

- Add boundary points with open circles for shallow defects.
DONE
"""