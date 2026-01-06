import unittest
import pandas as pd
from main2 import clean_data 

class TestGalamsayAnalysis(unittest.TestCase):
    def test_cleaning_logic(self):
        data = {
            'City': ['Accra', None],
            'Region': ['Greater Accra', 'Ashanti'],
            'Number_of_Galamsay_Sites': ['eleven', -5]
        }
        df = pd.DataFrame(data)
        cleaned_df = clean_data(df)
        self.assertEqual(cleaned_df['Number_of_Galamsay_Sites'].iloc[0], 11)
        self.assertEqual(cleaned_df['Number_of_Galamsay_Sites'].iloc[1], 5)

if __name__ == '__main__':
    unittest.main()