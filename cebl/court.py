import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Rectangle


def draw_court(ax=None, color="black", lw=2, outer_lines=False):
    """
    Draw a basketball court on a matplotlib figure.

    Parameters:
    ax : matplotlib.axes._axes.Axes, optional
        The matplotlib axes to plot the court on. If None, uses the current axes.
    color : str, optional
        The color of the court lines.
    lw : float, optional
        The line width of the court lines.
    outer_lines : bool, optional
        Whether to draw the outer lines (half-court line, baseline, side lines).

    Returns:
    ax : matplotlib.axes._axes.Axes
        The axes with the court drawn.
    """

    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    hoop = Circle((250, 47.5), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((220, 40), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box of the paint (width=16ft, height=19ft)
    outer_box = Rectangle((170, 0), 160, 190, linewidth=lw, color=color, fill=False)
    # Create the inner box of the paint, width=12ft, height=19ft
    inner_box = Rectangle((190, 0), 120, 190, linewidth=lw, color=color, fill=False)

    # Create free throw top arc
    top_free_throw = Arc((250, 190), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((250, 190), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color, linestyle="dashed")
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((250, 47.5), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((30, 0), 0, 140, linewidth=lw, color=color)
    corner_three_b = Rectangle((470, 0), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    three_arc = Arc((250, 47.5), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    # Center Court
    center_outer_arc = Arc((250, 470), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    center_inner_arc = Arc((250, 470), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [
        hoop,
        backboard,
        outer_box,
        inner_box,
        top_free_throw,
        bottom_free_throw,
        restricted,
        corner_three_a,
        corner_three_b,
        three_arc,
        center_outer_arc,
        center_inner_arc,
    ]

    if outer_lines:
        # Draw the half court line, baseline, and side outbound lines
        outer_lines = Rectangle((0, 0), 500, 470, linewidth=lw, color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax
