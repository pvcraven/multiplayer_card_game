layout = {
    "ratio": [16, 9],
    "locations": {
        "placements": {
            "x": "0%",
            "y": "25%",
            "width": "100%",
            "height": "75%",
            "color": "#9874F0",
        },
        "users": {
            "x": "0%",
            "y": "0%",
            "width": "100%",
            "height": "25%",
            "locations": {
                "user1": {
                    "x": "0%",
                    "y": "0%",
                    "width": "25%",
                    "height": "100%",
                    "color": "#73ABFF",
                },
                "user2": {
                    "x": "25%",
                    "y": "0%",
                    "width": "25%",
                    "height": "100%",
                    "color": "#5D65D9",
                },
                "user3": {
                    "x": "50%",
                    "y": "0%",
                    "width": "25%",
                    "height": "100%",
                    "color": "#AB5DD9",
                },
                "user4": {
                    "x": "75%",
                    "y": "0%",
                    "width": "25%",
                    "height": "100%",
                    "color": "#F870FA",
                },
            }
        }
    }
}


def get_value(value_string, total_size):

    if value_string == "0":
        return 0

    if value_string.endswith("%"):
        percent = int(value_string[:-1])
        return total_size * percent * .01

    elif value_string.endswith("px"):
        return int(value_string[:-2])

    else:
        raise NotImplemented("Error")


def calculate_position(start_x, start_y, screen_width, screen_height, position_name, layout):

    # Force a ratio if specified
    if "ratio" in layout:
        ratio_width, ratio_height = layout["ratio"]

        # Compare ratio to screen size, get the min so we can fit on screen
        ratio = min(screen_width / ratio_width, screen_height / ratio_height)

        # Get our display size based on this ratio
        display_width = ratio * ratio_width
        display_height = ratio * ratio_height
    else:
        display_width = screen_width
        display_height = screen_height

    # Calculate our lower-left origin
    origin_x = (screen_width - display_width) / 2
    origin_y = (screen_height - display_height) / 2

    # Fetch location
    position_data = layout["locations"][position_name]
    x = get_value(position_data["x"], display_width) + origin_x + start_x
    width = get_value(position_data["width"], display_width)
    y = get_value(position_data["y"], display_height) + origin_y + start_y
    height = get_value(position_data["height"], display_height)

    return x, y, width, height


# pos = calculate_position(1280, 720, "placements", layout)
# print(pos)
