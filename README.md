# SpaceX Falcon 9 First-Stage Landing Prediction

An end-to-end Data Science project analysing SpaceX Falcon 9 launches and predicting whether the first stage will successfully land.

The project covers the complete workflow from data acquisition to exploratory analysis, machine-learning modelling and interactive visualization.

## Project objective

Falcon 9 launch economics depend heavily on the ability to recover and reuse the first stage.

This project investigates historical launch data and builds classification models to estimate first-stage landing success from mission and vehicle characteristics.

## Data Science workflow

### 1. Data acquisition

Launch information is collected from multiple sources using:

- SpaceX API data
- Web scraping

### 2. Data preparation

The collected data is cleaned and transformed to create a structured dataset suitable for analysis and modelling.

This includes:

- Missing-value handling
- Feature preparation
- Landing-outcome classification
- Encoding of categorical variables

### 3. Exploratory data analysis

Launch outcomes are investigated using:

- Pandas
- SQL / SQLite
- Statistical summaries
- Data visualization

The analysis explores relationships between landing success and variables such as:

- Launch site
- Payload mass
- Orbit
- Booster characteristics
- Reuse history

### 4. Geospatial analysis

Launch-site locations and surrounding geographic features are explored using interactive maps.

### 5. Machine learning

The landing outcome is treated as a binary classification problem.

The notebook compares several supervised-learning algorithms:

- Logistic Regression
- Support Vector Machine
- Decision Tree
- K-Nearest Neighbours

Hyperparameters are explored using grid search and the models are evaluated on held-out test data.

### 6. Interactive dashboard

A Dash / Plotly application provides interactive exploration of launch records.

The dashboard includes:

- Launch-site selection
- Success/failure distribution
- Payload-range filtering
- Interactive payload-versus-outcome scatter plots
- Booster-category comparison

## Repository structure

| File | Purpose |
|---|---|
| `1.0-Spacex-data-collection-api.ipynb` | API-based data collection |
| `2.0- Webscraping.ipynb` | Web scraping |
| `3.0-Spacex-Data wrangling.ipynb` | Data cleaning and preparation |
| `4.0 EDA with Data Visulization.ipynb` | Exploratory data analysis |
| `5.0 EDA with SQLlite.ipynb` | SQL-based analysis |
| `6.0 SpaceX_Machine Learning Prediction_Part_5.ipynb` | Machine-learning modelling |
| `lab_jupyter_launch_site_location.ipynb` | Geospatial launch-site analysis |
| `spacex_dash_app_finished.py` | Interactive Dash application |
| `capstone-story-JoseMariaPacheco.pdf` | Project presentation |

## Technologies

- Python
- Pandas
- NumPy
- Requests / API integration
- Web scraping
- SQL / SQLite
- Matplotlib
- Seaborn
- Plotly
- Dash
- scikit-learn
- Jupyter Notebook

## Running the dashboard

The dashboard source is available in:

```bash
spacex_dash_app_finished.py
```

It expects a local dataset named:

```text
spacex_launch_dash.csv
```

That CSV is not currently included in the repository, so the dashboard is not yet fully reproducible from a fresh clone.

Restoring or regenerating this dataset is the next recommended maintenance step.

## Background

This project was originally developed as the capstone project of the IBM Data Science Professional Certificate and has been retained as an end-to-end demonstration of the Data Science workflow.

## Project type

**Data Acquisition · EDA · SQL · Machine Learning · Interactive Visualization**
