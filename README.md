# Galamsay Activity Analysis System

This project provides an automated tool for analyzing illegal small-scale mining (Galamsay) data in Ghana. It cleans raw dataset inputs, performs statistical analysis, logs results into a SQLite database, and exposes the data via a RESTful API.

## Features
- **Data Cleaning**: Automatically handles non-numeric values (e.g., "eleven"), missing cities/regions, and negative site counts.
- **Automated Analysis**: Calculates total sites, identifies the highest-activity region, computes regional averages, and filters high-risk cities.
- **Database Logging**: Every analysis run is stored as a JSON log in `galamsay_analysis.db`.
- **REST API**: Exposes the latest analysis results via a JSON endpoint.

## Setup Instructions

1. **Prerequisites**: 
   Ensure you have Python 3.x installed.
   
2. **Install Dependencies**:
   Open your terminal and run:
   ```bash

   pip install pandas openpyxl flask

3. **Run the Script:**
    python main.py
    python main2.py


4. **Access the Results: Once the server starts, open your browser and go to:**
    http://127.0.0.1:5000/api/results

**API Endpoints**
GET /api/results: Returns the latest analysis results including total sites, regional averages, and cities exceeding the threshold of 10 sites.
