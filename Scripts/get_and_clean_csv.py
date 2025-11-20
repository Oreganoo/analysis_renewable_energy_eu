import pandas as pd

url = "https://ourworldindata.org/grapher/energy-consumption-by-source-and-country.csv?v=1&csvType=filtered&useColumnShortNames=false&stackMode=absolute&country=~OWID_EUR&overlay=download-data"

df = pd.read_csv(url,storage_options={'User-Agent': 'PortfolioProject/1.0'})

for col in ['Entity', 'Code']:
    df[col] = df[col].replace('<null>', 'unknown')
    df[col] = df[col].fillna('unknown')

output_file = "../Data/energy_consumption_by_source_europe.csv"
df.to_csv(output_file, index=False)
print(f"Data saved to {output_file}")

