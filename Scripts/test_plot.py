import os
import unittest
from Scripts.energy_plot import load_energy_data, prepare_energy_frames, create_area_plot


class TestEnergyPlot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_dir, "..", "Data", "energy_consumption_by_source_europe.csv")

        df = load_energy_data(data_path)
        (
            cls.df_yearly,
            cls.df_melted,
            cls.energy_cols,
            cls.source_name_map
        ) = prepare_energy_frames(df)

    def test_yearly_aggregation(self):
        """Check that yearly totals match sum of all energy columns."""
        for _, row in self.df_yearly.iterrows():
            manual_sum = row[self.energy_cols].sum()
            self.assertAlmostEqual(manual_sum, row['Total_energy'], places=5)

    def test_melted_format(self):
        """Check melted dataframe contains correct columns."""
        required_cols = ['Year', 'Total_energy', 'Source', 'Energy_TWh', 'hover_text']
        for col in required_cols:
            self.assertIn(col, self.df_melted.columns)

    def test_no_missing_years(self):
        """Check for NaN years in melted dataset."""
        self.assertFalse(self.df_melted['Year'].isna().any())

    def test_no_negative_energy(self):
        """Verify that no negative TWh values appear."""
        self.assertTrue((self.df_melted['Energy_TWh'] >= 0).all())

    def test_source_mapping(self):
        """Ensure that every source was successfully renamed."""
        allowed_names = list(self.source_name_map.values())
        for source in self.df_melted['Source'].unique():
            self.assertIn(source, allowed_names)


if __name__ == "__main__":
    unittest.main()