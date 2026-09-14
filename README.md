# Flood Wave Graphs

A graph-based analytical framework for identifying and analysing flood-wave
propagation patterns from multi-station water-level time series.

This repository contains the analytical implementation used in the study:

> **Graph-based flood-wave tracking from multi-station water-level time series: a case study on the Tisza River, Central Europe**  
> Zsolt Vizi, Marcell Dabis, Norbert Deák, Balázs Mindszenti, Péter Kozák, István Fehérváry  
> *Computers & Geosciences*  
> [DOI to be added after publication]

The framework represents detected water-level peaks as vertices of a directed
graph and temporally admissible downstream peak associations as edges. This
representation allows graph-defined flood waves, peak-to-peak propagation times,
and river-section-level statistics to be extracted reproducibly from long-term,
multi-station water-level records.

The repository contains the analytical framework. Plotting and visualization
utilities are maintained separately in:

https://github.com/Water-Data-driven-Research/flood-wave-graphs-visualization

## Main features

The framework provides tools for:

- detecting local water-level peaks using a configurable temporal radius;
- constructing directed graphs from temporally admissible peak associations;
- identifying graph-defined flood waves across multiple gauging stations;
- handling multiple admissible propagation paths between the same source and
  destination peaks;
- calculating flood-wave counts and peak-to-peak propagation times;
- reducing the station-level graph to selected river-section boundaries;
- deriving section-level flood-wave statistics from long-term water-level data.

## Methodological overview

For each gauging station, local water-level peaks are identified using a
parameter `delta`, which defines the temporal neighbourhood used for peak
detection.

Detected peaks form the vertices of a directed graph. Two peaks at consecutive
downstream stations may be connected if their time difference lies within the
interval defined by `alpha` and `beta`.

The main parameters are:

- `delta`: radius of the local peak-detection window;
- `alpha`: minimum admissible propagation time between consecutive stations;
- `beta`: maximum admissible propagation time between consecutive stations.

The resulting graph follows the downstream ordering of stations and is therefore
a directed acyclic graph.

Within the framework, a *flood wave* is the mathematical graph object defined
in the accompanying paper. It represents a temporally admissible association
between source and destination water-level peaks under the selected parameter
values. It should not, by itself, be interpreted as an independently verified
hydrodynamic event.

## Requirements

The project was developed with **Python 3.12**.

Python 3.12 or later is recommended.

The required packages and tested versions are listed in `requirements.txt`.

No specialized hardware or GPU is required. The analyses can be run on a
standard desktop or laptop computer or in Google Colab.

## Installation

Clone the repository:

```bash
git clone https://github.com/Water-Data-driven-Research/flood-wave-graphs.git
cd flood-wave-graphs
```

Optionally, create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\\Scripts\\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Input data

The framework operates on multi-station water-level time series together with
metadata describing the position of each gauging station along the river.

The Tisza River dataset used in the accompanying study is publicly available
from the following Google Drive folder:

https://drive.google.com/drive/folders/12pkrhybv52KpmeNYsHZRSkL9nfF3May2?usp=sharing

The folder contains the water-level data used for the analyses presented in the
paper. These data can be downloaded directly and used with the analytical
workflow provided in this repository and in the reproducibility notebook.

The analysis requires, for each gauging station:

- a station identifier or station name;
- the river-kilometre position of the station;
- the altitude of the station zero point;
- a date or time index;
- water-level observations.

The analyses presented in the paper use daily water-level records. Missing
observations are represented explicitly in the time series and are handled
according to the validity conditions defined in the methodological framework.

Historical changes in station zero-point elevation are accounted for before the
graph analysis. The water-level series used in the study are therefore
zero-point corrected so that measurements from different periods are consistent
with the most recent zero-point altitude of the corresponding station.

The supplied data and the notebooks in this repository are intended to provide
a reproducible example of the complete workflow, including peak detection,
graph construction, flood-wave extraction, graph reduction, and the calculation
of section-level propagation statistics.

## Reproducing the manuscript

The complete analysis and the plots used in the manuscript can be reproduced
using the following Google Colab notebook:

https://colab.research.google.com/drive/1KYVsda0-WIYz3PhYXWa5-dc84IPo2CC4?usp=sharing

The notebook contains the workflow used for:

- detecting water-level peaks;
- constructing the flood-wave graph;
- reducing the graph to selected river-section boundaries;
- calculating river-section-level flood-wave counts;
- calculating mean peak-to-peak propagation times;
- calculating apparent peak-to-peak propagation speeds;
- generating event-level flood-wave graphs;
- generating annual average peak-to-peak propagation-time series.

The parameter values and station selections used in the manuscript are specified
directly in the notebook.

The notebook reproduces the principal analytical outputs presented in the paper,
including:

- **Table 1:** river-section-level flood-wave statistics;
- **Figure 6:** flood-wave graph for the beginning of 2001;
- **Figure 7:** annual average peak-to-peak propagation times.

If additional manuscript figures are reproduced by the same notebook, they
should also be listed here.

## Additional notebooks

The repository also provides notebooks for running and exploring the framework.

### Analysis notebook

https://colab.research.google.com/drive/1yBTk-fi1a4ZtTmleqXJ2rZzH-eFcX53-

### Runner notebook

https://colab.research.google.com/drive/1IL5LIxccj9rISpzttPhxBUj6h4TO01RV

## Repository structure

```text
flood-wave-graphs/
├── src/              # analytical framework
├── notebook/         # example and analysis notebooks
├── .github/workflows/
├── requirements.txt
├── LICENSE
└── README.md
```

The main analytical implementation is contained in `src/`.

Visualization functionality used for the manuscript figures is provided by the
companion repository.

## Outputs

Depending on the analysis workflow, the framework can provide:

- detected peak events at individual stations;
- directed flood-wave graphs;
- graph-defined flood waves;
- peak-to-peak propagation times;
- flood-wave counts between selected stations;
- reduced graphs for predefined river sections;
- annual and section-level propagation statistics.

The visualization of these outputs is handled by the companion
`flood-wave-graphs-visualization` repository.

## Testing

Tests can be run with:

```bash
pytest
```

The repository uses `pytest` for automated testing.

## Data availability

The Tisza River water-level data used in the accompanying study are publicly
available and can be downloaded from:

https://drive.google.com/drive/folders/12pkrhybv52KpmeNYsHZRSkL9nfF3May2?usp=sharing

The data required to reproduce the analyses presented in the manuscript are
used directly in the accompanying reproducibility notebook.

## Visualization repository

The graphical tools used to generate flood-wave graphs and related outputs are
maintained separately:

**Flood Wave Graphs Visualization**

https://github.com/Water-Data-driven-Research/flood-wave-graphs-visualization

## License

This project is released under the **Apache License 2.0**.

See [LICENSE](LICENSE) for details.

## Citation

If you use this software in academic work, please cite:

```bibtex
@article{vizi_flood_wave_graphs,
  title   = {Graph-based flood-wave tracking from multi-station 
             water-level time series: a case study on the Tisza River, 
             Central Europe},
  author  = {Vizi, Zsolt and Dabis, Marcell and Deák, Norbert and
             Kozák, Péter and Fehérváry, István},
  journal = {Computers & Geosciences},
  year    = {2026},
  doi     = {[DOI]}
}
```

For the exact software version used in the publication, cite the archived
release or DOI once available.

## Contact

For questions concerning the analytical framework, please contact:

**Zsolt Vizi**  
University of Szeged, Bolyai Institute  
Email: zsvizi@math.u-szeged.hu
