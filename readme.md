# SRP File Processor

Python utilities for processing and reporting on data exported from SRP Online.

## Getting Started

* Built on and requires [Python 3.8.x](https://www.python.org/downloads/) (or higher)
* Developed using [Poetry](https://python-poetry.org) instead of directly using
  pip; a pip requirements file has been generated for those who do not wish to
  install poetry. Instructions for running with either will be provided below.
* These tools utilize the Excel spreadsheet exports from SRP, while logged in as
  user with access to the entire region:
  * For [Book 1 Analysis](srp_file_processor/book1.ipynb), export both the In
    Progress activities and the Completed activities. Modify the first cell in
    the notebook to refer to the correct file names.
  * For the [Grouping Report](srp_file_processor/grouping.ipynb), export the
    current Cluster Growth Profile report.

### Poetry

From this project directory, open a PowerShell prompt and run:

```bash
poetry install
```

### Pip

From this project directory, open a PowerShell prompt and run:

```bash
pip install --upgrade pip
python -m pip install --user virtualenv
python -m venv .env
.\.env\Scripts\Activate.ps1
pip install -r .\requirements.txt
```

## Running the Reports

The reports are in the form of Jupyter notebooks. There are three options for
working with the [Book 1 Analysis](srp_file_processor/book1.ipynb) and [Grouping
Report](srp_file_processor/grouping.ipynb) notebooks:

1. Open them in [Visual Studio
   Code](https://code.visualstudio.com/docs/python/jupyter-support). Be sure to
   open Code on this parent directory after running the poetry / pip install, so
   that Code can use the virtual environment.
1. [Open in a browser](https://jupyter.readthedocs.io/en/latest/running.html)
   with one of the two commands below:

   ```bash
   # if you have Poetry installed
   poetry run jupyter notebook

   # otherwise
   jupyter notebook
   ```

1. Print to an HTML file. In theory it should be possible to print directly to
   PDF, but I have not been able to configure this correctly in Windows yet. Run
   the script [export_analyzer.ps1](export_analyzer.ps1) from a PowerShell
   prompt to write out an HTML file. Note: when you save to HTML, it hides the
   code so that you only see the desired display.

## About

Built by [Stephen Fuqua](https://www.safnet.com) in support of the South Central
Region and available for re-use under terms of the [MIT license](LICENSE).
