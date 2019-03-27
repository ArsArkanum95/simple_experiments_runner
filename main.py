import itertools
import os
import os.path
import pickle
import re


def perform_experiments(config_module, results_savedir, state_savedir=None):
    RUN_REGEXP = re.compile(r'RUN_\d+')
    run_names = [attr_name for attr_name in dir(config_module)
            if RUN_REGEXP.fullmatch(attr_name)]

    if not os.path.isdir(results_savedir):
        os.mkdir(results_savedir)

    if state_savedir and not os.path.isdir(state_savedir):
        os.mkdir(state_savedir)

    for run_name in run_names:
        run_info = getattr(config_module, run_name)
        results_savesubdir = os.path.join(results_savedir, run_name)
        state_savepath = os.path.join(state_savedir, run_name) + '.state.txt' \
                         if state_savedir else None

        _experiment_loop(run_info, results_savesubdir, state_savepath)

def _experiment_loop(run_info, results_savedir, state_savepath=None):
    if not os.path.isdir(results_savedir):
        os.mkdir(results_savedir)

    if state_savepath and os.path.isfile(state_savepath):
        with open(state_savepath, 'r') as f:
            state = dict((key, int(val)) for (key, val) in 
                         (line.split('\t', 1) for line in f))
        experiment_id = max(state.values())
    else:
        state = {}
        experiment_id = 0

    function = run_info['function']

    for args in _process_run_info(run_info):
        args_repr = _arg_dict_serializer(args)
        if args_repr in state:
            continue

        result = function(**args)
        experiment_id = experiment_id + 1

        result_savepath = os.path.join(results_savedir, str(experiment_id)) + \
                          '.result.pckl'
        with open(result_savepath, 'wb') as f:
            pickle.dump(result, f)

        if state_savepath:
            with open(state_savepath, 'a') as f:
                f.write(f'{args_repr}\t{experiment_id}\n')


def _arg_dict_serializer(arg_dict):
    sorted_kv_pairs = sorted(arg_dict.items())
    return ','.join(
        f'{_serializer(key)}:{_serializer(value)}'
        for key, value in sorted_kv_pairs
    )


def _serializer(obj):
    if hasattr(obj, '__name__'):
        if hasattr(obj, '__module__'):
            return f'{obj.__module__}.{obj.__name__}'
        return obj.__name__
    return repr(obj)


def _process_run_info(run_info):
    default_values = run_info['default_values']
    values = run_info['values']

    if 'grid_search' in run_info:
        yield from _process_grid_search(
            run_info['grid_search'], values, default_values)

    if 'individual_search' in run_info:
        yield from _process_individual_search(
            run_info['individual_search'], values, default_values)


def _process_grid_search(keys, values, default_values):
    vals = ([default_values[k], *values[k]] for k in keys)
    for arg_vals in itertools.product(*vals):
        yield {**default_values, **dict(zip(keys, arg_vals))}


def _process_individual_search(keys, values, default_values):
    for k in keys:
        for v in values[k]:
            yield {**default_values, k: v}



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