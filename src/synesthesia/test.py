from typing import Literal, Tuple

EdgeId = Literal[1, 2, 3, 4, 5, 6]


def snap_to_six_edges(
    rgb: Tuple[int, int, int],
    *,
    gamma_for_choice: float | None = None,
) -> Tuple[Tuple[int, int, int], EdgeId]:
    r, g, b = (max(0, min(255, int(c))) for c in rgb)

    def to_space(x: int) -> float:
        u = x / 255.0
        return u**gamma_for_choice if gamma_for_choice and gamma_for_choice > 0 else u

    R, G, B = map(to_space, (r, g, b))

    candidates = {
        1: {"fix": {"g": 0, "b": 255}, "free": "r"},  # 0-255, 0, 255
        2: {"fix": {"r": 255, "g": 0}, "free": "b"},  # 255, 0, 0-255
        3: {"fix": {"r": 255, "b": 0}, "free": "g"},  # 255, 0-255, 0
        4: {"fix": {"g": 255, "b": 0}, "free": "r"},  # 0-255, 255, 0
        5: {"fix": {"r": 0, "g": 255}, "free": "b"},  # 0, 255, 0-255
        6: {"fix": {"r": 0, "b": 255}, "free": "g"},  # 0, 0-255, 255
    }

    current = {"r": R, "g": G, "b": B}

    def dist2(edge: int) -> float:
        fix = candidates[edge]["fix"]
        d = 0.0
        for ch, val255 in fix.items():
            target = 0.0 if val255 == 0 else 1.0
            d += (current[ch] - target) ** 2
        return d

    best_edge = min(candidates.keys(), key=dist2)

    free_ch = candidates[best_edge]["free"]
    fix = candidates[best_edge]["fix"]

    out = {"r": r, "g": g, "b": b}  # по умолчанию — исходные
    for ch, v in fix.items():
        out[ch] = v

    return (out["r"], out["g"], out["b"]), best_edge
