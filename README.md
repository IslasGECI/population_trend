<a href="https://www.islas.org.mx/"><img src="https://www.islas.org.mx/img/logo.svg" align="right" width="256" /></a>
# Population trend
[![codecov](https://codecov.io/gh/IslasGECI/population_trend/graph/badge.svg)](https://codecov.io/gh/IslasGECI/population_trend)
![example branch
parameter](https://github.com/IslasGECI/population_trend/actions/workflows/actions.yml/badge.svg)
![licencia](https://img.shields.io/github/license/IslasGECI/population_trend)
![languages](https://img.shields.io/github/languages/top/IslasGECI/population_trend)
![commits](https://img.shields.io/github/commit-activity/y/IslasGECI/population_trend)
![GitHub contributors](https://img.shields.io/github/contributors/IslasGECI/population_trend)

## Descripción breve
Este paquete calcula y visualiza tendencias poblacionales a partir de datos de conteos y series de tiempo, y genera intervalos de crecimiento para evaluar cambios poblacionales en islas y regiones.

En términos simples: recibe una tabla de conteos de nidos por temporada, calcula si la población crece, se mantiene o disminuye, y produce gráficas y archivos JSON con los intervalos de confianza del crecimiento.

El comando que ejecuta el paquete es `population-trend`.

## Instalación
Desde la raíz del repositorio:

```bash
pip install --editable .
```

## Cómo se usa
Primero consulta los comandos disponibles:

```bash
population-trend --help
```

Después ejecuta el comando que necesites, por ejemplo para generar la gráfica de tendencia poblacional de una isla:

```bash
population-trend render-population-trend \
  --data-path tests/data/gumu_guadalupe_data.csv \
  --intervals-path tests/data/gumu_guadalupe_boostrap_intervals.json \
  --island Guadalupe
```

El resultado es una imagen PNG con la tendencia poblacional y su intervalo de crecimiento. Cada comando de la siguiente lista acepta `--help` para mostrar sus opciones.

## Funciones CLI
El paquete expone las siguientes funciones de línea de comandos desde `population_trend/cli.py`:

- `write_bootstrap_intervals_json`: escribe un JSON con intervalos bootstrap.
- `write_burrows_by_species_and_island`: filtra datos por especie e isla y escribe un CSV.
- `render-population-trend`: genera la gráfica de tendencia poblacional.
- `plot_population_trend_from_cpue`: grafica la tendencia poblacional a partir de CPUE.
- `write_regional_trends`: escribe un JSON con tendencias regionales.
- `plot_growth_rate`: genera una gráfica de tasas de crecimiento comparando intervalos regionales.
- `version`: imprime la versión del paquete.
