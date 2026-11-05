"""Complete these four small functions. Explain and test each function you write."""


def flat_index(x, y, width):
    """Valid coordinates -> index in a row-major pixel list. Example (2,1,4)->6."""
    raise NotImplementedError('TODO 1: rows before y, then x positions')


def marker_fraction(count, area):
    """0 <= count <= area, positive area -> fraction. Reject invalid counts."""
    raise NotImplementedError('TODO 2: validate first, then divide')


def marker_status(ratio, mean_value, threshold=.08):
    """Mean value < .12 -> unknown; otherwise >= threshold present, else absent."""
    raise NotImplementedError('TODO 3: uncertainty comes before classification')


def fuse_evidence(vision, sonar):
    """Inputs clear/blocked/unknown. Either blocked wins; both clear -> clear; else unknown.
    This exercise assumes vision evidence has ALREADY been justified and mapped.
    marker_absent is NOT automatically clear.
    """
    raise NotImplementedError('TODO 4: write the three rules in order')
