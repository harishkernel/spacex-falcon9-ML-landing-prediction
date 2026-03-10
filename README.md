# SpaceX Falcon 9 First Stage Landing Prediction
> **Data Science Capstone Project** — An end-to-end machine learning pipeline to predict whether SpaceX's Falcon 9 first stage will successfully land, enabling cost estimation for rocket launches.

---

## 📌 Project Overview

SpaceX advertises Falcon 9 rocket launches at **$62 million**, compared to competitors who charge over **$165 million**. The key cost advantage is the reusability of the Falcon 9 first stage. This project builds a **binary classification model** to predict first-stage landing success, which directly informs launch cost estimates.

---

## 🗂️ Project Structure

```
Capstone-main/
│
├── 📁 Notebook/
│   ├── Data collect API notebook.ipynb          # SpaceX REST API data collection
│   ├── Web Scraping notebook.ipynb              # Wikipedia HTML table scraping
│   ├── Data wrangling.ipynb                     # Cleaning & labelling training data
│   ├── EDA.ipynb                                # Visual EDA with Matplotlib & Seaborn
│   ├── EDA-SQL.ipynb                            # SQL-based EDA with ibm_db / SQLite
│   ├── folium.ipynb                             # Geospatial analysis with Folium
│   └── SpaceX_Machine Learning Prediction_Part_5.ipynb  # Model training & evaluation
│
├── 📁 csv/
│   ├── dataset_part_1.csv                       # Raw API data
│   ├── dataset_part_2.csv                       # Cleaned data with class labels
│   ├── dataset_part_3.csv                       # Feature-engineered data for ML
│   └── spacex_web_scraped.csv                   # Wikipedia scraped launch records
│
├── spacex_dash_app.py                           # Interactive Plotly Dash dashboard
├── requirements.txt                             # Python dependencies
└── README.md
```

---

## 🔬 Methodology

### 1. Data Collection
- **SpaceX REST API** (`/launches/v4/`) — Pulled structured launch records including payload mass, orbit, booster version, and landing outcomes.
- **Web Scraping (BeautifulSoup)** — Scraped Falcon 9 launch history from Wikipedia as a supplementary dataset.

### 2. Data Wrangling
- Handled missing `PayloadMass` values using column mean imputation.
- Created a binary `Class` label: `1` = successful landing, `0` = failed landing.
- Verified class balance: **~66.7% success rate** in the final dataset.

### 3. Exploratory Data Analysis (EDA)
- **Visual EDA**: Identified launch success trends by orbit type, launch site, and payload mass using Matplotlib/Seaborn.
- **SQL EDA**: Queried aggregated stats (total payload per customer, success rate per landing pad, etc.) using SQLite.
- **Geospatial EDA**: Mapped all launch sites with Folium; visualised proximity to coastlines, equator, and railways.

### 4. Interactive Dashboard
- Built with **Plotly Dash** — includes a site-selection dropdown, payload range slider, pie chart (success distribution), and scatter plot (payload vs. success by booster version).

### 5. Machine Learning
- Standardised features with `StandardScaler`.
- Trained and tuned **4 classifiers** using `GridSearchCV` (10-fold CV):
  - Logistic Regression
  - Support Vector Machine (SVM)
  - Decision Tree
  - K-Nearest Neighbors (KNN)

---

## 📊 Key Results

| Model | CV Accuracy | Test Accuracy |
|---|---|---|
| Logistic Regression | ~84.6% | **83.3%** |
| SVM | ~84.6% | **83.3%** |
| Decision Tree | ~87.1% | **83.3%** |
| KNN | ~84.8% | **83.3%** |

> **Best Model**: Decision Tree (`criterion=entropy, max_depth=6`) — highest cross-validation score.

### Key Insights
- **KSC LC-39A** has the highest launch success rate among all sites.
- **Heavier payloads (5,000–10,000 kg)** correlate with higher landing success — likely due to newer booster versions used for heavier payloads.
- **LEO and ISS orbits** show more consistent success rates compared to GEO and HEO.
- **Flight Number** is positively correlated with success — SpaceX improved over time.
- **B5 booster** category shows the best landing performance.

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.9+ |
| Data Collection | `requests`, `BeautifulSoup4` |
| Data Processing | `pandas`, `numpy` |
| Visualisation | `matplotlib`, `seaborn`, `folium`, `plotly` |
| Dashboard | `dash` |
| Machine Learning | `scikit-learn` |
| Database | `sqlite3` / `ibm_db_sa` |
| Notebook | `jupyter` |

---

## ⚙️ Getting Started

### Prerequisites
```bash
python >= 3.9
```

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/SpaceX-Falcon9-Landing-Prediction.git
cd SpaceX-Falcon9-Landing-Prediction

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

### Running the Dashboard

```bash
python spacex_dash_app.py
```
Then open **http://127.0.0.1:8050** in your browser.

### Running the Notebooks
```bash
jupyter notebook
```
Open notebooks in the following order for end-to-end reproducibility:
1. `Data collect API notebook.ipynb`
2. `Web Scraping notebook.ipynb`
3. `Data wrangling.ipynb`
4. `EDA.ipynb`
5. `EDA-SQL.ipynb`
6. `folium.ipynb`
7. `SpaceX_Machine Learning Prediction_Part_5.ipynb`

---

## 📈 Dashboard Features

| Feature | Description |
|---|---|
| 🔽 Site Dropdown | Filter by launch site (All Sites / individual sites) |
| 🥧 Pie Chart | Success vs. failure distribution for selected site |
| 🎚️ Payload Slider | Filter scatter plot by payload range (0 – 10,000 kg) |
| 💬 Scatter Plot | Payload mass vs. landing outcome, coloured by booster version |

---

## 🧠 ML Pipeline Summary

```python
# Preprocessing
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=2)

# Hyperparameter tuning
grid_search = GridSearchCV(estimator=model, param_grid=parameters, cv=10)
grid_search.fit(X_train, Y_train)

# Evaluation
accuracy = grid_search.score(X_test, Y_test)
```

---

## 🌐 Data Sources

- [SpaceX REST API v4](https://api.spacexdata.com/v4/launches)
- [Wikipedia — List of Falcon 9 and Falcon Heavy launches](https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches)
- Skills Network hosted datasets (Data Science)

---

## 👤 Author

**Harish M**
- B.E. Electrical & Electronics Engineering | Easwari Engineering College
- Data Science Capstone Project

---

## 📄 License

This project is for educational purposes as part of the Data Science program.
