# Tableau Dashboard Replication: Real GDP Growth Visualization

A Tableau project replicating the IMF's GDP Growth dashboard using provided data. This project demonstrates proficiency in data visualization and Tableau dashboard design.

### Final results: **[imf_workbook on Tableau Public](https://public.tableau.com/views/imf_workbook/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)**

## Project Structure

- `imf_workbook.twbx` - Tableau workbook containing the replicated dashboard.
- `data/` - Contains the data files.
  - `processed/`
    - `IMF Data full.csv` - Final processed dataset with all data (Country, Regions, Analytical groups).
    - `IMF Data.csv` - Temp processed dataset with partial data (only Country and Regions).
  - `processed_norm/`
    - `IMF Data normalized_country_t.csv` - Normalized table of countries.
    - `IMF Data normalized_region_t.csv` - Normalized table of regions.
    - `IMF Data normalized_country_regions_t.csv` - Normalized table of countries and their respective regions.
    - `IMF Data normalized_country_analyticalgroups_t.csv` - Normalized table of countries and their respective analytical groups.
    - `IMF Data normalized_countries_growth_t.csv` - Normalized table of countries GDP growth over the years.
    - `IMF Data normalized_regions_growth_t.csv` - Normalized table of regions GDP growth over the years.
    - `IMF Data normalized_analytical_groups_growth_t.csv` - Normalized table of analytical groups GDP growth over the years.
  - `raw/`
    - `IMF Data analytical-groups.csv` - Export of Analytical groups.
    - `IMF Data analytical-groups.xls` - Input dataset.
    - `IMF Data regions.csv` - Export of Regions sheet.
    - `IMF Data.xlsx` - Input dataset.
- `notebooks/` - 
  - `main_notebook_analytical_groups.ipynb`
  - `main_notebook_normalize.ipynb`
  - `main_notebook.ipynb`
- `pipelines/` - Contains the data pipelines.
  - `process_all_from_excel_normalized.py` - Pipeline that expands `IMF Data.xlsx` and `IMF Data analytical-groups.xls` files into normalized `.csv` files stored in `/data/processed_norm/`
  - `process_all_from_excel.py` - Pipeline that merges `IMF Data.xlsx` and `IMF Data analytical-groups.xls` files into singular processed `.csv`
  - `process_all.py` - Pipeline that merges all three raw `.csv` files into singular processed `.csv`
  - `process_countries_regions.py` - Temp pipeline that merges countries and regions `.csv` files into singular processed `.csv`
- Reference: [IMF Dashboard](https://www.imf.org/external/datamapper/NGDP_RPCH@WEO/OEMDC/ADVEC/WEOWORLD)

## Implementation Notes

This project involved analyzing the dataset and recreating a detailed dashboard similar to the IMF's example using Tableau. The data preparation has been automated using Python scripts that process merge the data.

### Key Features

- **Dynamic World Map**:
  - Interactive choropleth map displaying real GDP growth rates by country for a selected year.
  - Countries are color-coded into categories (e.g., >6%, 3–6%, 0–3%, <0%, and "no data").

- **Trend Line Chart**:
  - Historical and forecasted trends of GDP growth (1990-2023).

- **Selection List**:
  - A sortable list of countries, regions, or analytical groups with corresponding GDP growth rates for the selected year.

- **Interactive Filters**:
  - Year filter to adjust the map and corresponding data points dynamically.
  - Options to toggle between country, region, and analytical group categories.

### Development Process

1. **Data Preparation**:
   - The original Excel datasets (`IMF Data.xlsx` and `IMF Data analytical-groups.xls`) are processed and merged into a final CSV (`data/processed/IMF Data full.csv.csv`) using `scripts/process_all_from_excel.py`.
   - The `scripts` directory contains the python files for data processing.
   - This combined dataset is then imported into Tableau.
   - Data cleaning and transformations are performed using the python scripts to align with visualization requirements.

2. **Dashboard Design**:
   - Replicated the visual elements:
     - Choropleth map for country-wise GDP growth.
     - Line chart for historical and forecasted trends.
   - Ensured interactivity between the filters, map, and charts.

3. **Validation**:
   - Compared the replicated dashboard with the IMF reference to ensure design and data accuracy.

### Development Environment

- **Visualization Tool**: Tableau Desktop
- **Data Source**: Merged CSV (`data/merged_data.csv`) created by provided data processing scripts.
- **Reference Dashboard**: IMF Datamapper Tool

---

This project highlights advanced Tableau skills and the ability to replicate professional-grade dashboards with precision, providing insights into real GDP growth trends. The data preparation has been automated with Python scripts that handle downloading, processing, and merging of the data.