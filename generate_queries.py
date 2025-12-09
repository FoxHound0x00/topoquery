"""
Generate diverse SQL queries that analysts might run on the penguins database
"""
import json
from typing import List, Dict, Any

def generate_sample_queries() -> List[Dict[str, Any]]:
    """Generate diverse SQL queries representing different analytical patterns"""
    
    queries = [
        # Simple species filters
        {
            'sql': 'SELECT * FROM penguins WHERE species = "Adelie"',
            'description': 'Get all Adelie penguin observations',
            'user': 'Dr. Gorman',
            'timestamp': '2024-01-15 09:00:00'
        },
        {
            'sql': 'SELECT * FROM penguins WHERE species = "Chinstrap"',
            'description': 'Get all Chinstrap penguin observations',
            'user': 'Dr. Gorman',
            'timestamp': '2024-01-15 09:05:00'
        },
        {
            'sql': 'SELECT * FROM penguins WHERE species = "Gentoo"',
            'description': 'Get all Gentoo penguin observations',
            'user': 'Dr. Williams',
            'timestamp': '2024-01-15 10:00:00'
        },
        
        # Island-based queries
        {
            'sql': 'SELECT * FROM penguins WHERE island = "Torgersen"',
            'description': 'Get all observations from Torgersen island',
            'user': 'Dr. Fraser',
            'timestamp': '2024-01-16 08:00:00'
        },
        {
            'sql': 'SELECT * FROM penguins WHERE island = "Biscoe"',
            'description': 'Get all observations from Biscoe island',
            'user': 'Dr. Fraser',
            'timestamp': '2024-01-16 08:10:00'
        },
        
        # Aggregations by species
        {
            'sql': 'SELECT species, AVG(bill_length_mm) FROM penguins GROUP BY species',
            'description': 'Average bill length by species',
            'user': 'Dr. Gorman',
            'timestamp': '2024-01-15 09:15:00'
        },
        {
            'sql': 'SELECT species, AVG(bill_depth_mm) FROM penguins GROUP BY species',
            'description': 'Average bill depth by species',
            'user': 'Dr. Gorman',
            'timestamp': '2024-01-15 09:20:00'
        },
        {
            'sql': 'SELECT species, AVG(flipper_length_mm) FROM penguins GROUP BY species',
            'description': 'Average flipper length by species',
            'user': 'Dr. Williams',
            'timestamp': '2024-01-15 10:10:00'
        },
        {
            'sql': 'SELECT species, AVG(body_mass_g) FROM penguins GROUP BY species',
            'description': 'Average body mass by species',
            'user': 'Dr. Williams',
            'timestamp': '2024-01-15 10:15:00'
        },
        
        # Count aggregations
        {
            'sql': 'SELECT species, COUNT(*) FROM penguins GROUP BY species',
            'description': 'Count observations per species',
            'user': 'Dr. Palmer',
            'timestamp': '2024-01-17 11:00:00'
        },
        {
            'sql': 'SELECT island, COUNT(*) FROM penguins GROUP BY island',
            'description': 'Count observations per island',
            'user': 'Dr. Fraser',
            'timestamp': '2024-01-16 08:30:00'
        },
        {
            'sql': 'SELECT sex, COUNT(*) FROM penguins GROUP BY sex',
            'description': 'Count observations by sex',
            'user': 'Dr. Palmer',
            'timestamp': '2024-01-17 11:10:00'
        },
        
        # Multi-dimensional aggregations
        {
            'sql': 'SELECT species, island, COUNT(*) FROM penguins GROUP BY species, island',
            'description': 'Species distribution across islands',
            'user': 'Dr. Fraser',
            'timestamp': '2024-01-16 09:00:00'
        },
        {
            'sql': 'SELECT species, sex, AVG(body_mass_g) FROM penguins GROUP BY species, sex',
            'description': 'Average body mass by species and sex',
            'user': 'Dr. Williams',
            'timestamp': '2024-01-15 10:30:00'
        },
        {
            'sql': 'SELECT island, species, AVG(bill_length_mm) FROM penguins GROUP BY island, species',
            'description': 'Average bill length by island and species',
            'user': 'Dr. Fraser',
            'timestamp': '2024-01-16 09:15:00'
        },
        
        # JOIN queries with metadata
        {
            'sql': '''SELECT p.species, s.scientific_name, AVG(p.body_mass_g) 
                     FROM penguins p JOIN species_info s ON p.species = s.species 
                     GROUP BY p.species''',
            'description': 'Average body mass with scientific names',
            'user': 'Dr. Palmer',
            'timestamp': '2024-01-17 11:30:00'
        },
        {
            'sql': '''SELECT p.island, i.area_km2, COUNT(*) 
                     FROM penguins p JOIN island_info i ON p.island = i.island 
                     GROUP BY p.island''',
            'description': 'Observation counts with island area',
            'user': 'Dr. Fraser',
            'timestamp': '2024-01-16 09:30:00'
        },
        {
            'sql': '''SELECT p.species, s.habitat, AVG(p.flipper_length_mm) 
                     FROM penguins p JOIN species_info s ON p.species = s.species 
                     GROUP BY p.species''',
            'description': 'Average flipper length with habitat info',
            'user': 'Dr. Williams',
            'timestamp': '2024-01-15 11:00:00'
        },
        
        # Filtered aggregations
        {
            'sql': 'SELECT AVG(bill_length_mm) FROM penguins WHERE body_mass_g > 4000',
            'description': 'Average bill length for heavy penguins',
            'user': 'Dr. Gorman',
            'timestamp': '2024-01-15 09:30:00'
        },
        {
            'sql': 'SELECT AVG(flipper_length_mm) FROM penguins WHERE bill_depth_mm > 18',
            'description': 'Average flipper length for deep bills',
            'user': 'Dr. Williams',
            'timestamp': '2024-01-15 10:45:00'
        },
        {
            'sql': '''SELECT species, AVG(bill_length_mm) 
                     FROM penguins 
                     WHERE body_mass_g > 3500 
                     GROUP BY species''',
            'description': 'Average bill length by species for larger penguins',
            'user': 'Dr. Gorman',
            'timestamp': '2024-01-15 09:45:00'
        },
        
        # Complex filtering
        {
            'sql': '''SELECT * FROM penguins 
                     WHERE bill_length_mm > 45 AND flipper_length_mm > 200''',
            'description': 'Find large penguins (long bill and flipper)',
            'user': 'Dr. Williams',
            'timestamp': '2024-01-15 11:15:00'
        },
        {
            'sql': '''SELECT species, COUNT(*) FROM penguins 
                     WHERE body_mass_g BETWEEN 3000 AND 4000 
                     GROUP BY species''',
            'description': 'Count medium-sized penguins by species',
            'user': 'Dr. Palmer',
            'timestamp': '2024-01-17 11:45:00'
        },
        
        # Statistical queries
        {
            'sql': 'SELECT species, MAX(body_mass_g), MIN(body_mass_g) FROM penguins GROUP BY species',
            'description': 'Body mass range by species',
            'user': 'Dr. Williams',
            'timestamp': '2024-01-15 10:20:00'
        },
        {
            'sql': 'SELECT island, MAX(bill_length_mm), MIN(bill_length_mm) FROM penguins GROUP BY island',
            'description': 'Bill length range by island',
            'user': 'Dr. Fraser',
            'timestamp': '2024-01-16 09:45:00'
        },
        
        # Researcher queries
        {
            'sql': 'SELECT researcher, COUNT(*) FROM penguins GROUP BY researcher',
            'description': 'Observation counts by researcher',
            'user': 'Dr. Palmer',
            'timestamp': '2024-01-17 12:00:00'
        },
        {
            'sql': 'SELECT researcher, species, AVG(body_mass_g) FROM penguins GROUP BY researcher, species',
            'description': 'Average body mass by researcher and species',
            'user': 'Dr. Palmer',
            'timestamp': '2024-01-17 12:10:00'
        },
        
        # Ordering queries
        {
            'sql': 'SELECT * FROM penguins ORDER BY body_mass_g DESC LIMIT 10',
            'description': 'Top 10 heaviest penguins',
            'user': 'Dr. Williams',
            'timestamp': '2024-01-15 11:30:00'
        },
        {
            'sql': 'SELECT species, bill_length_mm FROM penguins ORDER BY bill_length_mm ASC LIMIT 5',
            'description': 'Penguins with shortest bills',
            'user': 'Dr. Gorman',
            'timestamp': '2024-01-15 10:00:00'
        },
        
        # Sex-based analysis
        {
            'sql': 'SELECT sex, AVG(body_mass_g) FROM penguins GROUP BY sex',
            'description': 'Average body mass by sex',
            'user': 'Dr. Williams',
            'timestamp': '2024-01-15 11:45:00'
        },
        {
            'sql': 'SELECT species, sex, AVG(flipper_length_mm) FROM penguins GROUP BY species, sex',
            'description': 'Average flipper length by species and sex',
            'user': 'Dr. Williams',
            'timestamp': '2024-01-15 11:50:00'
        },
    ]
    
    return queries

def save_queries():
    """Generate and save queries to JSON file"""
    print("Generating sample queries...")
    queries = generate_sample_queries()
    
    with open('queries/sample_queries.json', 'w') as f:
        json.dump(queries, f, indent=2)
    
    print(f"✓ Generated {len(queries)} SQL queries")
    print(f"✓ Saved to: queries/sample_queries.json")
    
    # Print summary
    query_types = {}
    for q in queries:
        sql_upper = q['sql'].upper()
        if 'JOIN' in sql_upper:
            qtype = 'JOIN'
        elif 'GROUP BY' in sql_upper:
            qtype = 'AGGREGATION'
        elif 'WHERE' in sql_upper:
            qtype = 'FILTER'
        else:
            qtype = 'SELECT'
        query_types[qtype] = query_types.get(qtype, 0) + 1
    
    print(f"✓ Query types: {query_types}")
    print()

if __name__ == '__main__':
    save_queries()

