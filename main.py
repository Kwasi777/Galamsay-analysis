import pandas as pd
import os

# 1. Load the file
file_path = r'D:\Assignment\galamsay_data.xlsx'

def run_analysis():
    if not os.path.exists(file_path):
        print("File not found.")
        return

    # Load using the engine we just verified
    df = pd.read_excel(file_path, engine='openpyxl')

    # 2. Clean the 'Number_of_Galamsay_Sites' column
    # This converts "eleven" to 11, "abc" to 0, and handles negative numbers
    def clean_sites(val):
        word_map = {'eleven': 11, 'ten': 10, 'five': 5}
        val_str = str(val).strip().lower()
        
        if val_str in word_map:
            return word_map[val_str]
        try:
            num = float(val)
            return abs(num) # Convert -5 to 5
        except:
            return 0 # Convert "abc" to 0

    df['Number_of_Galamsay_Sites'] = df['Number_of_Galamsay_Sites'].apply(clean_sites)

    # 3. Calculations
    # Total sites
    total_sites = df['Number_of_Galamsay_Sites'].sum()

    # Region with highest sites
    region_totals = df.groupby('Region')['Number_of_Galamsay_Sites'].sum()
    highest_region = region_totals.idxmax()
    highest_value = region_totals.max()

    # Average per region
    region_averages = df.groupby('Region')['Number_of_Galamsay_Sites'].mean()

    # Cities exceeding threshold (10)
    threshold = 10
    top_cities = df[df['Number_of_Galamsay_Sites'] > threshold][['City', 'Number_of_Galamsay_Sites']]

    # 4. Display Results
    print("--- GALAMSAY ANALYSIS RESULTS ---")
    print(f"1. Total Galamsay Sites: {total_sites}")
    print(f"2. Region with Highest Activity: {highest_region} ({highest_value} sites)")
    print(f"3. Average Sites per Region:\n{region_averages}")
    print(f"\n4. Cities with more than {threshold} sites:")
    print(top_cities.to_string(index=False))

if __name__ == "__main__":
    run_analysis()