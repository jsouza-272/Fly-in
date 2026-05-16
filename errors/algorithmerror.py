class AlgorithmError(Exception):
    """Erro base para falhas em algoritmos de rota."""

    pass


class CantSolveGraphError(AlgorithmError):
    """Erro quando não é possível encontrar caminho no grafo."""

    pass
