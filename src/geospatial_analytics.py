# src/geospatial_analytics.py
import pandas as pd
from shapely.geometry import Point, Polygon

# Definition of key maritime chokepoints using Shapely polygons
CHOKEPOINTS = {
    "Suez_Canal": Polygon([(31.0, 27.0), (35.0, 27.0), (35.0, 32.0), (31.0, 32.0)]),
    "Strait_of_Hormuz": Polygon([(53.0, 24.0), (58.0, 24.0), (58.0, 27.5), (53.0, 27.5)]),
    "Cape_of_Good_Hope": Polygon([(15.0, -36.0), (22.0, -36.0), (22.0, -32.0), (15.0, -32.0)])
}


def detect_chokepoints(df_ais: pd.DataFrame) -> pd.DataFrame:
    """
    Associates each AIS vessel position with a chokepoint by checking spatial containment.
    
    Parameters:
        df_ais (pd.DataFrame): Dataframe containing 'longitude' and 'latitude' columns.
        
    Returns:
        pd.DataFrame: Dataframe with an added 'chokepoint' column.
    """
    chokepoint_list = []
    
    for _, row in df_ais.iterrows():
        point = Point(row['longitude'], row['latitude'])
        found = "Open Ocean"
        
        for name, polygon in CHOKEPOINTS.items():
            if polygon.contains(point):
                found = name
                break
                
        chokepoint_list.append(found)
        
    df_ais['chokepoint'] = chokepoint_list
    return df_ais


def calculate_oil_on_water(df_ais: pd.DataFrame) -> float:
    """
    Estimates the total volume of oil at sea in Million Barrels (MMbbl).
    
    Parameters:
        df_ais (pd.DataFrame): Dataframe containing vessel status, DWT, and draft info.
        
    Returns:
        float: Total estimated oil volume in MMbbl.
    """
    df_loaded = df_ais[df_ais['nav_status'] == 'Underway']
    estimated_tons = df_loaded['dwt'] * (df_loaded['draft'] / df_loaded['max_draft'])
    total_barrels = estimated_tons.sum() * 7.33  # 1 metric ton ≈ 7.33 barrels
    return total_barrels / 1_000_000