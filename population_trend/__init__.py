"""A population growth model package"""

__version__ = "6.0.0"
from .calculate_growth_rates import (  # noqa
    calculate_growth_rates_table,
    set_axis_plot_config,
    fit_population_model,
)
from .cli import (  # noqa
    render_population_trend,
    write_bootstrap_intervals_json,
)
