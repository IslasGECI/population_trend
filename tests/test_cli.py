import pandas as pd
from typer.testing import CliRunner
from population_trend import (
    app,
    write_burrows_by_species_and_island,
    obtain_name_from_regional_names,
)
import geci_test_tools as gtt


runner = CliRunner()

data_path = "tests/data/dcco_laal_gumu_burrows_data.csv"
data = pd.read_csv(data_path)
species = "Laysan Albatross"
island = "Guadalupe"
output_path = "tests/data/laal_guadalupe.csv"
intervals_path = "tests/data/gumu_guadalupe_boostrap_intervals.json"
output_figure = "tests/data/figure.png"


def test_app_plot_growth_rate():
    result = runner.invoke(
        app,
        ["plot-growth-rate", "--help"],
    )
    assert "XX" not in result.stdout
    trend_california_json_path = "tests/data/california_trend_test.json"
    trend_pacific_json_path = "tests/data/pacific_trend_test.json"
    output_figure = "tests/data/regional_figure.png"
    regional_names = "Sur, Norte"
    gtt.if_exist_remove(output_figure)
    result = runner.invoke(
        app,
        [
            "plot-growth-rate",
            "--intervals-california",
            trend_california_json_path,
            "--intervals-pacific",
            trend_pacific_json_path,
            "--output-path",
            output_figure,
            "--regional-names",
            regional_names,
        ],
    )
    assert result.exit_code == 0
    gtt.assert_exist(output_figure)
    gtt.if_exist_remove(output_figure)


def test_app_plot_population_trend():
    result = runner.invoke(
        app,
        ["plot-population-trend", "--help"],
    )
    assert "XX" not in result.stdout
    assert "[default: Guadalupe]" in result.stdout
    assert "[default: Maxima_cantidad_nidos]" in result.stdout
    gtt.if_exist_remove(output_figure)
    result = runner.invoke(
        app,
        [
            "plot-population-trend",
            "--data-path",
            data_path,
            "--intervals-path",
            intervals_path,
            "--island",
            "Guadalupe",
            "--variable-of-interest",
            "Maxima_cantidad_nidos",
            "--output-path",
            output_figure,
        ],
    )
    assert result.exit_code == 0
    gtt.assert_exist(output_figure)
    gtt.if_exist_remove(output_figure)


def test_app_plot_population_trend_from_cpue():
    result = runner.invoke(
        app,
        ["plot-population-trend-from-cpue", "--help"],
    )
    assert result.exit_code == 0
    assert "Plot population trend from CPUE " in result.stdout

    output_figure_cpue = "tests/data/figure_cpue.png"
    gtt.if_exist_remove(output_figure_cpue)

    result = runner.invoke(
        app,
        [
            "plot-population-trend-from-cpue",
            "--data-path",
            data_path,
            "--intervals-path",
            intervals_path,
            "--variable-of-interest",
            "Maxima_cantidad_nidos",
            "--output-path",
            output_figure_cpue,
        ],
    )
    assert result.exit_code == 0
    gtt.assert_exist(output_figure_cpue)
    obtained_hash = gtt.calculate_hash(output_figure_cpue)
    expected_hash = "bded6eff64c524081aa88b65cc8d266d"
    assert obtained_hash == expected_hash


def test_app_write_burrows_by_species_and_island():
    result = runner.invoke(
        app,
        ["write-burrows-by-species-and-island", "--help"],
    )
    assert "[default: data/processed/subset_burrows_data.csv]" in result.stdout
    assert "[default: Guadalupe Murrelet]" in result.stdout
    assert "[default: Guadalupe]" in result.stdout
    result = runner.invoke(
        app,
        [
            "write-burrows-by-species-and-island",
            "--data-path",
            data_path,
            "--species",
            species,
            "--island",
            island,
            "--output-path",
            output_path,
        ],
    )
    assert result.exit_code == 0
    result = runner.invoke(
        app,
        ["--help"],
    )
    assert "XX" not in result.stdout


def test_app_write_bootstrap_intervals_json():
    data_gumu_path = "tests/data/gumu_guadalupe_data.csv"
    output_json = "tests/data/gumu_guadalupe_tests.json"
    result = runner.invoke(
        app,
        ["write-bootstrap-intervals-json", "--help"],
    )
    assert "[default: 3]" in result.stdout
    assert "[default: 2000]" in result.stdout
    assert "[default: 0.05]" in result.stdout
    assert " reports/non-tabular" in result.stdout
    assert " data/processed" in result.stdout

    result = runner.invoke(
        app,
        [
            "write-bootstrap-intervals-json",
            "--data-path",
            data_gumu_path,
            "--blocks-length",
            3,
            "--bootstrap-number",
            10,
            "--alpha",
            0.05,
            "--output-path",
            output_json,
        ],
    )
    assert result.exit_code == 0

    result = runner.invoke(
        app,
        [
            "write-bootstrap-intervals-json",
            "--data-path",
            data_gumu_path,
            "--blocks-length",
            3,
            "--bootstrap-number",
            10,
            "--output-path",
            output_json,
            "--variable-of-interest",
            "Cantidad de nidos",
        ],
    )
    assert result.exit_code == 0


def test_app_write_regional_trends():
    result = runner.invoke(
        app,
        ["write-regional-trends", "--help"],
    )
    assert result.exit_code == 0
    output_json = "tests/data/region_1_trends.json"
    gtt.if_exist_remove(output_json)
    result = runner.invoke(
        app,
        [
            "write-regional-trends",
            "--config-path",
            "tests/data/region_config.json",
            "--region",
            "region_1",
            "--regional-trend-path",
            output_json,
        ],
    )
    assert result.exit_code == 0
    gtt.assert_exist(output_json)
    gtt.if_exist_remove(output_json)


def test_write_burrows_by_species_and_island():
    write_burrows_by_species_and_island(data_path, species, island, output_path)
    obtained_csv = pd.read_csv(output_path)
    obtained_columns = len(obtained_csv.columns)
    expected_columns = 12
    assert obtained_columns == expected_columns

def test_obtain_name_from_regional_names():
    obtained=obtain_name_from_regional_names(None)
    expected=["Gulf of California", "Pacific"]
    assert obtained==expected