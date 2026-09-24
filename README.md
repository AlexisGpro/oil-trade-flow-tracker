# Oil Trade Flow Tracker & AIS Pipeline

An interactive geospatial decision-support tool engineered for oil trading desks (e.g., TotalEnergies / BxT Trading) to track global crude and refined product tanker movements, detect bottlenecks at strategic maritime chokepoints, and estimate physical Oil-on-Water volumes.

## Key Features
* **Geospatial Chokepoint Detection:** Uses 2D spatial containment algorithms (Shapely polygons) to detect vessel transits through critical passages (Suez Canal, Strait of Hormuz, Cape of Good Hope).
* **Oil-on-Water Estimation:** Applies Archimedes' buoyancy principles to estimate physical cargo volume in Million Barrels (MMbbl) based on operational draft-to-max-draft immersion ratios.
* **Interactive Fleet Visualization:** Real-time interactive maps rendered with Folium distinguishing vessels underway (blue) from moored/waiting vessels (red) to highlight bottlenecking.
* **Regional Tonnage Breakdown:** Dynamic Plotly pie chart visualizations aggregating fleet capacity across geographic zones.

## Tech Stack
* **Language:** Python 3.10+
* **Framework:** Streamlit, Folium, Streamlit-Folium
* **Geospatial Analytics:** GeoPandas, Shapely, Pandas, NumPy
* **Visualization:** Plotly Express

## Local Installation & Running

1. Clone the repository:
git clone https://github.com/AlexisGpro/oil-trade-flow-tracker.git
cd oil-trade-flow-tracker

2. Install dependencies:
pip install -r requirements.txt

3. Run the Streamlit dashboard:
streamlit run app.py

## Technical Report
A full LaTeX engineering report detailing the computational geometry algorithms and hydrodynamics equations is available in the docs/ directory.