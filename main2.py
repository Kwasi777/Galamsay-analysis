import pandas as pd
import sqlite3
import json
from flask import Flask, jsonify
import os

# Configuration
FILE_PATH = r'D:\Assignment\galamsay_data.xlsx'
DB_NAME = 'galamsay_analysis.db'

app = Flask(__name__)

# --- MODULAR FUNCTIONS ---

def clean_data(df):
    """Cleans numeric and missing values."""
    def parse_numeric(val):
        word_map = {'eleven': 11, 'ten': 10, 'five': 5}
        val_str = str(val).strip().lower()
        if val_str in word_map: return word_map[val_str]
        try:
            return abs(float(val))
        except:
            return 0
    
    df['Number_of_Galamsay_Sites'] = df['Number_of_Galamsay_Sites'].apply(parse_numeric)
    df['City'] = df['City'].fillna('Unknown')
    df['Region'] = df['Region'].fillna('Unknown')
    return df

def save_to_log(analysis_results):
    """Saves analysis summary as a log entry in the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Create log table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS analysis_logs 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                       results_json TEXT)''')
    
    # Insert results as a JSON string
    cursor.execute("INSERT INTO analysis_logs (results_json) VALUES (?)", 
                   (json.dumps(analysis_results),))
    conn.commit()
    conn.close()

# --- API ENDPOINTS ---

@app.route('/api/results', methods=['GET'])
def get_results():
    """Exposes the latest analysis from the database log."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT results_json FROM analysis_logs ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return jsonify(json.loads(row[0]))
    return jsonify({"error": "No data found"}), 404

# --- MAIN EXECUTION ---

if __name__ == "__main__":
    # 1. Load and Clean
    raw_df = pd.read_excel(FILE_PATH, engine='openpyxl')
    df = clean_data(raw_df)

    # 2. Perform Analysis
    results = {
        "total_sites": float(df['Number_of_Galamsay_Sites'].sum()),
        "highest_region": df.groupby('Region')['Number_of_Galamsay_Sites'].sum().idxmax(),
        "average_per_region": df.groupby('Region')['Number_of_Galamsay_Sites'].mean().to_dict(),
        "cities_above_10": df[df['Number_of_Galamsay_Sites'] > 10]['City'].tolist()
    }

    # 3. Save to Database Log
    save_to_log(results)
    print(f"Analysis saved to {DB_NAME}. Starting API server...")

    # 4. Start API (this will stay running)
    app.run(port=5000)