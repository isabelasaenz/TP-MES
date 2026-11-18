# calculadora.py
"""Pequeno módulo de utilidades matemáticas para a demo de revisão de PR."""


def somar(a, b):
    """Retorna a soma de dois números."""
    return a + b


def subtrair(a, b):
    """Retorna a diferença entre dois números."""
    return a - b


def multiplicar(a, b):
    """Retorna o produto de dois números."""
    return a * b


def dividir(a, b):
    """Retorna a divisão de a por b."""
    if b == 0:
        raise ValueError("Não é possível dividir por zero.")
    return a / b


def media(numeros):
    """Retorna a média de uma lista de números."""
    if not numeros:
        return 0
    return sum(numeros) / len(numeros)


if __name__ == "__main__":
    print("Soma:", somar(2, 3))
    print("Divisão:", dividir(10, 2))
    print("Média:", media([1, 2, 3, 4, 5]))