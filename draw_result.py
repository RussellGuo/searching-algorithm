from fractions import Fraction

from PIL import Image, ImageDraw, ImageColor

from figure import Figure
from geo import Point, Line


def draw_result(fig: Figure, img_path=None):
    grid_size = 100
    line_width = 1
    grid_count = 6
    margin = 10
    total_size = margin * 2 + grid_count * grid_size + line_width

    color_background = ImageColor.colormap["whitesmoke"]
    color_frame      = ImageColor.colormap["darkgrey"]
    color_pre_line   = ImageColor.colormap["darkred"]
    color_ans_line   = ImageColor.colormap["darkblue"]

    img = Image.new('RGB', (total_size, total_size), color_background)
    draw = ImageDraw.Draw(img)

    line_top    = Line(Fraction(0), Fraction(1), Fraction(0))
    line_bottom = Line(Fraction(0), Fraction(1), Fraction(6))
    line_left   = Line(Fraction(1), Fraction(0), Fraction(0))
    line_right  = Line(Fraction(1), Fraction(0), Fraction(6))
    frame = (line_top, line_bottom, line_left, line_right)

    def coord_in_img(p: Point):
        return margin + p.x * grid_size, margin + (grid_count - p.y) * grid_size

    def draw_line(line):
        points = set(line.get_cross_point(frame_line, fig.new_point_checker) for frame_line in frame) - {None}
        points = tuple(points)
        if type(line.obj_list) == list:
            color = color_ans_line
        elif line.obj_list[0] in ('H', 'V'):
            color = color_frame
        else:
            color = color_pre_line
        draw.line([coord_in_img(points[0]), coord_in_img(points[1])], color)

    for line_ in fig.lines:
        draw_line(line_)

    img.show()

    pass
