# Project: Automated Tensile Test Analyzer

## Objective

This project automates the end-to-end processing of tensile test data to produce reliable material properties, visualizations, and exportable reports while providing a reproducible, modular toolkit and an Excel integration for non-programmer workflows.

Main goals and objectives
- Automate data ingestion, validation, and preprocessing for common tensile-test formats (CSV, TXT, Excel).
- Compute engineering and true stress–strain curves and extract key properties (Young's modulus, yield strength using configurable methods, ultimate tensile strength, elongation, toughness, reduction of area).
- Provide robust error handling and input validation to flag noisy or incomplete tests and produce meaningful diagnostics.
- Offer clear visualizations (stress–strain plots, annotated property markers) suitable for publication and quick QA.
- Integrate with a master Excel workbook and an Excel add-in to enable easy import/export and batch processing by lab users.
- Include a simulation module to generate synthetic tests for method validation and unit tests to ensure correctness and reproducibility.
- Structure code as modular, well-documented scripts with a command-line interface and example Jupyter/VS Code notebook workflows.
- Deliverables: working pipeline scripts, visualization utilities, Excel add-in hooks, example datasets, automated tests, and user documentation.
- Success criteria: accurate property extraction validated against reference datasets, clear visual outputs, automated tests with CI, and accessible documentation enabling routine use by materials engineers.

## Problem Statement

Tensile testing generates critical material property data, but current lab workflows are fragmented, manual, and error-prone. Raw outputs come in diverse vendor formats (CSV, TXT, Excel) with inconsistent metadata, noisy measurements, and occasional missing segments. Manually cleaning, aligning, and analyzing each test is time-consuming and non-reproducible, leading to variability in reported properties (Young’s modulus, yield strength, UTS, elongation, toughness) between operators and labs.

Key problems to solve:
- Ingest heterogeneous file formats and discover/standardize metadata automatically.
- Robustly validate and preprocess noisy or incomplete load-displacement/time data (filtering, baseline correction, gauge length handling).
- Compute engineering and true stress–strain curves and extract properties using configurable, well-documented algorithms (multiple yield detection methods, fitting windows for modulus).
- Provide clear diagnostics and failure flags when tests are unreliable (e.g., slippage, poor gauge alignment, sensor saturation).
- Produce publication-quality visualizations and annotated outputs that support QA and reporting.
- Integrate with Excel workflows so non-programmer lab users can import/export and batch-process results without scripting.
- Enable method validation via simulated datasets and automated unit tests to ensure consistent property extraction across updates.

This project must deliver an automated, modular, and auditable pipeline that reduces manual effort, improves result consistency, and supports routine deployment in materials-testing labs.

## Folder Structure

Top-level files provide CLI entry points, project metadata, and a notebook example, while the scripts/ directory contains modular processing steps (simulation, validation, stress–strain calculation, property extraction, and visualization). A placeholder Excel workbook in the root supports lab integration and batch workflows.

```kotlin
tensile-analyzer/
├── main.py
├── main_excel_addin.py
├── .gitignore
├── .vscode
├── tensile_analyzer_notebook.ipynb
├── README.md
├── scripts/
│   ├── material_selector.py
│   ├── simulate_data.py
│   ├── calculate_stress_strain.py
│   ├── extract_properties.py
│   ├── visualize.py
│   ├── input_validation.py
│   └── user_inputs.py   
└── Tensile_Analyzer_MasterWorkbook.xlsx (place this file manually)
```

## Dataset(s)

- MatWeb material property sheets (used to parameterize and validate the pipeline)
    - Retrieved engineering property summaries (Young's modulus, yield/UTS, elongation at break) for a small verification set:
        - Metals & metal alloys (examples used): Aluminum 6061‑T6, AISI 1020 Steel, Ti‑6Al‑4V
        - Polymers (examples used): Polycarbonate (PC), Nylon 6, polyethylene terephthalate (PET)


## Tools, Software, and Python Libraries

- IDE / Editors
    - Visual Studio Code (custom notebook support)
    - Jupyter / JupyterLab (for notebooks and examples)

- Version control / CI / packaging
    - Git, GitHub (repo + issue tracking)
    - GitHub Actions (CI)
    - setuptools / pip (packaging & distribution)
    - Docker (optional reproducible environments)

- Core Python libraries (data handling & numerics)
    - numpy
    - pandas
    - matplotlib

- Excel & reporting integration
    - Python add-on inside Excel
    - openpyxl (read/write .xlsx)

## Features

## Methodology

## Usage

## Insights and Results

## Authors

Project created by a Master's graduate student in Materials Science and Engineering to showcase data science skills with materials science knowledge.

## License

MIT License
