from poisson.grid import Grid


def test_grid_shape_includes_endpoints():
    g = Grid(10, 10, 1, 1, includeEnd=True)
    assert g.potential.shape == (11, 11)
    assert g.x[0] == 0 and g.x[-1] == 10
    assert g.y[0] == 0 and g.y[-1] == 10


def test_grid_without_endpoints():
    g = Grid(10, 10, 1, 1, includeEnd=False)
    assert g.potential.shape == (10, 10)
    assert g.x[-1] == 9 and g.y[-1] == 9


def test_grid_str_contains_info():
    g = Grid(4, 2, 0.5, 1.0)
    s = str(g)
    # quick sanity checks
    assert "Lx = 4.0" in s and "Ly = 2.0" in s
    assert "Shape = (9,3)" in s  # 4/0.5=8 ⇒ +1 = 9 ; 2/1=2 ⇒ +1 = 3
