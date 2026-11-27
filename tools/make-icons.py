#!/usr/bin/env python3
"""사랑 오피스 PWA 아이콘 생성기.

다크 네이비(#0F172A) 배경 위 흰색 'S.' 로고.
- icon-192.png / icon-512.png          : purpose "any"    (둥근 모서리, 투명 코너)
- icon-192-maskable.png / -512         : purpose "maskable" (풀블리드, 안전영역 안에 로고)

사용: python3 tools/make-icons.py
"""
from PIL import Image, ImageDraw, ImageFont

NAVY_TOP = (27, 42, 69)      # #1B2A45 하이라이트
NAVY_BASE = (15, 23, 42)     # #0F172A
NAVY_DEEP = (9, 14, 27)      # #090E1B
MINT = (16, 185, 129)        # #10B981 — 페이지의 민트 포인트
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
S = 4                        # 슈퍼샘플 배율


def gradient(size):
    """좌상단 하이라이트 → 우하단 딥 네이비 대각선 그라데이션."""
    img = Image.new("RGB", (size, size), NAVY_BASE)
    px = img.load()
    for y in range(size):
        for x in range(size):
            t = (x / size * 0.45 + y / size * 0.55)          # 0..1 대각선
            if t < 0.5:                                       # 위쪽: 하이라이트 → 베이스
                k = t / 0.5
                c = tuple(round(NAVY_TOP[i] + (NAVY_BASE[i] - NAVY_TOP[i]) * k) for i in range(3))
            else:                                             # 아래쪽: 베이스 → 딥
                k = (t - 0.5) / 0.5
                c = tuple(round(NAVY_BASE[i] + (NAVY_DEEP[i] - NAVY_BASE[i]) * k) for i in range(3))
            px[x, y] = c
    return img


def draw_logo(size, ratio, radius_ratio):
    """size 크기 아이콘. ratio = 'S.' 글자 높이 비율, radius_ratio = 모서리 반경 비율."""
    big = size * S
    # 1) 배경(풀블리드 정사각) + 그라데이션
    bg = gradient(big)
    # 2) 마스크: 둥근 사각형(radius_ratio>0) 또는 정사각 전체
    mask = Image.new("L", (big, big), 0)
    md = ImageDraw.Draw(mask)
    if radius_ratio > 0:
        md.rounded_rectangle([0, 0, big - 1, big - 1], radius=round(big * radius_ratio), fill=255)
    else:
        md.rectangle([0, 0, big - 1, big - 1], fill=255)
    out = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    out.paste(bg, (0, 0), mask)

    # 3) 흰색 'S' + 민트 점 — 목표 높이에 맞춰 폰트 크기 역산
    target_h = big * ratio
    fs = 100
    for _ in range(24):
        f = ImageFont.truetype(FONT, fs)
        box = f.getbbox("S")
        h = box[3] - box[1]
        if h == 0:
            break
        fs = max(8, round(fs * target_h / h))
    f = ImageFont.truetype(FONT, fs)
    box = f.getbbox("S")
    gw, gh = box[2] - box[0], box[3] - box[1]

    dot = gh * 0.255                     # 점 지름
    gap = gh * 0.085                     # S ↔ 점 간격
    total_w = gw + gap + dot
    left = (big - total_w) / 2
    top = (big - gh) / 2 + big * 0.004   # 광학 보정: 살짝 아래

    layer = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.text((left - box[0], top - box[1]), "S", font=f, fill=(255, 255, 255, 255))
    baseline = top + gh             # 'S' 아랫선
    dx = left + gw + gap
    ld.rounded_rectangle([dx, baseline - dot, dx + dot, baseline],
                         radius=dot * 0.40, fill=MINT + (255,))
    out = Image.alpha_composite(out, layer)
    return out.resize((size, size), Image.LANCZOS)


def main():
    # any: 둥근 모서리(22.6%), 로고 높이 46%
    for s in (192, 512):
        draw_logo(s, 0.455, 0.226).save(f"icon-{s}.png")
    # maskable: 풀블리드, 로고 높이 36% (안전영역 = 중앙 80% 원 안)
    for s in (192, 512):
        draw_logo(s, 0.355, 0.0).save(f"icon-{s}-maskable.png")
    # iOS 홈화면용 (투명 없음)
    draw_logo(180, 0.44, 0.0).save("icon-180.png")
    print("icons written")


if __name__ == "__main__":
    main()
