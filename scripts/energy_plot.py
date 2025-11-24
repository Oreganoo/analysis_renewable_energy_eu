import pandas as pd
import plotly.express as px

def load_energy_data(path):
    """
    Load CSV and replace <null> values with 'unknown'.
    """
    df = pd.read_csv(path)
    df = df.replace('<null>', 'unknown')
    return df

def prepare_energy_frames(df):
    """
    Prepare cleaned, aggregated and melted dataframes for plotting.
    """
    energy_cols = [
        "Other renewables (including geothermal and biomass) - TWh",
        "Biofuels consumption - TWh",
        "Solar consumption - TWh",
        "Wind consumption - TWh",
        "Hydro consumption - TWh",
        "Nuclear consumption - TWh",
        "Gas consumption - TWh",
        "Coal consumption - TWh",
        "Oil consumption - TWh"
    ]

    df[energy_cols] = df[energy_cols].apply(pd.to_numeric, errors='coerce')

    df_yearly = df.groupby("Year")[energy_cols].sum().reset_index()
    df_yearly["Total_energy"] = df_yearly[energy_cols].sum(axis=1)

    df_melted = df_yearly.melt(
        id_vars=["Year", "Total_energy"],
        value_vars=energy_cols,
        var_name="Source",
        value_name="Energy_TWh"
    )

    source_name_map = {
        "Other renewables (including geothermal and biomass) - TWh": "Other renewables",
        "Biofuels consumption - TWh": "Biofuels",
        "Solar consumption - TWh": "Solar",
        "Wind consumption - TWh": "Wind",
        "Hydro consumption - TWh": "Hydropower",
        "Nuclear consumption - TWh": "Nuclear",
        "Gas consumption - TWh": "Gas",
        "Coal consumption - TWh": "Coal",
        "Oil consumption - TWh": "Oil"
    }
    df_melted["Source"] = df_melted["Source"].replace(source_name_map)

    hover_dict = {}
    for _, row in df_yearly.iterrows():
        hover = f"<b>Year: {int(row['Year'])}</b><br>"
        for col in energy_cols:
            hover += f"{source_name_map[col]}: {row[col]:,.2f} TWh<br>"
        hover += f"<b>Total: {row['Total_energy']:,.2f} TWh</b>"
        hover_dict[row["Year"]] = hover

    df_melted["hover_text"] = df_melted["Year"].map(hover_dict)

    return df_yearly, df_melted, energy_cols, source_name_map

def create_area_plot(df_melted, source_name_map):
    """
    Create and return a Plotly stacked area chart.
    """
    fig = px.area(
        df_melted,
        x="Year",
        y="Energy_TWh",
        color="Source",
        category_orders={"Source": list(source_name_map.values())},
        hover_data={"Energy_TWh": False, "Total_energy": False},
        title="Europe: Energy Consumption by Source (TWh)"
    )

    fig.update_traces(
        text=df_melted["hover_text"],
        hovertemplate="%{text}<extra></extra>"
    )

    return fig