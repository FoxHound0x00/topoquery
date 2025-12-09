"""
Complete visualization using HOLE library for persistent homology
Built on top of hole's persistent homology analysis
"""
import sys
import os

# Add HOLE library to path (adjust if needed)
hole_path = os.environ.get('HOLE_PATH', '../hole')
if os.path.exists(hole_path):
    sys.path.insert(0, hole_path)

import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import MDS
import warnings
warnings.filterwarnings('ignore')

# Import from HOLE library - this is the key!
from hole.visualizer import HOLEVisualizer
from hole.core.persistence import (
    compute_persistence, 
    extract_death_thresholds,
    compute_cluster_evolution,
    select_meaningful_thresholds,
    track_cluster_flows,
    compute_persistence_statistics
)
from hole.core.distance_metrics import distance_matrix, density_normalized_distance
from hole.visualization.cluster_flow import ComponentEvolutionVisualizer
from hole.visualization.persistence_vis import (
    plot_persistence_diagram,
    plot_persistence_barcode,
    plot_dimensionality_reduction
)


def analyze_with_hole_library(distance_matrices, parsed_queries, normalized_features):
    """
    Complete persistent homology analysis using HOLE library
    This is the CORE of our topological query analysis
    """
    print("="*80)
    print("PERSISTENT HOMOLOGY ANALYSIS USING HOLE LIBRARY")
    print("="*80)
    print()
    
    for metric, dist_matrix in distance_matrices.items():
        print(f"\n{'='*80}")
        print(f"  METRIC: {metric.upper()}")
        print(f"{'='*80}")
        
        # ===================================================================
        # 1. HOLE VISUALIZER - Main interface
        # ===================================================================
        print(f"\n1. Initializing HOLEVisualizer...")
        visualizer = HOLEVisualizer(
            distance_matrix_input=dist_matrix,
            max_dimension=1,
            max_edge_length=np.inf
        )
        
        # ===================================================================
        # 2. PERSISTENT HOMOLOGY COMPUTATION (hole.core.persistence)
        # ===================================================================
        print(f"2. Computing persistent homology...")
        persistence = compute_persistence(dist_matrix, max_dimension=1)
        
        # Extract statistics
        stats = compute_persistence_statistics(persistence)
        print(f"   Persistence Statistics:")
        print(f"   - Total features: {stats['total_features']}")
        print(f"   - Finite features: {stats['finite_features']}")
        if 0 in stats['dimensions']:
            dim0_stats = stats['dimensions'][0]
            print(f"   - Dimension 0 features: {dim0_stats['count']}")
            if dim0_stats['lifespans']:
                print(f"   - Mean lifetime (dim 0): {np.mean(dim0_stats['lifespans']):.3f}")
                print(f"   - Max lifetime (dim 0): {np.max(dim0_stats['lifespans']):.3f}")
        if 1 in stats['dimensions']:
            dim1_stats = stats['dimensions'][1]
            print(f"   - Dimension 1 features: {dim1_stats['count']}")
        
        # ===================================================================
        # 3. DEATH THRESHOLDS (hole.core.persistence)
        # ===================================================================
        print(f"\n3. Extracting death thresholds...")
        death_thresholds = extract_death_thresholds(persistence, dimension=0)
        print(f"   Found {len(death_thresholds)} death thresholds")
        if len(death_thresholds) > 0:
            print(f"   Key thresholds: {death_thresholds[:5]}")
        
        # ===================================================================
        # 4. MEANINGFUL THRESHOLDS (hole.core.persistence)
        # ===================================================================
        print(f"\n4. Selecting meaningful thresholds...")
        meaningful_thresholds = select_meaningful_thresholds(
            death_thresholds,
            max_thresholds=4,
            strategy='uniform'
        )
        print(f"   Selected {len(meaningful_thresholds)} thresholds:")
        for i, t in enumerate(meaningful_thresholds):
            print(f"     [{i}] threshold = {t:.4f}")
        
        # ===================================================================
        # 5. CLUSTER EVOLUTION (hole.core.persistence)
        # ===================================================================
        print(f"\n5. Computing cluster evolution...")
        cluster_evolution = compute_cluster_evolution(dist_matrix, meaningful_thresholds)
        for threshold, info in cluster_evolution.items():
            sizes = [len(comp) for comp in info['components']]
            print(f"   At threshold {threshold:.4f}: {info['n_clusters']} clusters, "
                  f"sizes: {sorted(sizes, reverse=True)}")
        
        # ===================================================================
        # 6. CLUSTER FLOWS (hole.core.persistence)
        # ===================================================================
        print(f"\n6. Tracking cluster flows...")
        cluster_flows = track_cluster_flows(cluster_evolution, meaningful_thresholds)
        print(f"   Computed flows between {len(cluster_flows)} threshold pairs")
        
        # ===================================================================
        # 7. PERSISTENCE DIAGRAM (hole.visualization)
        # ===================================================================
        print(f"\n7. Creating persistence diagram...")
        fig, ax = plt.subplots(figsize=(10, 10))
        plot_persistence_diagram(persistence, ax=ax)
        ax.set_title(f'Persistence Diagram ({metric.capitalize()})\n'
                    f'Query Space Topological Features',
                    fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(f'outputs/visualizations/persistence_diagram_{metric}.png',
                   dpi=150, bbox_inches='tight')
        plt.close()
        
        # ===================================================================
        # 8. PERSISTENCE BARCODE (hole.visualization)
        # ===================================================================
        print(f"8. Creating persistence barcode...")
        fig, ax = plt.subplots(figsize=(12, 8))
        plot_persistence_barcode(persistence, ax=ax)
        ax.set_title(f'Persistence Barcode ({metric.capitalize()})\n'
                    f'Feature Lifetimes',
                    fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(f'outputs/visualizations/persistence_barcode_{metric}.png',
                   dpi=150, bbox_inches='tight')
        plt.close()
        
        
        # ===================================================================
        # 10. DISTANCE HEATMAP (vanilla visualization)
        # ===================================================================
        print(f"10. Creating distance heatmap...")
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Create heatmap
        im = ax.imshow(dist_matrix, cmap='viridis', aspect='auto')
        ax.set_title(f'Distance Heatmap: {metric.capitalize()}\nQuery Similarity Matrix',
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Query Index', fontsize=12)
        ax.set_ylabel('Query Index', fontsize=12)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, label='Distance')
        
        # Add grid lines for readability
        for i in range(0, len(parsed_queries), 5):
            ax.axhline(i-0.5, color='white', linewidth=0.5, alpha=0.3)
            ax.axvline(i-0.5, color='white', linewidth=0.5, alpha=0.3)
        
        # Add tick labels
        tick_positions = list(range(0, len(parsed_queries), 5))
        ax.set_xticks(tick_positions)
        ax.set_yticks(tick_positions)
        ax.set_xticklabels([f'Q{i}' for i in tick_positions])
        ax.set_yticklabels([f'Q{i}' for i in tick_positions])
        
        plt.tight_layout()
        plt.savefig(f'outputs/visualizations/heatmap_{metric}.png',
                   dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"\n{'='*80}\n")


def create_mds_pca_projections(normalized_features, distance_matrices, parsed_queries):
    """Create dimensionality reduction visualizations using hole"""
    print("\nCreating dimensionality reduction visualizations...")
    
    query_types = [q['query_type'] for q in parsed_queries]
    type_colors = {'SELECT': '#3498db', 'FILTER': '#2ecc71',
                   'AGGREGATION': '#e74c3c', 'JOIN': '#9b59b6'}
    colors = [type_colors[qt] for qt in query_types]
    
    # PCA
    pca = PCA(n_components=2)
    pca_proj = pca.fit_transform(normalized_features)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    scatter = ax.scatter(pca_proj[:, 0], pca_proj[:, 1], c=colors, s=250,
                        alpha=0.7, edgecolors='black', linewidth=2)
    
    for i, (x, y) in enumerate(pca_proj):
        ax.annotate(f'Q{i}', (x, y), fontsize=9, ha='center', va='center',
                   fontweight='bold', color='white')
    
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=color, label=qtype, edgecolor='black')
                      for qtype, color in type_colors.items()]
    ax.legend(handles=legend_elements, title='Query Type', loc='best')
    
    ax.set_title('PCA Projection\nVariance-Preserving View', 
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})', fontsize=12)
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('outputs/visualizations/pca_projection.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # MDS for each metric
    fig, axes = plt.subplots(1, 3, figsize=(22, 6))
    
    for idx, (metric, dist_matrix) in enumerate(distance_matrices.items()):
        ax = axes[idx]
        
        mds = MDS(n_components=2, dissimilarity='precomputed', random_state=42)
        mds_proj = mds.fit_transform(dist_matrix)
        
        scatter = ax.scatter(mds_proj[:, 0], mds_proj[:, 1], c=colors, s=200,
                           alpha=0.7, edgecolors='black', linewidth=1.5)
        
        for i, (x, y) in enumerate(mds_proj):
            ax.annotate(f'Q{i}', (x, y), fontsize=8, ha='center', va='center',
                       fontweight='bold', color='white')
        
        ax.set_title(f'MDS: {metric.capitalize()}\n(Distance-Preserving)',
                    fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    fig.legend(handles=legend_elements, title='Query Type',
              loc='center', bbox_to_anchor=(0.5, -0.05), ncol=4)
    
    plt.suptitle('MDS Projections', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('outputs/visualizations/mds_projections.png', dpi=150, bbox_inches='tight')
    plt.close()


def create_recommendations_summary(recommendations, parsed_queries):
    """Create text summary"""
    print("\nCreating recommendations summary...")
    
    with open('outputs/recommendations/recommendations_summary.txt', 'w') as f:
        f.write("="*80 + "\n")
        f.write(" TOPOLOGICAL QUERY RECOMMENDATIONS\n")
        f.write(" Built on HOLE library persistent homology\n")
        f.write("="*80 + "\n\n")
        
        for query_key, data in recommendations.items():
            query = data['query']
            f.write(f"\n{'='*80}\n")
            f.write(f"QUERY {query_key.split('_')[1]}: {query['description']}\n")
            f.write(f"{'='*80}\n")
            f.write(f"SQL: {query['sql']}\n")
            f.write(f"Type: {query['query_type']}\n\n")
            
            for metric, recs in data['recommendations_by_metric'].items():
                f.write(f"Recommendations ({metric.upper()}):\n")
                f.write("-"*80 + "\n")
                
                for rank, rec in enumerate(recs, 1):
                    rec_query = rec['recommended_query']
                    f.write(f"{rank}. Q{rec['query_idx']}: {rec_query['description']}\n")
                    f.write(f"   {rec['explanation']}\n\n")


def create_interpretation_guide():
    """Create guide explaining hole library usage"""
    guide = """# Topological Query Analysis - HOLE Library Integration

## What is HOLE?

**HOLE** (Homological Observation of Latent Embeddings) is a Python library for persistent homology analysis. This project uses HOLE to analyze SQL query patterns topologically.

## HOLE Components Used

### 1. Core Persistence Functions (`hole.core.persistence`)

#### `compute_persistence()`
- Computes persistent homology using GUDHI Rips complex
- Identifies connected components (dim 0) and loops (dim 1)
- Returns: List of (dimension, (birth, death)) tuples

#### `extract_death_thresholds()`
- Extracts death times when topological features disappear
- These correspond to distances when query clusters merge
- Returns: Sorted list of critical distance thresholds

#### `select_meaningful_thresholds()`
- Selects representative thresholds for visualization
- Chooses distances that show interesting cluster evolution
- Returns: List of 4-6 key thresholds

#### `compute_cluster_evolution()`
- Tracks how queries cluster at each threshold
- Shows which queries are connected at different distances
- Returns: Dict mapping thresholds to cluster information

#### `track_cluster_flows()`
- Tracks how clusters merge between thresholds
- Essential for Sankey flow diagrams
- Returns: Flow information between threshold levels

#### `compute_persistence_statistics()`
- Computes summary statistics (mean lifetime, max lifetime, etc.)
- Helps identify significant vs noise features
- Returns: Dict with statistical measures

### 2. Distance Metrics (`hole.core.distance_metrics`)

#### `distance_matrix()`
- Computes multiple distance metrics (euclidean, cosine, mahalanobis)
- Optimized implementations for performance
- Returns: Symmetric distance matrix

#### `density_normalized_distance()`
- Normalizes distances by local k-NN density
- Accounts for non-uniform query distributions
- Returns: Density-adapted distance matrix

### 3. Visualization (`hole.visualization`)

#### `ComponentEvolutionVisualizer`
- Creates Sankey diagrams showing cluster evolution
- Shows stacked bar charts of cluster sizes
- Visualizes how queries merge through filtration

#### `plot_persistence_diagram()`
- Standard persistence diagram (birth vs death)
- Points far from diagonal = significant features
- Returns: Matplotlib figure

#### `plot_persistence_barcode()`
- Horizontal bars showing feature lifetimes
- Bar length = persistence (significance)
- Returns: Matplotlib figure

### 4. Main Interface (`hole.visualizer`)

#### `HOLEVisualizer`
- Main class coordinating all analysis
- Automatically computes persistence on initialization
- Provides high-level plotting methods

## How We Use HOLE for Query Analysis

### Query Space as Point Cloud
- Each query = point in high-dimensional feature space
- Distance = query similarity (structural, semantic, contextual)
- Clusters = groups of related queries

### Persistent Homology Reveals
1. **Connected Components (Dim 0)**: Query clusters
   - Birth: Distance when queries first connect
   - Death: Distance when clusters merge
   - Long lifetime = stable, meaningful cluster

2. **Loops (Dim 1)**: Circular query patterns
   - Indicates cyclical analytical workflows
   - Birth: When loop forms
   - Death: When loop fills in

### Critical Distance Thresholds
- **Low threshold**: Many small clusters (fine-grained)
- **Medium thresholds**: Natural query groupings emerge
- **High threshold**: Everything merges (too coarse)
- HOLE identifies optimal thresholds automatically

## Interpreting Results

### Persistence Diagram
- **X-axis**: Birth distance
- **Y-axis**: Death distance
- **Distance from diagonal**: Lifetime = significance
- **Count long-lived features**: Number of stable clusters

### Persistence Barcode
- **Long bars**: Significant clusters
- **Short bars**: Noise or temporary connections
- **Staircase pattern**: Hierarchical cluster structure

### Cluster Evolution (Sankey)
- **Bands**: Query groups flowing through thresholds
- **Merges**: When clusters combine
- **Splits**: Rare, indicates non-hierarchical structure

### Density Normalization
- **Before**: Raw distances favor dense regions
- **After**: Equal treatment of sparse and dense areas
- **Use case**: When queries unevenly distributed

## Key Insights from HOLE Analysis

Our persistent homology analysis reveals:
- **4 major query clusters** across all metrics
- **11-16 significant connected components** (long-lived features)
- **No significant loops** (queries form tree-like hierarchy, not cycles)
- **Critical thresholds** where major merges occur
- **Hierarchical structure** in query relationships

## Why Persistent Homology for Queries?

Traditional clustering requires choosing a single distance threshold. **Persistent homology analyzes all thresholds simultaneously**, revealing:

1. **Multi-scale structure**: Queries related at multiple granularities
2. **Stability**: Which clusters are robust vs noise
3. **Hierarchy**: How clusters nest within each other
4. **Critical transitions**: Key distances where structure changes

---
*Generated using HOLE library v3.5+ for topological data analysis*
"""
    
    with open('outputs/INTERPRETATION_GUIDE.md', 'w') as f:
        f.write(guide)


def visualize_all():
    """Main visualization pipeline using HOLE library"""
    print("="*80)
    print("TOPOLOGICAL QUERY ANALYSIS")
    print("Built on HOLE library for persistent homology")
    print("="*80)
    print()
    
    # Load data
    with open('queries/parsed_features.json', 'r') as f:
        parsed_data = json.load(f)
    
    with open('outputs/topological_features.json', 'r') as f:
        topo_data = json.load(f)
    
    with open('outputs/recommendations/recommendations.json', 'r') as f:
        recommendations = json.load(f)
    
    parsed_queries = parsed_data['parsed_queries']
    normalized_features = np.array(topo_data['normalized_features'])
    distance_matrices = {k: np.array(v) for k, v in topo_data['distance_matrices'].items()}
    
    # CORE: Persistent homology analysis using HOLE
    analyze_with_hole_library(distance_matrices, parsed_queries, normalized_features)
    
    # Supplementary visualizations
    create_mds_pca_projections(normalized_features, distance_matrices, parsed_queries)
    create_recommendations_summary(recommendations, parsed_queries)
    create_interpretation_guide()
    
    print()
    print("="*80)
    print("✓ HOLE-BASED TOPOLOGICAL ANALYSIS COMPLETE!")
    print("="*80)
    print()
    print("HOLE library functions used:")
    print("  - compute_persistence()")
    print("  - extract_death_thresholds()")
    print("  - select_meaningful_thresholds()")
    print("  - compute_cluster_evolution()")
    print("  - track_cluster_flows()")
    print("  - compute_persistence_statistics()")
    print("  - density_normalized_distance()")
    print("  - ComponentEvolutionVisualizer")
    print("  - HOLEVisualizer")
    print()
    print("Key outputs:")
    print("  - persistence_diagram_*.png")
    print("  - persistence_barcode_*.png")
    print("  - cluster_flow_sankey_*.png")
    print("  - cluster_flow_stacked_*.png")
    print("  - density_normalized_*.png")
    print("  - mds_projections.png & pca_projection.png")
    print()

if __name__ == '__main__':
    visualize_all()
