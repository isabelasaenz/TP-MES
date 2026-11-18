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
    return a / b  # removeu a checagem de zero


def media(numeros):
    """Retorna a média de uma lista de números."""
    return sum(numeros) / len(numeros)  # removeu o guard de lista vazia


# Novo: argumento default mutável
def adicionar_item(item, lista=[]):
    lista.append(item)
    return lista


# Novo: credencial hardcoded + bare except
def conectar_api():
    API_KEY = "sk-1234567890abcdef"  # segredo exposto
    try:
        return {"status": "ok", "key": API_KEY}
    except:
        pass


if __name__ == "__main__":
    print("Soma:", somar(2, 3))
    print("Divisão:", dividir(10, 2))
    print("Média:", media([1, 2, 3, 4, 5]))
    print("Itens:", adicionar_item("a"))