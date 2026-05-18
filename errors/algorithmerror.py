"""Algorithm-related exception hierarchy definitions."""

class AlgorithmError(Exception):
    """Base error for route algorithm failures."""

    pass


class CantSolveGraphError(AlgorithmError):
    """Error raised when no path can be found in the graph."""

    pass
