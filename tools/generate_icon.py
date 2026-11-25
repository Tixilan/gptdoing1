from pathlib import Path

from PIL import Image, ImageDraw


def main() -> None:
    output = Path("build/icon.ico")
    output.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((12, 12, 244, 244), radius=54, fill="#216FD1")
    draw.ellipse((52, 52, 204, 204), outline="white", width=12)
    draw.line((128, 128, 128, 78), fill="white", width=12)
    draw.line((128, 128, 174, 151), fill="white", width=12)
    draw.ellipse((119, 119, 137, 137), fill="white")
    image.save(output, sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])


if __name__ == "__main__":
    main()

