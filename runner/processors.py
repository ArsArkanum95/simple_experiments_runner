import itertools


def process_flags_in_args(args, experiment_id):
    return {k: (experiment_id if v == '$id' else v) for k, v in args.items()}


def process_exp_info(run_info, values, default_values=None):
    if default_values is None:
        default_values = {}

    if 'grid_search' in run_info:
        yield from _process_run_level(
            run_info['grid_search'],
            _process_grid_search,
            values,
            default_values
        )

    if 'individual_search' in run_info:
        yield from _process_run_level(
            run_info['individual_search'],
            _process_individual_search,
            values,
            default_values
        )


def _process_run_level(run_info, search_method, values, default_values):
    if isinstance(run_info, dict):
        for arg_vals in search_method(run_info['args'], values, default_values):
            yield from process_exp_info(
                run_info, values, {**default_values, **arg_vals})
    else:
        yield from search_method(run_info, values, default_values)


def _process_grid_search(keys, values, default_values):
    vals = (([default_values[k]] if k in default_values else []) + values[k]
            for k in keys)
    for arg_vals in itertools.product(*vals):
        yield {**default_values, **dict(zip(keys, arg_vals))}


def _process_individual_search(keys, values, default_values):
    for k in keys:
        for v in ([default_values[k]] if k in default_values else []) + values[k]:
            yield {**default_values, k: v}
