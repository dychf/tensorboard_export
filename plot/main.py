from tensorboard.backend.event_processing import event_accumulator
import argparse
import pandas as pd
from defaults import _C as cfg
import os
import matplotlib.pyplot as plt
from tqdm import tqdm


def main():
    # load log data
    parser = argparse.ArgumentParser(description='Export tensorboard data')
    parser.add_argument(
        "--config-file",
        default="config.yaml",
        metavar="FILE",
        help="path to config file",
        type=str,
    )
    args = parser.parse_args()
    cfg.merge_from_file(args.config_file)

    save_dir = cfg.OUTPUT_DIR
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    print("img generating...")
    for plot in cfg.PLOTS:
        with plt.style.context(plot['TEMPLATE']):
            fig, ax = plt.subplots()
            for input_file in tqdm(plot['INPUT_FILES']):
                event_data = event_accumulator.EventAccumulator(input_file['FILE_NAME'])
                event_data.Reload()
                data = pd.DataFrame(event_data.Scalars(plot['KEY'])).value

                ax.plot(data, label=input_file['LABEL'])
            ax.set(xlabel=plot['X_LABEL'])
            ax.set(ylabel=plot['Y_LABEL'])
            plt.legend(title=plot['LEGEND'], edgecolor='k')
            plt.title(plot['TITLE'])
            ax.autoscale(tight=True)
            fig.savefig(cfg.OUTPUT_DIR + '/' + plot['SAVE_NAME'], dpi=300)
    print(f"done! Images has been saved to directory --> {cfg.OUTPUT_DIR}")


if __name__ == '__main__':
    main()
