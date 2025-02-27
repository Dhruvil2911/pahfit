from astropy.table import Table
import numpy as np
from pahfit.base import PAHFITBase
from pahfit.helpers import find_packfile


def test_model_trimming():
    """
    Goal
    ----
    Test if the model is built correctly with certain features removed
    from the science pack. For example, when this test was written,
    generating the model without specifying any gaussians will cause the
    code to crash. This test will try to provoke such crashes.

    Desired behavior
    ----------------

    The PAHFITBase instance is generated correctly, without crashing.

    Functions that depend on specific model contents (lines, dust
    features, ...) can deal with those feature not being there.

    """
    # fake obsdata from 0 to 30 micron (will not actually do fitting in
    # this test)
    N = 100
    obsdata = {
        "x": np.linspace(1, 30, N),
        "y": np.linspace(1, 2, N),
        "unc": np.full(N, 0.1),
    }

    # choose any science pack
    packfile = find_packfile("scipack_ExGal_SpitzerIRSSLLL.ipac")

    # load the pack table using astropy
    packtable = Table.read(packfile, format=packfile.split(".")[-1])

    # parse table into the param_info dict, and init PAHFITBase object from it
    def parse_and_init(astropy_table):
        param_info = PAHFITBase.parse_table(astropy_table)
        pmodel = PAHFITBase(
            obsdata["x"], obsdata["y"], estimate_start=True, param_info=param_info
        )
        return pmodel

    # Case 0: the whole table
    # whole_pmodel
    _ = parse_and_init(packtable)

    # Case 1, 2, and 3 (no BB, Gauss, Drude)
    remove_forms = ["BlackBody1D", "Gaussian1D", "Drude1D", "att_Drude1D"]
    for form in remove_forms:
        _ = parse_and_init(packtable[packtable["Form"] != form])


if __name__ == "__main__":
    test_model_trimming()
