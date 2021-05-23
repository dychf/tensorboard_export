from tensorboard.backend.event_processing import event_accumulator
import argparse
import pandas as pd
from tqdm import tqdm
from defaults import _C as cfg
import os


def main():
    parser = argparse.ArgumentParser(description='Export tensorboard data as asv')
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

    for tf_log_file in cfg.INPUT_FILE:
        event_data = event_accumulator.EventAccumulator(
            tf_log_file['FILE_NAME'])
        event_data.Reload()
        keys = event_data.scalars.Keys()
        df = pd.DataFrame(columns=keys[:])
        for key in tqdm(keys):
            df[key] = pd.DataFrame(event_data.Scalars(key)).value

        df.to_csv(save_dir + '/' + tf_log_file['NEW_NAME'])

    print("Tensorboard data exported successfully")


if __name__ == '__main__':
    main()
