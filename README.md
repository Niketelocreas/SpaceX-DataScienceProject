# SpaceX Portfolio Package

This package contains the final portfolio-ready machine-learning notebook and two versions of the launch dashboard.

## Files

- `SpaceX_Machine_Learning_Prediction_FINAL.ipynb`
  - Standard Python/Jupyter version.
  - Removes Pyodide-specific code.
  - Prevents preprocessing leakage by fitting scaling inside model pipelines.
  - Compares Logistic Regression, SVM, Decision Tree and KNN.
  - Adds a final test-accuracy comparison chart.

- `spacex_dashboard.html`
  - Self-contained interactive dashboard.
  - No Python server required.
  - Open directly in a browser or upload as a static HTML file.
  - Plotly JavaScript is embedded in the file.

- `spacex_dashboard.py`
  - Dash version of the same dashboard.
  - Suitable for local execution or deployment to a Python host such as Render.

- `spacex_launch_dash.csv`
  - Dataset used by the interactive dashboard.

- `requirements.txt`
  - Dependencies for the Dash version.

- `Procfile`
  - Gunicorn start command for simple cloud deployment.

## Run the Dash dashboard locally

```bash
pip install -r requirements.txt
python spacex_dashboard.py
```

Then open:

```text
http://127.0.0.1:8050
```

## Fastest portfolio option

For Nikado, the easiest option is `spacex_dashboard.html`.

Because it is static and self-contained, it can be uploaded to your hosting and linked from a button such as:

**Explorar dashboard**

or embedded in an iframe.

## Notebook data

The notebook downloads the two public IBM Skills Network datasets used by the original project when it runs. Run the notebook once before committing it to GitHub if you want GitHub to display the final generated plots as saved outputs.