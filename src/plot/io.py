import os
import matplotlib.pyplot as plt


def save_plt_using_title(plot_dir: str, title: str):
    file_path = title.lower().replace(' ', '_') + '.png'
    save_plt(os.path.join(plot_dir, file_path))


def save_plt(plot_path: str):
    plot_path = plot_path.replace(' ', '_').replace('\n', '').strip()

    dirs, _ = os.path.split(plot_path)
    if dirs:
        os.makedirs(dirs, exist_ok=True)

    plt.tight_layout()
    plt.savefig(plot_path, bbox_inches='tight')
    plt.close()
