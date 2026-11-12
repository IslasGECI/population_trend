# Public interface

## Command line

### population-trend write-bootstrap-intervals-json --data-path PATH --blocks-length INT --bootstrap-number INT --variable-of-interest TEXT --alpha FLOAT --output-path PATH
Writes a JSON file with bootstrapped growth-rate intervals for one species and island.

**Parameters**
- `--data-path` (default `data/processed/gumu_guadalupe_burrows.csv`): CSV containing the nest counts.
- `--blocks-length` (default `3`): block length used for the bootstrap.
- `--bootstrap-number` (default `2000`): number of bootstrap resamples.
- `--variable-of-interest` (default `Maxima_cantidad_nidos`): count column to analyze.
- `--alpha` (default `0.05`): significance level for the intervals.
- `--output-path` (default `reports/non-tabular/gumu_guadalupe_boostrap_intervals.json`): destination JSON path.

**Returns**
Nothing; writes `intervals`, `lambda_latex_interval`, `p-values`, and `bootstrap_intermediate_distribution` to the output file.

**Errors**
Raises file and parsing errors when the CSV is missing or malformed, and key errors when `Temporada` or the requested variable is absent.

### population-trend write-burrows-by-species-and-island --data-path PATH --species TEXT --island TEXT --output-path PATH
Filters a burrows table by species and island and writes the result as CSV.

**Parameters**
- `--data-path` (default `data/processed/subset_burrows_data.csv`): source CSV.
- `--species` (default `Guadalupe Murrelet`): value matched against `Nombre_en_ingles`.
- `--island` (default `Guadalupe`): value matched against `Isla`.
- `--output-path` (default `data/processed/gumu_guadalupe_burrows.csv`): destination CSV path.

**Returns**
Nothing; writes the matching rows without the DataFrame index.

**Errors**
Raises file and parsing errors when the source is missing or malformed, and an attribute or key error when the species or island columns are absent.

### population-trend render-population-trend --data-path PATH --intervals-path PATH --island TEXT --variable-of-interest TEXT --tick-mode TEXT --show-legend / --no-show-legend --language TEXT --output-path PATH
Renders a population trend figure with its growth-rate interval.

**Parameters**
- `--data-path` (required): CSV with nest counts.
- `--intervals-path` (required): JSON with the bootstrap intervals.
- `--island` (default `Guadalupe`): island name used in the figure.
- `--variable-of-interest` (default `Maxima_cantidad_nidos`): count column to plot.
- `--tick-mode` (default `full`): `full` shows every season label; `sparse` shows every other one.
- `--show-legend` / `--no-show-legend` (default show): controls legend visibility.
- `--language` (default `english`): axis-label language, `english` or `spanish`.
- `--output-path` (default empty): destination PNG path; supply a filename.

**Returns**
Nothing; writes a transparent-background PNG.

**Errors**
Raises file and parsing errors when either input is missing or malformed, key errors when the intervals JSON lacks `lambda_latex_interval`, `intervals`, or `bootstrap_intermediate_distribution`, and key errors when `--tick-mode` or `--language` is not one of the documented values.

**Notes**
Provide `--output-path`; the empty default does not name a file. `--island Natividad` places the legend at the upper left.

### population-trend plot-population-trend-from-cpue --data-path PATH --intervals-path PATH --variable-of-interest TEXT --output-path PATH
Renders a population trend from catch-per-unit-effort data.

**Parameters**
- `--data-path` (required): CSV with CPUE observations.
- `--intervals-path` (required): JSON with the bootstrap intervals.
- `--variable-of-interest` (required): CPUE column to plot.
- `--output-path` (required): destination PNG path.

**Returns**
Nothing; writes a transparent-background PNG with the smooth confidence zone, fitted model, observations, and growth-rate annotation.

**Errors**
Raises file and parsing errors when either input is missing or malformed, and key errors when the data or intervals JSON lacks a required column or field.

### population-trend write-regional-trends --config-path PATH --region TEXT --regional-trend-path PATH --alpha FLOAT
Writes a JSON file with the growth-rate intervals for a region.

**Parameters**
- `--config-path` (default `data/processed/gumu_guadalupe_burrows.json`): JSON config mapping region names to `paths` lists.
- `--region` (default empty): region key to aggregate; supply a region.
- `--regional-trend-path` (default empty): destination JSON path; supply a filename.
- `--alpha` (default `0.05`): significance level for the intervals.

**Returns**
Nothing; writes `intervals`, `lambda_latex_interval`, `p-values`, `bootstrap_intermediate_distribution`, and the Spanish and English hypothesis-test statements.

**Errors**
Raises file and parsing errors when the config or a referenced intervals file is missing or malformed, and key errors when the region key or a required field is absent.

**Notes**
Each referenced file must already contain a `bootstrap_intermediate_distribution`.

### population-trend plot-growth-rate --intervals-california PATH --intervals-pacific PATH --output-path PATH
Plots growth-rate intervals for the Gulf of California and Pacific regions.

**Parameters**
- `--intervals-california` (required): JSON with the Gulf of California intervals.
- `--intervals-pacific` (required): JSON with the Pacific intervals.
- `--output-path` (required): destination PNG path.

**Returns**
Nothing; writes a transparent-background PNG with error bars and a reference line at a growth rate of 1.

**Errors**
Raises file and parsing errors when either JSON is missing or malformed, and key errors when an `intervals` field is absent.

### population-trend version
Prints the installed package version.

**Parameters**
None.

**Returns**
Nothing; prints the version number.

## Python package

### calculate_growth_rates_table(bootstrap)
Builds the row of growth-rate values for one species and island.

**Parameters**
- `bootstrap`: a configured `Bootstrap_from_time_series_parametrizer` holding the data, count column, block length, number of resamples, and alpha.

**Returns**
A 13-item list: season interval, first observed count with season, last observed count with season, last modeled count with season, lambda LaTeX interval, latitude, central lambda, lower delta, upper delta, percent change, p-value for growth, p-value for decline, and monitored seasons.

**Errors**
Raises key and parsing errors when the configured data lacks `Temporada`, the chosen count column, or `Latitud`.

**Notes**
The lower and upper deltas are formatted as signed strings, and the percent change is wrapped in braces.

### set_axis_plot_config(ax)
Applies the standard population-trend axis styling.

**Parameters**
- `ax`: Matplotlib axes to format.

**Returns**
Nothing.

**Notes**
Sets integer x-axis ticks, hides the top and right spines, rotates y-axis labels, and labels the axes in Spanish.

### fit_population_model(seasons_series, data_series)
Fits a power-law population model and returns modeled counts.

**Parameters**
- `seasons_series`: series of seasons.
- `data_series`: series of observed counts for the same seasons.

**Returns**
The modeled counts over the supplied seasons, measured from the first season.

**Errors**
Raises an error when the series cannot be used to fit the model.

### write_bootstrap_intervals_json(data_path="data/processed/gumu_guadalupe_burrows.csv", blocks_length=3, bootstrap_number=2000, variable_of_interest="Maxima_cantidad_nidos", alpha=0.05, output_path="reports/non-tabular/gumu_guadalupe_boostrap_intervals.json")
Writes a JSON file with bootstrapped growth-rate intervals for one species and island.

**Parameters**
- `data_path`: CSV containing the nest counts.
- `blocks_length`: block length used for the bootstrap.
- `bootstrap_number`: number of bootstrap resamples.
- `variable_of_interest`: count column to analyze.
- `alpha`: significance level for the intervals.
- `output_path`: destination JSON path.

**Returns**
Nothing; writes `intervals`, `lambda_latex_interval`, `p-values`, and `bootstrap_intermediate_distribution`.

**Errors**
Raises file and parsing errors when the CSV is missing or malformed, and key errors when `Temporada` or the requested variable is absent.

### render_population_trend(data_path, intervals_path, island="Guadalupe", variable_of_interest="Maxima_cantidad_nidos", tick_mode="full", show_legend=True, language="english", output_path="")
Renders a population trend figure with its growth-rate interval.

**Parameters**
- `data_path`: CSV with nest counts.
- `intervals_path`: JSON with the bootstrap intervals.
- `island`: island name used in the figure.
- `variable_of_interest`: count column to plot.
- `tick_mode`: `full` shows every season label; `sparse` shows every other one.
- `show_legend`: whether to display the legend.
- `language`: axis-label language, `english` or `spanish`.
- `output_path`: destination PNG path; supply a filename.

**Returns**
Nothing; writes a transparent-background PNG.

**Errors**
Raises file and parsing errors when either input is missing or malformed, key errors when the intervals JSON lacks a required field, and key errors when `tick_mode` or `language` is not one of the documented values.
