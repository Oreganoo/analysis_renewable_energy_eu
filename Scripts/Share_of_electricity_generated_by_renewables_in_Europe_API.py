import pandas as pd

# First dataset: share_of_electricity_production_from_renewable_sources_europe
url = "https://ourworldindata.org/grapher/share-of-electricity-production-from-renewable-sources.csv?v=1&csvType=full&useColumnShortNames=true"

df = pd.read_csv(
    url,
    storage_options={'User-Agent': 'PortfolioProject/1.0'}
)

df = df.fillna('unknown')

df = df[[col for col in df.columns if not col.endswith(".1")]]

european_countries = [
    "Albania", "Austria", "Belarus",
    "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia",
    "Czechia", "Denmark", "Estonia", "Finland", "France",
    "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy",
    "Kosovo", "Latvia", "Lithuania", "Luxembourg",
    "Malta", "Moldova", "Montenegro", "Netherlands",
    "North Macedonia", "Norway", "Poland", "Portugal", "Romania",
    "Russia", "Serbia", "Slovakia", "Slovenia", "Spain",
    "Sweden", "Switzerland", "Turkey", "Ukraine",
    "United Kingdom"
]

df_europe = df[df["Entity"].isin(european_countries)].copy()

output_file = "../Data/share_of_electricity_production_from_renewable_sources_europe.csv"
df_europe.to_csv(output_file, index=False)

# Second dataset: energy_consumption_by_source_europe
url = "https://ourworldindata.org/grapher/energy-consumption-by-source-and-country.csv?v=1&csvType=filtered&useColumnShortNames=false&stackMode=absolute&country=~OWID_EUR&overlay=download-data"

df = pd.read_csv(url,storage_options={'User-Agent': 'PortfolioProject/1.0'})

for col in ['Entity', 'Code']:
    df[col] = df[col].replace('<null>', 'unknown')
    df[col] = df[col].fillna('unknown')

output_file = "../Data/energy_consumption_by_source_europe.csv"
df.to_csv(output_file, index=False)
print(f"Data saved to {output_file}")

