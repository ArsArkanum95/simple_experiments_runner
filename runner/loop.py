import os
import os.path
import pickle

from .processors import process_exp_info
from .serializers import arg_dict_serializer


def experiment_loop(exp_info, results_savedir, state_savepath=None):
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

    function = exp_info['function']

    for args in process_exp_info(exp_info['run'], exp_info['values'],
                                  exp_info['default_values']):
        args_repr = arg_dict_serializer(args)
        if args_repr in state:
            continue

        result = function(**args)
        experiment_id = experiment_id + 1

        result_savepath = os.path.join(results_savedir, str(experiment_id)) + \
                          '.result.pckl'
        with open(result_savepath, 'wb') as f:
            pickle.dump(result, f)

        state[args_repr] = experiment_id

        if state_savepath:
            with open(state_savepath, 'a') as f:
                f.write(f'{args_repr}\t{experiment_id}\n')
