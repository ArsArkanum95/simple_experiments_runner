import os
import os.path
import re

from .loop import experiment_loop


def perform_experiments(config_module, results_savedir, state_savedir=None):
    RUN_REGEXP = re.compile(r'RUN_\d+')
    run_names = [attr_name for attr_name in dir(config_module)
            if RUN_REGEXP.fullmatch(attr_name)]

    if not os.path.isdir(results_savedir):
        os.mkdir(results_savedir)

    if state_savedir and not os.path.isdir(state_savedir):
        os.mkdir(state_savedir)

    for run_name in run_names:
        exp_info = getattr(config_module, run_name)
        results_savesubdir = os.path.join(results_savedir, run_name)
        state_savepath = os.path.join(state_savedir, run_name) + '.state.txt' \
                         if state_savedir else None

        experiment_loop(exp_info, results_savesubdir, state_savepath)


if __name__ == '__main__':
    import argparse
    import importlib.util

    parser = argparse.ArgumentParser(description='Simple experiments runner')
    parser.add_argument('config_path')
    parser.add_argument('results_dir')
    parser.add_argument('state_dir', nargs='?', default=None)

    args = parser.parse_args()

    spec = importlib.util.spec_from_file_location(
        "experiments_config", args.config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)

    perform_experiments(config, args.results_dir, args.state_dir)
