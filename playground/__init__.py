def _convert_array_by_css_color(css_color: str) -> list:
    if css_color.startswith('rgb'):
        color_tuple = eval(css_color[css_color.find('('):])
        result = []
        if len(color_tuple) == 4:
            result.append(color_tuple[3] * 255)
        result += color_tuple[:3]
        return result
    if len(css_color) != 7 and len(css_color) != 9:
        raise ValueError('The css_color is invalid which is {0}'.format(css_color))
    i = 1
    result = []
    if len(css_color) == 9:
        result.append(int(css_color[6:8], 16))
    else:
        result.append(255)
    while i < 7:
        result.append(int(css_color[i:i + 2], 16))
        i += 2
    return result


print(_convert_array_by_css_color('rgba(82, 63, 63, 0.937)'))
