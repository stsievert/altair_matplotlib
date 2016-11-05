from altair import Chart, load_dataset
from altair_matplotlib import render
import matplotlib.pyplot as plt


def test_heatmap(show=False):
    """ A visual check that the heatmap looks appropriate """
    df = load_dataset('cars')

    c = Chart(df).mark_text().encode(
            row='Origin', column='Cylinders', text='Horsepower', color='Horsepower'
        )

    render(c)
    if show:
        plt.show()

if __name__ == "__main__":
    test_heatmap(show=True)
