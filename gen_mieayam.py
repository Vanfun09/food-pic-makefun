"""
Mie Ayam Khas Indonesia - Dark Moody Food Photography Style
Generated with Pillow - no external assets
Style reference: warm ambient lighting, dark background, 35-40° angle view
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, random, colorsys, os

random.seed(42)
W, H = 800, 800
img = Image.new('RGB', (W, H))
draw = ImageDraw.Draw(img)

# ============================================================
# 1. DARK WOOD TABLE BACKGROUND with grain texture
# ============================================================
for y in range(H):
    for x in range(W):
        # Base dark wood
        base_r = 28 + int(8 * math.sin(x * 0.02 + y * 0.005))
        base_g = 20 + int(6 * math.sin(x * 0.02 + y * 0.005))
        base_b = 14 + int(4 * math.sin(x * 0.02 + y * 0.005))
        # Wood grain horizontal streaks
        grain = int(5 * math.sin(y * 0.3 + x * 0.01) * math.sin(y * 0.7))
        # Noise
        noise = random.randint(-6, 6)
        r = max(0, min(255, base_r + grain + noise))
        g = max(0, min(255, base_g + grain + noise))
        b = max(0, min(255, base_b + grain + noise))
        img.putpixel((x, y), (r, g, b))

# ============================================================
# 2. BOWL - dark ceramic, slightly elliptical (3/4 angle view)
# ============================================================
cx, cy = 400, 420  # bowl center
bowl_rx, bowl_ry = 280, 220  # ellipse radii

# Bowl outer shadow
shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
for i in range(30, 0, -1):
    alpha = int(40 * (1 - i / 30))
    sd.ellipse([cx - bowl_rx - i, cy - bowl_ry - i + 10, cx + bowl_rx + i, cy + bowl_ry + i + 10],
               fill=(0, 0, 0, alpha))
img.paste(Image.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, 0)), shadow).convert('RGB'),
          mask=shadow.split()[3])

# Bowl rim (dark ceramic with subtle glaze)
for i in range(15, 0, -1):
    t = i / 15
    rc = int(45 + 20 * t)
    gc = int(38 + 15 * t)
    bc = int(32 + 10 * t)
    draw.ellipse([cx - bowl_rx - i, cy - bowl_ry - i, cx + bowl_rx + i, cy + bowl_ry + i],
                 fill=(rc, gc, bc))

# Bowl inner - lighter rim highlight (top-left light source)
for angle_deg in range(360):
    angle = math.radians(angle_deg)
    for r_off in range(8):
        px = int(cx + (bowl_rx - r_off) * math.cos(angle))
        py = int(cy + (bowl_ry - r_off) * math.sin(angle))
        if 0 <= px < W and 0 <= py < H:
            # Highlight on top-left of rim
            highlight = max(0, math.cos(angle - math.radians(225))) * 40
            base = img.getpixel((px, py))
            nr = min(255, int(base[0] + highlight))
            ng = min(255, int(base[1] + highlight * 0.8))
            nb = min(255, int(base[2] + highlight * 0.6))
            img.putpixel((px, py), (nr, ng, nb))

# ============================================================
# 3. BROTH AREA - kuah mie ayam (clear chicken broth, lighter than ramen)
# ============================================================
broth_rx, broth_ry = bowl_rx - 18, bowl_ry - 14

# Fill broth base - clear golden chicken broth
for y in range(cy - broth_ry, cy + broth_ry):
    for x in range(cx - broth_rx, cx + broth_rx):
        # Check if inside ellipse
        ex = ((x - cx) / broth_rx) ** 2 + ((y - cy) / broth_ry) ** 2
        if ex <= 1.0:
            # Broth color - lighter, clearer than ramen (kuah bening kecoklatan)
            depth = ex  # darker at edges
            noise = random.randint(-4, 4)
            # Light chicken broth - golden brown
            br = min(255, max(0, int(175 - 40 * depth + noise)))
            bg = min(255, max(0, int(120 - 30 * depth + noise)))
            bb = min(255, max(0, int(55 - 20 * depth + noise)))
            
            # Oil sheen spots (chicken fat)
            oil_val = math.sin(x * 0.15) * math.sin(y * 0.12) * math.cos((x + y) * 0.08)
            if oil_val > 0.5:
                br = min(255, br + 35)
                bg = min(255, bg + 25)
                bb = min(255, bb + 10)
            
            img.putpixel((x, y), (br, bg, bb))

# ============================================================
# 4. NOODLES - mie kuning (egg noodles, thicker than ramen)
# ============================================================
def draw_noodle(img, start_x, start_y, length, angle, thickness, color_base):
    d = ImageDraw.Draw(img)
    points = []
    for t in range(length):
        wobble = math.sin(t * 0.15) * 4 + math.sin(t * 0.3) * 2
        x = start_x + t * math.cos(angle) + wobble * math.sin(angle)
        y = start_y + t * math.sin(angle) - wobble * math.cos(angle)
        points.append((x, y))
    
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        # Vary color slightly along noodle
        noise = random.randint(-8, 8)
        r = min(255, max(0, color_base[0] + noise))
        g = min(255, max(0, color_base[1] + noise))
        b = min(255, max(0, color_base[2] + noise))
        
        # Draw thick line
        for dt in range(-thickness, thickness + 1):
            px = int(x1 + dt * math.sin(angle) * 0.3)
            py = int(y1 - dt * math.cos(angle) * 0.3)
            if 0 <= px < W and 0 <= py < H:
                ex = ((px - cx) / broth_rx) ** 2 + ((py - cy) / broth_ry) ** 2
                if ex <= 0.95:
                    # Shading - lighter on top
                    shade = 1.0 + dt * 0.02
                    img.putpixel((px, py), (min(255, int(r * shade)),
                                            min(255, int(g * shade)),
                                            min(255, int(b * shade))))

# Mie ayam noodles - pile of yellow egg noodles (center-left area)
noodle_colors = [(215, 185, 90), (200, 170, 75), (225, 195, 100), (210, 178, 82)]
noodle_cx, noodle_cy = cx - 30, cy - 10

for i in range(45):
    angle = random.uniform(0, math.pi * 2)
    sx = noodle_cx + random.randint(-100, 100)
    sy = noodle_cy + random.randint(-60, 60)
    length = random.randint(60, 140)
    thickness = random.randint(2, 4)
    color = random.choice(noodle_colors)
    # Check if start is within broth
    ex = ((sx - cx) / broth_rx) ** 2 + ((sy - cy) / broth_ry) ** 2
    if ex <= 0.85:
        draw_noodle(img, sx, sy, length, angle, thickness, color)

# ============================================================
# 5. AYAM SUWIR (shredded chicken) - top right area
# ============================================================
chicken_cx, chicken_cy = cx + 100, cy - 50

for i in range(60):
    # Shredded chicken pieces
    sx = chicken_cx + random.randint(-70, 50)
    sy = chicken_cy + random.randint(-40, 30)
    ex_check = ((sx - cx) / broth_rx) ** 2 + ((sy - cy) / broth_ry) ** 2
    if ex_check <= 0.8:
        angle = random.uniform(-0.3, 0.3) + math.pi * 0.1
        length = random.randint(15, 35)
        # Chicken color - cooked, slightly caramelized with kecap manis
        base_shade = random.uniform(0.8, 1.2)
        color = (min(255, int(160 * base_shade)),
                 min(255, int(105 * base_shade)),
                 min(255, int(50 * base_shade)))
        for t in range(length):
            wobble = math.sin(t * 0.4) * 1.5
            px = int(sx + t * math.cos(angle) + wobble)
            py = int(sy + t * math.sin(angle))
            thick = random.randint(1, 3)
            for dy in range(-thick, thick + 1):
                ppx, ppy = px, py + dy
                if 0 <= ppx < W and 0 <= ppy < H:
                    noise = random.randint(-10, 10)
                    img.putpixel((ppx, ppy), (min(255, max(0, color[0] + noise)),
                                               min(255, max(0, color[1] + noise)),
                                               min(255, max(0, color[2] + noise))))

# Kecap manis glaze on chicken
for i in range(25):
    gx = chicken_cx + random.randint(-50, 40)
    gy = chicken_cy + random.randint(-30, 20)
    ex_check = ((gx - cx) / broth_rx) ** 2 + ((gy - cy) / broth_ry) ** 2
    if ex_check <= 0.75:
        for dx in range(-2, 3):
            for dy in range(-1, 2):
                px, py = gx + dx, gy + dy
                if 0 <= px < W and 0 <= py < H:
                    img.putpixel((px, py), (85 + random.randint(-5, 5),
                                            45 + random.randint(-5, 5),
                                            15 + random.randint(-3, 3)))

# ============================================================
# 6. BAKSO (meatballs) - 2-3 small meatballs
# ============================================================
meatball_positions = [(cx - 130, cy + 40, 22), (cx - 80, cy + 70, 20), (cx + 30, cy + 80, 18)]

for mbx, mby, mbr in meatball_positions:
    ex_check = ((mbx - cx) / broth_rx) ** 2 + ((mby - cy) / broth_ry) ** 2
    if ex_check <= 0.9:
        for dy in range(-mbr, mbr + 1):
            for dx in range(-mbr, mbr + 1):
                dist = math.sqrt(dx * dx + dy * dy)
                if dist <= mbr:
                    px, py = mbx + dx, mby + dy
                    if 0 <= px < W and 0 <= py < H:
                        # Sphere shading (light from top-left)
                        light = max(0, (-dx * 0.6 - dy * 0.8) / mbr)
                        shade = 0.7 + 0.5 * light
                        noise = random.randint(-5, 5)
                        # Brown meatball color
                        r = min(255, max(0, int(110 * shade + noise)))
                        g = min(255, max(0, int(70 * shade + noise)))
                        b = min(255, max(0, int(40 * shade + noise)))
                        img.putpixel((px, py), (r, g, b))

# ============================================================
# 7. DAUN BAWANG (scallion slices) - scattered
# ============================================================
for i in range(35):
    sx = cx + random.randint(-150, 150)
    sy = cy + random.randint(-120, 100)
    ex_check = ((sx - cx) / broth_rx) ** 2 + ((sy - cy) / broth_ry) ** 2
    if ex_check <= 0.88:
        # Small ring or slice of scallion
        size = random.randint(4, 8)
        is_ring = random.random() > 0.4
        for dy in range(-size, size + 1):
            for dx in range(-size, size + 1):
                dist = math.sqrt(dx * dx + dy * dy)
                if is_ring:
                    if size - 2 <= dist <= size:
                        px, py = sx + dx, sy + dy
                        if 0 <= px < W and 0 <= py < H:
                            img.putpixel((px, py), (60 + random.randint(-10, 10),
                                                     140 + random.randint(-15, 15),
                                                     45 + random.randint(-10, 10)))
                else:
                    if dist <= size * 0.6:
                        px, py = sx + dx, sy + dy
                        if 0 <= px < W and 0 <= py < H:
                            img.putpixel((px, py), (55 + random.randint(-8, 8),
                                                     135 + random.randint(-12, 12),
                                                     40 + random.randint(-8, 8)))

# ============================================================
# 8. BAWANG GORENG (fried shallots) - crispy bits scattered on top
# ============================================================
for i in range(80):
    fx = cx + random.randint(-130, 130)
    fy = cy + random.randint(-90, 70)
    ex_check = ((fx - cx) / broth_rx) ** 2 + ((fy - cy) / broth_ry) ** 2
    if ex_check <= 0.82:
        # Tiny crispy shallot pieces
        size = random.randint(2, 5)
        angle = random.uniform(0, math.pi)
        for t in range(size):
            px = int(fx + t * math.cos(angle))
            py = int(fy + t * math.sin(angle))
            if 0 <= px < W and 0 <= py < H:
                # Golden brown fried shallots
                img.putpixel((px, py), (180 + random.randint(-15, 15),
                                        130 + random.randint(-15, 15),
                                        50 + random.randint(-10, 10)))

# ============================================================
# 9. SELEDRI (celery leaves) - small green pieces
# ============================================================
for i in range(20):
    lx = cx + random.randint(-100, 100)
    ly = cy + random.randint(-80, 50)
    ex_check = ((lx - cx) / broth_rx) ** 2 + ((ly - cy) / broth_ry) ** 2
    if ex_check <= 0.85:
        # Tiny celery leaf
        leaf_size = random.randint(4, 9)
        for dy in range(-leaf_size, leaf_size + 1):
            for dx in range(-leaf_size, leaf_size + 1):
                # Leaf shape (pointed oval)
                if abs(dx) * 1.5 + abs(dy) <= leaf_size * 1.2:
                    px, py = lx + dx, ly + dy
                    if 0 <= px < W and 0 <= py < H:
                        img.putpixel((px, py), (40 + random.randint(-8, 8),
                                                 110 + random.randint(-15, 15),
                                                 30 + random.randint(-8, 8)))

# ============================================================
# 10. SAMBAL (red chili sauce) - small dollop on the side
# ============================================================
sambal_cx, sambal_cy = cx + 160, cy + 20
sambal_r = 18
for dy in range(-sambal_r, sambal_r + 1):
    for dx in range(-sambal_r, sambal_r + 1):
        dist = math.sqrt(dx * dx + dy * dy)
        if dist <= sambal_r:
            px, py = sambal_cx + dx, sambal_cy + dy
            ex_check = ((px - cx) / broth_rx) ** 2 + ((py - cy) / broth_ry) ** 2
            if ex_check <= 0.9 and 0 <= px < W and 0 <= py < H:
                # Red sambal with sphere shading
                light = max(0, (-dx * 0.5 - dy * 0.7) / sambal_r)
                shade = 0.6 + 0.6 * light
                noise = random.randint(-5, 5)
                r = min(255, max(0, int(190 * shade + noise)))
                g = min(255, max(0, int(40 * shade + noise)))
                b = min(255, max(0, int(25 * shade + noise)))
                img.putpixel((px, py), (r, g, b))

# Chili seeds in sambal
for i in range(8):
    sx = sambal_cx + random.randint(-10, 10)
    sy = sambal_cy + random.randint(-10, 10)
    dist = math.sqrt((sx - sambal_cx)**2 + (sy - sambal_cy)**2)
    if dist < sambal_r - 3:
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                px, py = sx + dx, sy + dy
                if 0 <= px < W and 0 <= py < H:
                    img.putpixel((px, py), (220 + random.randint(-10, 10),
                                            180 + random.randint(-10, 10),
                                            100 + random.randint(-10, 10)))

# ============================================================
# 11. CHOPSTICKS (sumpit) resting on bowl
# ============================================================
chopstick_color1 = (140, 90, 45)  # wood color
chopstick_color2 = (130, 82, 40)

for stick in range(2):
    # Two parallel chopsticks crossing the bowl
    start_x = 180 + stick * 15
    start_y = 200 + stick * 12
    end_x = 620 + stick * 10
    end_y = 350 + stick * 8
    
    steps = 300
    for t in range(steps):
        frac = t / steps
        x = start_x + (end_x - start_x) * frac
        y = start_y + (end_y - start_y) * frac
        
        # Chopstick thickness (tapers)
        thickness = int(4 - 1.5 * frac)
        
        color = chopstick_color1 if stick == 0 else chopstick_color2
        angle = math.atan2(end_y - start_y, end_x - start_x)
        
        for dt in range(-thickness, thickness + 1):
            px = int(x + dt * math.sin(angle))
            py = int(y - dt * math.cos(angle))
            if 0 <= px < W and 0 <= py < H:
                # Wood grain on chopstick
                grain = int(8 * math.sin(t * 0.1))
                light = 1.0 + dt * 0.04  # highlight on one side
                r = min(255, max(0, int((color[0] + grain) * light)))
                g = min(255, max(0, int((color[1] + grain) * light)))
                b = min(255, max(0, int((color[2] + grain) * light)))
                img.putpixel((px, py), (r, g, b))

# ============================================================
# 12. MANGKOK SAMBAL KECIL (small condiment dish) - bottom right
# ============================================================
cond_cx, cond_cy = 620, 620
cond_r = 45

# Small white ceramic dish
for dy in range(-cond_r - 5, cond_r + 6):
    for dx in range(-cond_r - 5, cond_r + 6):
        dist = math.sqrt(dx * dx + dy * dy)
        if dist <= cond_r + 4:
            px, py = cond_cx + dx, cond_cy + dy
            if 0 <= px < W and 0 <= py < H:
                if dist > cond_r:
                    # Rim
                    light = max(0, (-dx * 0.5 - dy * 0.7) / (cond_r + 4))
                    shade = 0.7 + 0.4 * light
                    img.putpixel((px, py), (int(180 * shade), int(175 * shade), int(168 * shade)))
                else:
                    # Inside - kecap manis (sweet soy sauce)
                    light = max(0, (-dx * 0.3 - dy * 0.5) / cond_r)
                    shade = 0.3 + 0.3 * light
                    noise = random.randint(-3, 3)
                    img.putpixel((px, py), (max(0, int(60 * shade + noise)),
                                            max(0, int(35 * shade + noise)),
                                            max(0, int(15 * shade + noise))))

# ============================================================
# 13. POST-PROCESSING: Warm lighting from top-left + vignette
# ============================================================
# Apply slight blur for more natural look
img = img.filter(ImageFilter.GaussianBlur(radius=0.8))

# Warm light gradient (top-left source)
light_layer = Image.new('RGB', (W, H), (0, 0, 0))
for y in range(H):
    for x in range(W):
        # Distance from top-left light source
        dist = math.sqrt((x - 100) ** 2 + (y - 50) ** 2)
        # Warm light falloff
        intensity = max(0, 1.0 - dist / 900)
        warm_r = int(30 * intensity)
        warm_g = int(18 * intensity)
        warm_b = int(5 * intensity)
        
        base = img.getpixel((x, y))
        r = min(255, base[0] + warm_r)
        g = min(255, base[1] + warm_g)
        b = min(255, base[2] + warm_b)
        img.putpixel((x, y), (r, g, b))

# Vignette
for y in range(H):
    for x in range(W):
        # Distance from center
        dx = (x - W / 2) / (W / 2)
        dy = (y - H / 2) / (H / 2)
        dist = math.sqrt(dx * dx + dy * dy)
        # Darken edges
        vignette = max(0, min(1, 1.0 - (dist - 0.6) * 0.8))
        base = img.getpixel((x, y))
        r = int(base[0] * vignette)
        g = int(base[1] * vignette)
        b = int(base[2] * vignette)
        img.putpixel((x, y), (r, g, b))

# Final slight sharpen for detail
img = img.filter(ImageFilter.SHARPEN)

# Save
img.save("C:/Users/Admin/makefun-food-pic/entry.png", "PNG")
size = os.path.getsize("C:/Users/Admin/makefun-food-pic/entry.png")
print(f"Image: {img.size}, File: {size} bytes ({size/1024:.1f} KB)")
print("OK")
