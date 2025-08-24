# Standart
import colorsys
from collections import Counter

# Third-party
from PIL import Image, ImageStat

def _clamp8(x: int) -> int:
    return max(0, min(255, int(round(x))))

def _snap_colour(rgb: tuple[int, int, int]):
    v = [_clamp8(c) for c in rgb]
    max_idx = max(range(3), key=lambda i: v[i])
    min_idx = min([i for i in range(3) if i != max_idx], key=lambda i: v[i])
    mid_idx = ({0, 1, 2} - {max_idx, min_idx}).pop()

    out = v[:]
    out[max_idx] = 255
    out[mid_idx] = _clamp8(v[mid_idx] // 5)
    out[min_idx] = 0


    return tuple(out)


def get_main_hue_hex(path: str) -> str:
    img = Image.open(path).convert("RGB").resize((100, 100))
    pixels = img.getdata()

    hues = []
    for r, g, b in pixels:
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        if s > 0.2 and 0.2 < v < 0.98:
            hues.append(int(h * 360))

    if not hues:
        stat = ImageStat.Stat(img)
        r8, g8, b8 = map(lambda x: int(x), stat.mean[:3])
    else:
        hue = Counter(hues).most_common(1)[0][0] / 360.0
        r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.8)
        r8, g8, b8 = int(round(r*255)), int(round(g*255)), int(round(b*255))

    result_rgb = _snap_colour((r8, g8, b8))

    return f"{result_rgb[0]:02x}{result_rgb[1]:02x}{result_rgb[2]:02x}"

if __name__ == "__main__":
    print(get_main_hue_hex("/home/decent/Downloads/550x550-3302868797.jpg"))

