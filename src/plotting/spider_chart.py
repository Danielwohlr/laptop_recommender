import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.path import Path
from matplotlib.transforms import Affine2D
from matplotlib.figure import Figure



# Radar factory function
def radar_factory(num_vars, frame='circle'):
    theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

    class RadarTransform(PolarAxes.PolarTransform):
        def transform_path_non_affine(self, path):
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):
        name = 'radar'
        PolarTransform = RadarTransform

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                spine = Spine(axes=self, spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5) +
                                    self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta

def concat_new_old_laptop(
        new_laptop: pd.DataFrame,
        old_laptop: pd.DataFrame,
    ) -> pd.DataFrame:
    comparison_closest_mine = pd.concat([new_laptop,old_laptop], axis=0)
    comparison_closest_mine = comparison_closest_mine.T
    comparison_closest_mine.columns = comparison_closest_mine.iloc[0]  # Use the first row as the header
    comparison_closest_mine = comparison_closest_mine[1:]

    return comparison_closest_mine.T

def plot_spider_chart(
        new_laptop: pd.DataFrame,
        my_laptop: pd.DataFrame,
    ) -> str:
    """
    Plot spider chart with statistics of my_laptop and new_laptop.
    Returns the file path of the saved chart.
    """
    df = concat_new_old_laptop(new_laptop, my_laptop)

    # Number of metrics
    num_vars = df.shape[1]
    theta = radar_factory(num_vars, frame='polygon')

    # Extract data for the radar chart
    spoke_labels = df.columns
    values_new_laptop = df.iloc[0,:].values # first row
    values_my_laptop = df.iloc[1,:].values # second row

    # Radar chart
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='radar'))
    ax.set_varlabels(spoke_labels)
    for label in ax.get_xticklabels():
        if label.get_text() in ['Storage space', 'Battery Life', 'Camera Quality', 'Indestructibility']:
            label.set_position((label.get_position()[0], label.get_position()[1] - 0.1))

    # Plot each dataset
    ax.plot(theta, values_new_laptop, label='Suggested Laptop', color='blue', linewidth=2)
    ax.fill(theta, values_new_laptop, color='blue', alpha=0.25)

    ax.plot(theta, values_my_laptop, label='Ideal Laptop', color='orange', linewidth=2)
    ax.fill(theta, values_my_laptop, color='orange', alpha=0.25)

    ax.set_yticks([])


    # Add title and legend
    ax.set_title('Laptop Comparison', weight='bold', size=16, position=(0.5, 1.2))
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

    # Save the figure to a file
    output_dir = os.path.join(os.path.dirname(__file__), '../../static/images')
    os.makedirs(output_dir, exist_ok=True)

    # Save the figure
    file_path = os.path.join(output_dir, "spider_chart.png")
    fig.savefig(file_path, bbox_inches='tight')  # Ensure the whole figure, including legend, is saved
    plt.close(fig)

    return os.path.relpath(file_path, start=os.path.dirname(__file__))
