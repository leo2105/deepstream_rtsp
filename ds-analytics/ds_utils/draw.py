import pyds
import numpy as np

def add_line_to_display_meta(display_meta, label, color, points, x_limit=None, y_limit=None):
    for j in range(len(points) - 1):
        display_meta.num_lines += 1
        line_params = display_meta.line_params[display_meta.num_lines - 1]
        line_params.line_color.set(color[0], color[1], color[2], color[3])
        line_params.line_width = 8
        line_params.x1 = points[j][0]
        line_params.x2 = points[j+1][0]
        line_params.y1 = points[j][1]
        line_params.y2 = points[j+1][1]

    add_text_to_display_meta(display_meta, label, points[0][0], points[0][1], x_limit=x_limit, y_limit=y_limit)


def add_arrow_to_display_meta(display_meta, label, color, arrow, x_limit=None, y_limit=None):
    display_meta.num_arrows += 1

    arrow_params = display_meta.arrow_params[display_meta.num_arrows - 1]
    arrow_params.arrow_color.set(color[0], color[1], color[2], color[3])
    arrow_params.arrow_head = pyds.NvOSD_Arrow_Head_Direction.END_HEAD
    arrow_params.arrow_width = 8
    arrow_params.x1 = arrow[0][0]
    arrow_params.x2 = arrow[1][0]
    arrow_params.y1 = arrow[0][1]
    arrow_params.y2 = arrow[1][1]

    add_text_to_display_meta(display_meta, label, arrow[1][0], arrow[1][1], x_limit=x_limit, y_limit=y_limit)


def add_text_to_display_meta(display_meta, label, x_offset, y_offset, font_size = 20, set_bg_clr = 1, text_color=(1.0, 1.0, 1.0, 1.0), text_bg_clr = (0.0, 0.0, 0.0, 0.6), x_limit=None, y_limit=None):
    display_meta.num_labels += 1
    text_params = display_meta.text_params[display_meta.num_labels - 1]

    if x_limit is not None:
        biggest_line = max(label.split("\n"))
        if x_offset > x_limit - (font_size * len(biggest_line)*0.8):
            x_offset = x_offset - (font_size * len(biggest_line)*0.8)
    if y_limit is not None:
        if y_offset > y_limit - (font_size * 2):
            y_offset = y_offset - (font_size * 2)

    text_params.display_text = label
    text_params.x_offset = int(x_offset)
    text_params.y_offset = int(y_offset)
    text_params.font_params.font_name = "Serif"
    text_params.font_params.font_size = font_size
    # set(red, green, blue, alpha)
    text_params.font_params.font_color.set(text_color[0], text_color[1], text_color[2], text_color[3])
    text_params.set_bg_clr = set_bg_clr
    # set(red, green, blue, alpha)
    text_params.text_bg_clr.set(text_bg_clr[0], text_bg_clr[1], text_bg_clr[2], text_bg_clr[3])


def get_random_rgba_color(alpha=0.4):
    color = np.random.rand(1,3)
    color = np.append(color, alpha)
    return tuple(color)
