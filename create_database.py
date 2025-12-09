"""
Create SQLite database with Palmer Penguins dataset
"""
import sqlite3
import pandas as pd
import seaborn as sns
from datetime import datetime, timedelta
import random

def create_penguins_database():
    """Create SQLite database with Palmer Penguins data"""
    print("Creating Palmer Penguins database...")
    
    # Load Palmer Penguins dataset
    penguins = sns.load_dataset('penguins')
    penguins = penguins.dropna()  # Remove rows with missing values
    
    # Add synthetic temporal and researcher info
    base_date = datetime(2007, 11, 1)
    researchers = ['Dr. Gorman', 'Dr. Williams', 'Dr. Fraser', 'Dr. Palmer']
    
    penguins['observation_date'] = [
        (base_date + timedelta(days=random.randint(0, 1095))).strftime('%Y-%m-%d')
        for _ in range(len(penguins))
    ]
    penguins['researcher'] = [random.choice(researchers) for _ in range(len(penguins))]
    
    # Create database
    conn = sqlite3.connect('data/penguins.db')
    
    # Main penguins table
    penguins.to_sql('penguins', conn, if_exists='replace', index=False)
    
    # Create species metadata table
    species_info = pd.DataFrame([
        {'species': 'Adelie', 'scientific_name': 'Pygoscelis adeliae', 
         'habitat': 'Rocky coastlines', 'avg_lifespan_years': 15},
        {'species': 'Chinstrap', 'scientific_name': 'Pygoscelis antarcticus',
         'habitat': 'Rocky islands', 'avg_lifespan_years': 20},
        {'species': 'Gentoo', 'scientific_name': 'Pygoscelis papua',
         'habitat': 'Coastal plains', 'avg_lifespan_years': 13}
    ])
    species_info.to_sql('species_info', conn, if_exists='replace', index=False)
    
    # Create island metadata table
    island_info = pd.DataFrame([
        {'island': 'Torgersen', 'area_km2': 1.59, 'latitude': -64.77, 'longitude': -64.07},
        {'island': 'Biscoe', 'area_km2': 28.33, 'latitude': -65.43, 'longitude': -65.50},
        {'island': 'Dream', 'area_km2': 0.93, 'latitude': -64.73, 'longitude': -64.23}
    ])
    island_info.to_sql('island_info', conn, if_exists='replace', index=False)
    
    conn.commit()
    conn.close()
    
    print(f"✓ Database created: data/penguins.db")
    print(f"✓ Loaded {len(penguins)} penguin observations")
    print(f"✓ Species: {penguins['species'].unique().tolist()}")
    print(f"✓ Islands: {penguins['island'].unique().tolist()}")
    print(f"✓ Sex distribution: {penguins['sex'].value_counts().to_dict()}")
    print()

if __name__ == '__main__':
    create_penguins_database()

