<a href="https://www.islas.org.mx/"><img src="https://www.islas.org.mx/img/logo.svg" align="right" width="256" /></a>
# Population trend
[![codecov](https://codecov.io/gh/IslasGECI/population_trend/graph/badge.svg)](https://codecov.io/gh/IslasGECI/population_trend)
![example branch
parameter](https://github.com/IslasGECI/population_trend/actions/workflows/actions.yml/badge.svg)
![licencia](https://img.shields.io/github/license/IslasGECI/population_trend)
![languages](https://img.shields.io/github/languages/top/IslasGECI/population_trend)
![commits](https://img.shields.io/github/commit-activity/y/IslasGECI/population_trend)
![GitHub contributors](https://img.shields.io/github/contributors/IslasGECI/population_trend)

Calcula y visualiza tendencias poblacionales de aves marinas a partir de conteos de nidos por temporada.

## Qué hace
El paquete recibe una tabla con los conteos de nidos de una isla o región y calcula si la población crece, se mantiene o disminuye. Con esos datos produce una imagen de la tendencia poblacional y archivos JSON con los intervalos de crecimiento, que sirven para comparar islas y regiones o para sustentar decisiones de conservación.

## Uso
Para ver todos los comandos disponibles:

```bash
population-trend --help
```

Por ejemplo, para generar la gráfica de tendencia de la isla Guadalupe:

```bash
population-trend render-population-trend \
  --data-path tests/data/gumu_guadalupe_data.csv \
  --intervals-path tests/data/gumu_guadalupe_boostrap_intervals.json \
  --island Guadalupe
```

El resultado es una imagen PNG con la tendencia y su intervalo de crecimiento.

## Antes de empezar
Necesitas una tabla CSV con los conteos de nidos por temporada y un archivo JSON con los intervalos de crecimiento. Puedes usar los archivos de ejemplo de `tests/data/`.

## Ejecutar el proyecto
### Con Docker (recomendado)
Levanta una sesión dentro del contenedor, que ya incluye las herramientas de desarrollo:

```bash
docker compose run --rm islasgeci bash
```

Dentro del contenedor, instala el paquete y consulta la ayuda:

```bash
make setup
population-trend --help
```

### De forma nativa
Necesitas Python 3.9 o posterior. Desde la raíz del repositorio:

```bash
pip install --editable .
population-trend --help
```
