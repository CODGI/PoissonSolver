from poisson.charge import Charge
import pytest


def test_invalidValue():
    with pytest.raises(ValueError):
        c = Charge(2, 2, "++")
