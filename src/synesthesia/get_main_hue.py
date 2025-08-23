# Third-party
from PIL import Image, ImageStat
import colorsys
from collections import Counter

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

    return f"{r8:02x}{g8:02x}{b8:02x}"


def album_led_hex(path: str) -> str:
    """
    Возвращает RRGGBB для ленты:
    - берём основной hue из 2-квантов,
    - смешиваем «натуральный» цвет с «чистым» (S=1) через коэффициент PURITY,
    - гамма-коррекция и мягкая отсечка слабого канала (убираем грязь).
    """
    PURITY = 1.0   
    GAMMA  = 2.6    
    MIN_CH = 6 

    img = Image.open(path).convert("RGB").resize((128, 128))
    pal = img.quantize(colors=2, method=Image.MEDIANCUT)
    counts = pal.getcolors(10000) or []
    palette = pal.getpalette()

    if counts:
        best_hsv = None
        best_score = -1.0
        for cnt, idx in counts:
            r = palette[idx*3 + 0]; g = palette[idx*3 + 1]; b = palette[idx*3 + 2]
            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
            score = cnt * (0.6 + 0.4*s) * (0.4 + 0.6*v)
            if score > best_score:
                best_score = score
                best_hsv = (h, s, v)
    else:
        r, g, b = img.resize((1,1)).getpixel((0,0))
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        best_hsv = (h, s, v)

    h, s, v = best_hsv
    V = max(0.35, min(0.95, v))      
    S_nat = max(0.35, min(1.0, s))    

    rn, gn, bn = colorsys.hsv_to_rgb(h, S_nat, V)
    rp, gp, bp = colorsys.hsv_to_rgb(h, 1.0,   V)

    r = int(round(((1-PURITY)*rn + PURITY*rp) * 255))
    g = int(round(((1-PURITY)*gn + PURITY*gp) * 255))
    b = int(round(((1-PURITY)*bn + PURITY*bp) * 255))

    def gfix(x: int) -> int:
        return int(round((x/255.0) ** GAMMA * 255))
    r, g, b = map(gfix, (r, g, b))

    if r < MIN_CH: r = 0
    if g < MIN_CH: g = 0
    if b < MIN_CH: b = 0

    return f"{r:02x}{g:02x}{b:02x}"



