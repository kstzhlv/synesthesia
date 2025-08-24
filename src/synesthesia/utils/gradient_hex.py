from typing import List, Tuple
from loguru import logger

def _hex_to_rgb_nohash(s: str) -> Tuple[int, int, int]:
    s = s.strip()
    if len(s) == 6:
        return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)

    raise ValueError("Expected hex string 'RRGGBB' without '#'")


def _rgb_to_hex_nohash(rgb: Tuple[int,int,int]) -> str:
    r,g,b = (max(0, min(255, int(v))) for v in rgb)
    return f"{r:02x}{g:02x}{b:02x}"

def gradient_hex(
    c1: str,
    c2: str,
    steps: int,
    *,
    include_end: bool = True
): 
    if steps < 1 or (include_end and steps < 2):
        raise ValueError("steps must be >= 2 when include_end=True")

    r1,g1,b1 = _hex_to_rgb_nohash(c1)
    r2,g2,b2 = _hex_to_rgb_nohash(c2)

    denom = (steps - 1) if include_end else steps
    out: List[str] = []
    for i in range(steps):
        t = 0.0 if denom == 0 else i / denom
        r = round(r1 + (r2 - r1) * t)
        g = round(g1 + (g2 - g1) * t)
        b = round(b1 + (b2 - b1) * t)
        out.append(_rgb_to_hex_nohash((r,g,b)))

    for c in out:
        yield c

