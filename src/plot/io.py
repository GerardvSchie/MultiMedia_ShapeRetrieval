import os
import matplotlib.pyplot as plt


def save_plt_using_title(plot_dir: str, title: str):
    file_path = title.lower().replace(' ', '_') + '.png'
    save_plt(os.path.join(plot_dir, file_path))


def save_plt(plot_path: str):
    os.makedirs(os.path.split(plot_path)[0], exist_ok=True)
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()
