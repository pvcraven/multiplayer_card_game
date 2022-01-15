def calculate_screen_data(svg_width, svg_height, screen_width, screen_height):

    # Compare ratio to screen size, get the min so we can fit on screen
    ratio = min(screen_width / svg_width, screen_height / svg_height)

    # Get our display size based on this ratio
    display_width = ratio * svg_width
    display_height = ratio * svg_height

    # Calculate our lower-left origin
    origin_x = (screen_width - display_width) / 2
    origin_y = (screen_height - display_height) / 2
    return origin_x, origin_y, ratio
