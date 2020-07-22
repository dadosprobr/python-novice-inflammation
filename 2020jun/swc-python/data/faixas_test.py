from faixas import sobreposição


def test_sobreposição_um_dentro_do_outro():
    faixa1 = (-3, 5)
    faixa2 = (0, 4.5)
    res = sobreposição(faixa1, faixa2)
    assert res == faixa2
    res = sobreposição(faixa2, faixa1)
    assert res == faixa2


def test_sobreposição_parcial():
    faixa1 = (-3, 3)
    faixa2 = (0, 4.5)
    esperado = (0, 3)
    res = sobreposição(faixa1, faixa2)
    assert res == esperado, f'{res} != {faixa2}'
    res = sobreposição(faixa2, faixa1)
    assert res == esperado


def test_sobreposição_inexistente():
    faixa1 = (-3, 5)
    faixa2 = (6, 10)
    res = sobreposição(faixa1, faixa2)
    assert res is None, f'esperava None, veio {res}'