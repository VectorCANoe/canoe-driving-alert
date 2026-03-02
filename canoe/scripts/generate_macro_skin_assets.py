from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("canoe/project/panel/Bitmaps/reference_pack_v1")
ROOT.mkdir(parents=True, exist_ok=True)


def save(img: Image.Image, name: str):
    out = ROOT / name
    img.save(out)
    print(f"generated:{out}")


def make_external_background():
    w, h = 1024, 480
    img = Image.new("RGB", (w, h), (9, 14, 22))
    d = ImageDraw.Draw(img)

    for y in range(h):
        c = int(22 + (y / h) * 28)
        d.line([(0, y), (w, y)], fill=(c, c + 8, c + 18))

    road_top = 120
    road_bottom = 455
    d.polygon([(0, road_bottom), (w, road_bottom), (w - 120, road_top), (120, road_top)], fill=(22, 24, 30))

    for x in range(70, w, 150):
        d.polygon([(x, 430), (x + 46, 430), (x + 70, 355), (x + 24, 355)], fill=(230, 189, 60))

    for i in range(8):
        alpha = max(0, 160 - i * 20)
        d.arc((250 - i * 24, 42 - i * 10, 900 + i * 24, 280 + i * 14), start=188, end=350, fill=(255, 145, 55, alpha), width=3)

    d.rectangle((0, 0, w, 58), fill=(5, 8, 12))
    d.text((18, 18), "SDV External Macro View", fill=(190, 220, 255), font=ImageFont.load_default())

    save(img, "EXT_Background.png")


def make_cabin_background():
    w, h = 1024, 480
    base = Image.open(ROOT / "CABIN_FrontWindow_scene.bmp").convert("RGB")
    img = base.resize((w, h), Image.Resampling.LANCZOS)
    d = ImageDraw.Draw(img)

    d.rectangle((0, 0, w, 74), fill=(6, 9, 14))
    d.rectangle((0, h - 50, w, h), fill=(8, 10, 14))
    d.text((20, 22), "SDV Cabin Panorama View", fill=(210, 230, 255), font=ImageFont.load_default())

    for x in range(120, 930, 200):
        d.ellipse((x, 150, x + 100, 240), outline=(255, 140, 40), width=2)
        d.ellipse((x - 25, 132, x + 125, 258), outline=(255, 140, 40), width=1)

    save(img, "CABIN_Background.png")


def make_vehicle_move_strip():
    frame_w, frame_h, n = 460, 70, 11
    car = Image.open(ROOT / "EXT_VCar_topview.png").convert("RGBA").resize((42, 92), Image.Resampling.LANCZOS)

    strip = Image.new("RGBA", (frame_w * n, frame_h), (0, 0, 0, 0))
    for i in range(n):
        frame = Image.new("RGBA", (frame_w, frame_h), (0, 0, 0, 0))
        d = ImageDraw.Draw(frame)
        d.rectangle((0, 31, frame_w, 40), fill=(70, 205, 165, 220))
        d.rectangle((0, 22, frame_w, 24), fill=(255, 208, 70, 140))
        d.rectangle((0, 46, frame_w, 48), fill=(255, 208, 70, 140))

        x = int(16 + (frame_w - 72) * (i / (n - 1)))
        frame.alpha_composite(car, (x, -10))
        strip.alpha_composite(frame, (i * frame_w, 0))

    save(strip, "EXT_VehicleMove11.png")


def make_flow_badge():
    frame_w, frame_h, n = 200, 26, 3
    strip = Image.new("RGBA", (frame_w * n, frame_h), (0, 0, 0, 0))
    labels = ["FLOW: --", "FLOW: L->R", "FLOW: R->L"]
    colors = [(58, 64, 74), (86, 182, 255), (86, 182, 255)]

    for i in range(n):
        frame = Image.new("RGBA", (frame_w, frame_h), colors[i])
        d = ImageDraw.Draw(frame)
        d.rectangle((0, 0, frame_w - 1, frame_h - 1), outline=(180, 190, 210), width=1)
        d.text((52, 7), labels[i], fill=(255, 255, 255), font=ImageFont.load_default())
        strip.alpha_composite(frame, (i * frame_w, 0))

    save(strip, "EXT_FlowBadge3.png")


def make_vehicle_class_strip():
    frame_w, frame_h, n = 220, 90, 8
    strip = Image.new("RGBA", (frame_w * n, frame_h), (0, 0, 0, 0))

    names = [
        "NONE", "ZONE", "POLICE", "AMB", "IC", "LANE", "WARN", "SYS"
    ]
    tones = [
        (50, 56, 66), (228, 192, 72), (67, 132, 255), (229, 92, 92),
        (92, 195, 155), (102, 166, 244), (241, 132, 70), (155, 144, 212)
    ]

    for i in range(n):
        frame = Image.new("RGBA", (frame_w, frame_h), (0, 0, 0, 0))
        d = ImageDraw.Draw(frame)
        d.rounded_rectangle((4, 7, frame_w - 4, frame_h - 8), radius=12, fill=(18, 22, 30), outline=(95, 105, 122), width=1)
        d.rounded_rectangle((12, 16, 102, 74), radius=10, fill=tones[i])
        d.rectangle((123, 20, 206, 31), fill=(tones[i][0], tones[i][1], tones[i][2], 220))
        d.text((124, 38), names[i], fill=(225, 232, 242), font=ImageFont.load_default())
        strip.alpha_composite(frame, (i * frame_w, 0))

    save(strip, "EXT_VehicleClass8.png")


def make_ems_blink_strip():
    frame_w, frame_h = 20, 20
    strip = Image.new("RGBA", (frame_w * 2, frame_h), (0, 0, 0, 0))

    a = Image.new("RGBA", (frame_w, frame_h), (0, 0, 0, 0))
    da = ImageDraw.Draw(a)
    da.polygon([(2, 18), (10, 2), (18, 18)], fill=(220, 32, 32))

    b = Image.new("RGBA", (frame_w, frame_h), (0, 0, 0, 0))
    db = ImageDraw.Draw(b)
    db.polygon([(2, 18), (10, 2), (18, 18)], fill=(60, 120, 255))

    strip.alpha_composite(a, (0, 0))
    strip.alpha_composite(b, (frame_w, 0))
    save(strip, "EXT_EmsBlink2.png")


def make_nav_background():
    w, h = 734, 396
    img = Image.new("RGB", (w, h), (8, 12, 20))
    d = ImageDraw.Draw(img)

    for y in range(h):
        c = int(18 + (y / h) * 34)
        d.line([(0, y), (w, y)], fill=(c, c + 6, c + 14))

    d.polygon([(0, h - 8), (w, h - 8), (w - 74, 126), (74, 126)], fill=(26, 28, 34))
    for x in range(70, w, 120):
        d.polygon([(x, 332), (x + 34, 332), (x + 48, 276), (x + 14, 276)], fill=(245, 198, 66))

    d.rectangle((0, 0, w, 52), fill=(5, 8, 12))
    d.text((14, 18), "SDV Navigation Detail", fill=(186, 216, 255), font=ImageFont.load_default())
    save(img, "NAV_Background.png")


def make_ambient_background():
    w, h = 768, 340
    img = Image.new("RGB", (w, h), (10, 11, 16))
    d = ImageDraw.Draw(img)

    for y in range(h):
        c = int(14 + (y / h) * 18)
        d.line([(0, y), (w, y)], fill=(c, c + 4, c + 10))

    for i in range(5):
        off = i * 22
        d.arc((90 - off, 42 - off, 670 + off, 290 + off), start=188, end=350, fill=(255, 132, 52), width=2)

    d.rectangle((0, 0, w, 48), fill=(6, 8, 13))
    d.text((14, 16), "SDV Ambient Detail", fill=(230, 232, 238), font=ImageFont.load_default())
    save(img, "AMB_Background.png")


if __name__ == "__main__":
    make_external_background()
    make_cabin_background()
    make_vehicle_move_strip()
    make_flow_badge()
    make_vehicle_class_strip()
    make_ems_blink_strip()
    make_nav_background()
    make_ambient_background()
