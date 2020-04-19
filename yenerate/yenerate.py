import textwrap
import sys
import os.path

from argparse import ArgumentParser
from PIL import Image, ImageFont, ImageDraw
from functools import reduce


def create_image(text, cover_img_path, font_path, font_size=120, text_color=(41, 247, 78), line_spacing=55):
    """
    Overlays text over the image corresponding to cover_img_name.
    Returns an Image object with the text overlay.
    """

    cover_img = Image.open(cover_img_path)
    draw = ImageDraw.Draw(cover_img)
    font = ImageFont.truetype(font_path, font_size)

    wrapped_text, max_line = wrap_text(text)

    W, H = cover_img.size
    print(f"{cover_img_path} [{W}x{H}]")

    w, h = draw.textsize(max_line, font=font, spacing=line_spacing)
    print(f"text overlay [{W}x{H}]")

    w_c, h_c = (W - w) / 2, (H - h) / 2
    print(f"text centered at ({w_c}, {h_c})")

    draw.multiline_text((w_c, h_c),
                        wrapped_text,
                        font=font,
                        fill=text_color,
                        align='center',
                        spacing=line_spacing)

    del font
    del draw

    return cover_img


def wrap_text(text, max_width=15):
    """
    wraps text such that each line has a maximum
    width of 20 characters. Increases the spacing between
    each word.

    Returns the wrapped text along with the line with
    the greatest number of characters.
    """
    # expanded = map(lambda w : '  ' + w + '  ', text.split())
    # lines = textwrap.wrap(''.join(expanded), width=20)

    # TODO: handle new lines
    lines = textwrap.wrap(text, width=max_width)
    def get_max_line(x, y): return x if len(x) > len(y) else y
    max_line = reduce(get_max_line, lines)

    print(f"text was split into {len(lines)} line(s)")

    return '\n'.join(lines), max_line


def main():
    parser = ArgumentParser(description="generate custom ye album art")
    parser.add_argument(
        "-c", "--cover", help="the background album art", default="yenerate/data/ye_album_art.jpg")
    parser.add_argument(
        "-f", "--font", help="the path to the ye font", default="yenerate/data/ye_font_num_regular.ttf")
    parser.add_argument(
        "-o", "--output", help="the output file name", default="my_ye.jpg")
    parser.add_argument("text", help="the ye text to render")
    args = parser.parse_args()

    my_ye = create_image(
        text=args.text, cover_img_path=args.cover, font_path=args.font)
    my_ye.save(args.output)
    print("saved image:", args.output)


if __name__ == '__main__':
    main()