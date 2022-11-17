import os
import matplotlib.pyplot as plt


def save_plt_using_title(plot_dir: str, title: str) -> None:
    """Save plot under file with plot title as name

    :param plot_dir: Directory to save the plot in
    :param title: Title of the plot
    """
    file_path = title.lower().replace(' ', '_') + '.png'
    save_plt(os.path.join(plot_dir, file_path))


def save_plt(plot_path: str) -> None:
    """Saves the current plot under the given path

    :param plot_path: Plot path
    """
    #
    plot_path = plot_path.replace(' ', '_').replace('\n', '').strip()

    # Create the plot
    dirs, _ = os.path.split(plot_path)
    if dirs:
        os.makedirs(dirs, exist_ok=True)

    # Save the plot and clear it
    plt.tight_layout()
    plt.savefig(plot_path, bbox_inches='tight')
    plt.close()
