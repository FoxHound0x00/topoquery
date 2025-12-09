# TopoQuery: Explainable Query Recommendations via Persistent Homology

**Topological data analysis of SQL queries using the HOLE library**

A novel query recommendation system that leverages persistent homology to identify multi-scale topological patterns in SQL workloads and generate explainable recommendations.

## Quick Start

```bash
# 1. Setup
cd topoquery-system
python3 -m venv venv
source venv/bin/activate
pip install numpy scipy scikit-learn matplotlib seaborn sqlparse networkx loguru gudhi tqdm pillow pandas

# 2. Run the complete pipeline
python run_pipeline.py

# 3. View results
ls outputs/visualizations/
cat outputs/recommendations/recommendations_summary.txt

# 4. Clean outputs (if needed)
./clean.sh
```

**Done!** Takes ~2 minutes. Generates 14 visualizations and topological recommendations.

---

## What This Does

Applies **persistent homology** (via HOLE library) to analyze SQL query patterns and generate explainable recommendations based on topological similarity.

### The Pipeline

1. **Create Database** - Palmer Penguins dataset (333 observations) in SQLite
2. **Generate Queries** - 31 diverse SQL queries (filters, aggregations, joins)
3. **Extract Features** - Structural, semantic, and contextual features
4. **Topological Analysis** - Persistent homology using HOLE library
5. **Recommendations** - Find topologically similar queries
6. **Visualizations** - 14 plots showing topological structure

### Key Innovation

Traditional query similarity uses string matching or syntax trees. We use **persistent homology** to reveal multi-scale structure in query relationships that text-based methods miss.

---

## HOLE Library Integration

This project extensively uses **10+ functions** from the HOLE library:

### Core Persistent Homology (`hole.core.persistence`)

```python
compute_persistence()           # Computes PH using GUDHI
extract_death_thresholds()      # Gets critical distances
select_meaningful_thresholds()  # Chooses representative scales
compute_cluster_evolution()     # Tracks cluster formation
track_cluster_flows()           # Monitors cluster merging
compute_persistence_statistics()# Statistical summaries
```

### Distance Metrics (`hole.core.distance_metrics`)

```python
distance_matrix()               # Multi-metric computation
density_normalized_distance()   # Adaptive normalization
```

### Visualization (`hole.visualization`)

```python
HOLEVisualizer                  # Main analysis interface
plot_persistence_diagram()      # Birth-death plots
plot_persistence_barcode()      # Feature lifetimes
```

---

## Outputs

### 14 Visualizations (`outputs/visualizations/`)

**Persistent Homology (HOLE):**
- `persistence_diagram_*.png` (3) - Topological features (birth vs death)
- `persistence_barcode_*.png` (3) - Feature lifetimes as bars
- `heatmap_*.png` (3) - Distance matrices (darker = more similar)

**Projections:**
- `mds_projections.png` - Distance-preserving 2D views (3 metrics)
- `pca_projection.png` - Variance-based 2D view

### Recommendations (`outputs/recommendations/`)
- `recommendations.json` - Structured data
- `recommendations_summary.txt` - Human-readable examples

### Data Files
- `data/penguins.db` - SQLite database
- `queries/sample_queries.json` - Generated SQL queries
- `queries/parsed_features.json` - Feature vectors
- `outputs/topological_features.json` - Distance matrices

---

## Key Findings

From persistent homology analysis:

- **31 queries** → **4 stable clusters**
- **Mean feature lifetime:** 2-5 distance units
- **Max persistence:** 4-10 (very stable structures)
- **No loops (dim 1):** Hierarchical, not cyclic relationships
- **Multi-scale structure:** Patterns at multiple granularities

### Critical Thresholds (Euclidean example)
- **Threshold 2.48:** 29 clusters (mostly isolated queries)
- **Threshold 4.58:** 17 clusters (groups emerging)
- **Threshold 6.10:** 11 clusters (clear structure)
- **Threshold 10.09:** 1 cluster (all connected)

---

## Understanding the Visualizations

### Persistence Diagrams
- **Axes:** Birth distance (x) vs Death distance (y)
- **Meaning:** Points far from diagonal = significant features
- **Red dots:** Connected components (clusters)
- **Blue dots:** Loops (none in our data - hierarchical structure)

### Persistence Barcodes
- **Bars:** Each bar is one topological feature
- **Length:** Feature lifetime (longer = more significant)
- **Interpretation:** Count long bars to see stable clusters

### Cluster Evolution
- **Shows:** How queries connect at different thresholds
- **Dark cells:** Queries connected at that threshold
- **Label:** Number of clusters at each threshold

### Density Normalization
- **Left:** Original distances
- **Middle:** Density-normalized (HOLE function)
- **Right:** Difference (shows adjustment effect)
- **Purpose:** Handles non-uniform query distributions

---

## Example Recommendation

**Query 0:** `SELECT * FROM penguins WHERE species = "Adelie"`

**Top Recommendation (Euclidean):**
```sql
SELECT species, AVG(bill_length_mm) 
FROM penguins 
WHERE body_mass_g > 3500 
GROUP BY species
```
**Distance:** 7.867  
**Explanation:** Share columns: species; same analyst (Dr. Gorman)

---

## Project Structure

```
explainable-recs/
├── create_database.py       # Step 1: SQLite DB creation
├── generate_queries.py      # Step 2: Generate 31 queries
├── parse_queries.py         # Step 3: Feature extraction
├── topological_analysis.py  # Step 4: HOLE computations
├── recommend_queries.py     # Step 5: Recommendations
├── visualize_results.py     # Step 6: HOLE visualizations
├── run_pipeline.py          # Run all steps
├── clean.sh                 # Clean all generated files
├── README.md                # This file
├── .gitignore              
├── data/penguins.db         # Generated
├── queries/                 # Generated
└── outputs/                 # Generated
    ├── visualizations/      # 14 PNGs
    ├── recommendations/     # JSON + text
    └── INTERPRETATION_GUIDE.md
```

---

## Running Individual Steps

Instead of `run_pipeline.py`, you can run steps individually:

```bash
python create_database.py        # Creates penguins.db
python generate_queries.py       # Generates 31 SQL queries
python parse_queries.py          # Extracts features
python topological_analysis.py   # Computes distances (HOLE)
python recommend_queries.py      # Generates recommendations
python visualize_results.py      # Creates visualizations (HOLE)
```

---

## Dependencies

```
numpy>=1.21.0
scipy>=1.7.0
scikit-learn>=1.0.0
matplotlib>=3.5.0
seaborn>=0.12.0
networkx>=2.6.0
sqlparse
pandas

# For HOLE library
gudhi>=3.5.0
loguru>=0.7.0
tqdm>=4.60.0
pillow>=9.0.0
```

---

## Troubleshooting

**Problem:** `ModuleNotFoundError`  
**Fix:** Activate venv first: `source venv/bin/activate`

**Problem:** Cannot import from HOLE  
**Fix:** Update HOLE path in `topological_analysis.py` and `visualize_results.py` line 2:
```python
sys.path.insert(0, '/your/path/to/hole')
```

**Problem:** No visualizations generated  
**Fix:** Ensure output directories exist:
```bash
mkdir -p outputs/visualizations outputs/recommendations
python visualize_results.py
```

**Problem:** Permission errors  
**Fix:** Check file permissions in project directory

---

## Why Persistent Homology?

Traditional clustering requires choosing a single distance threshold. **Persistent homology analyzes all thresholds simultaneously**, revealing:

1. **Multi-scale structure** - Queries related at multiple granularities
2. **Stability** - Which clusters are robust vs noise
3. **Hierarchy** - How clusters nest within each other
4. **Critical transitions** - Key distances where structure changes

This gives us **topologically meaningful** query recommendations instead of just syntactic similarity.

---

## Technical Details

### Query Features Extracted
- **Structural:** Tables, joins, WHERE, GROUP BY, ORDER BY, aggregations
- **Semantic:** Column types (temporal, measurement, categorical)
- **Contextual:** User, timestamp patterns

### Distance Metrics
- **Euclidean:** Overall structural similarity
- **Cosine:** Pattern direction similarity
- **Mahalanobis:** Correlation-aware similarity

### Feature Vector
Each query → 41-dimensional vector encoding all features

---

## Citation

This project uses:
- **HOLE library** - Persistent homology framework (your library)
- **Palmer Penguins dataset** - Horst, Hill, & Gorman (2020)
- **GUDHI** - Computational topology library (via HOLE)

---

## Stats

- **Code:** ~1,400 lines of clean Python
- **Scripts:** 7 modular files
- **Queries:** 31 diverse SQL patterns
- **Visualizations:** 14 using HOLE library
- **Runtime:** ~2 minutes for complete pipeline

---

**Just run `python run_pipeline.py` and explore the outputs!**

For detailed interpretation of results, see `outputs/INTERPRETATION_GUIDE.md`.
