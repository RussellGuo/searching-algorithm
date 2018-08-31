from fractions import Fraction

from PIL import Image, ImageDraw, ImageColor

from figure import Figure
from geo import Point, Line


def draw_result(fig: Figure, target_point: Point):
    grid_size = 100
    line_width = 1
    grid_count = 6
    margin = 10
    total_size = margin * 2 + grid_count * grid_size + line_width

    color_background = ImageColor.colormap["whitesmoke"]
    color_frame      = ImageColor.colormap["darkgrey"]
    color_pre_line   = ImageColor.colormap["darkred"]
    color_ans_line   = ImageColor.colormap["darkblue"]
    color_key_point  = ImageColor.colormap["yellow"]

    radius_key_point = 5

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
        if type(line.obj_tuple) == tuple:
            color = color_ans_line
            width = 3
        elif line.obj_tuple[0] in ('H', 'V'):
            color = color_frame
            width = 1
        else:
            color = color_pre_line
            width = 2
        draw.line([coord_in_img(points[0]), coord_in_img(points[1])], color, width)

    for line_ in fig.lines:
        draw_line(line_)

    def draw_point_cascade(e):
        if type(e) is Point:
            pos = coord_in_img(e)
            r = radius_key_point
            draw.ellipse( (pos[0] - r, pos[1] - r, pos[0] + r, pos[1] + r), color_key_point)
        if type(e.obj_tuple) is tuple:
            draw_point_cascade(e.obj_tuple[1])
            draw_point_cascade(e.obj_tuple[2])
        pass

    draw_point_cascade(target_point)

    img.show()

    pass
