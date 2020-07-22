def sobreposição(faixa1, faixa2):
    inferior = max(faixa1[0], faixa2[0])
    superior = min(faixa1[1], faixa2[1])
    if inferior <= superior:
        return (inferior, superior)
    else:
        return None
