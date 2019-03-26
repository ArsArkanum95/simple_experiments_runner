import itertools
import re


def experiment_loop(config):
    RUN_REGEXP = re.compile(r'RUN_\d+')
    run_names = [attr_name for attr_name in dir(config)
            if RUN_REGEXP.fullmatch(attr_name)]

    for run_name in run_names:
        run_info = getattr(config, run_name)
        _process_run_info(run_info)

def _process_run_info(run_info):
    function = run_info['function']
    default_values = run_info['default_values']
    values = run_info['values']

    if 'grid_search' in run_info:
        _grid_search(run_info['grid_search'], values)

def _grid_search(keys, values):
    vals = [values[k] for k in keys]
    print(vals)



PATH = 'example_config.py'
    
import importlib.util

spec = importlib.util.spec_from_file_location("experiments_config", PATH)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

experiment_loop(config)