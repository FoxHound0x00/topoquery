"""
Create generalized TopoQuery pipeline visualization
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

def create_generalized_pipeline():
    """Create a clean, generalized pipeline visualization"""
    
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Define pipeline steps with more general descriptions
    steps = [
        {
            'num': '1',
            'title': 'DATABASE',
            'desc': 'Query\nWorkload',
            'color': '#5DADE2',  # Blue
            'x': 1
        },
        {
            'num': '2',
            'title': 'QUERIES',
            'desc': 'SQL\nStatements',
            'color': '#C39BD3',  # Purple
            'x': 3.2
        },
        {
            'num': '3',
            'title': 'FEATURES',
            'desc': 'n-D Vector\nExtraction',
            'color': '#EC7063',  # Coral red
            'x': 5.4
        },
        {
            'num': '4',
            'title': 'DISTANCES',
            'desc': 'Metric\nComputation',
            'color': '#F5B041',  # Orange
            'x': 7.6
        },
        {
            'num': '5',
            'title': 'TOPOLOGY',
            'desc': 'Persistent\nHomology',
            'color': '#58D68D',  # Green
            'x': 9.8
        },
        {
            'num': '6',
            'title': 'RECOMMEND',
            'desc': 'Similar\nQueries',
            'color': '#45B7A8',  # Teal
            'x': 12
        },
        {
            'num': '7',
            'title': 'VISUALIZE',
            'desc': 'Diagrams &\nInsights',
            'color': '#52BE80',  # Light green
            'x': 14.2
        }
    ]
    
    # Draw boxes and arrows
    box_y = 2.5
    box_width = 1.8
    box_height = 2.0
    
    for i, step in enumerate(steps):
        # Draw box with rounded corners
        box = FancyBboxPatch(
            (step['x'], box_y), box_width, box_height,
            boxstyle="round,pad=0.1",
            linewidth=2.5,
            edgecolor='#2C3E50',
            facecolor=step['color'],
            alpha=0.85,
            zorder=2
        )
        ax.add_patch(box)
        
        # Add step number (small circle at top)
        circle = plt.Circle(
            (step['x'] + box_width/2, box_y + box_height - 0.3),
            0.25,
            color='white',
            edgecolor='#2C3E50',
            linewidth=2,
            zorder=3
        )
        ax.add_patch(circle)
        ax.text(
            step['x'] + box_width/2, box_y + box_height - 0.3,
            step['num'],
            ha='center', va='center',
            fontsize=14, fontweight='bold',
            color='#2C3E50',
            zorder=4
        )
        
        # Add title
        ax.text(
            step['x'] + box_width/2, box_y + box_height - 0.8,
            step['title'],
            ha='center', va='center',
            fontsize=13, fontweight='bold',
            color='white',
            zorder=3
        )
        
        # Add description
        ax.text(
            step['x'] + box_width/2, box_y + 0.6,
            step['desc'],
            ha='center', va='center',
            fontsize=10.5,
            color='white',
            linespacing=1.4,
            zorder=3
        )
        
        # Draw arrow to next step
        if i < len(steps) - 1:
            arrow_start_x = step['x'] + box_width + 0.05
            arrow_end_x = steps[i+1]['x'] - 0.05
            arrow_y = box_y + box_height / 2
            
            arrow = FancyArrowPatch(
                (arrow_start_x, arrow_y),
                (arrow_end_x, arrow_y),
                arrowstyle='->,head_width=0.4,head_length=0.4',
                linewidth=3,
                color='#34495E',
                zorder=1
            )
            ax.add_patch(arrow)
    
    # Add title
    ax.text(
        8, 5.3,
        'TopoQuery Pipeline',
        ha='center', va='center',
        fontsize=22, fontweight='bold',
        color='#2C3E50'
    )
    
    # Add subtitle
    ax.text(
        8, 4.85,
        'Explainable Query Recommendations via Persistent Homology',
        ha='center', va='center',
        fontsize=12,
        color='#7F8C8D',
        style='italic'
    )
    
    # Add bottom description with key concepts
    concepts = [
        ('Structural', 'Tables, Joins, Filters'),
        ('Semantic', 'Column Types, Operations'),
        ('Topological', 'Multi-scale Patterns'),
        ('Explainable', 'Visual Justifications')
    ]
    
    concept_y = 0.8
    start_x = 2.5
    spacing = 3.2
    
    for i, (concept, desc) in enumerate(concepts):
        x_pos = start_x + i * spacing
        # Small colored indicator
        indicator = plt.Circle(
            (x_pos - 0.15, concept_y),
            0.08,
            color=steps[i+1]['color'],
            zorder=2
        )
        ax.add_patch(indicator)
        
        ax.text(
            x_pos, concept_y + 0.15,
            concept,
            ha='left', va='center',
            fontsize=10, fontweight='bold',
            color='#2C3E50'
        )
        ax.text(
            x_pos, concept_y - 0.15,
            desc,
            ha='left', va='center',
            fontsize=8,
            color='#7F8C8D'
        )
    
    plt.tight_layout()
    return fig

def create_detailed_pipeline():
    """Create a more detailed version with technical specifics"""
    
    fig, ax = plt.subplots(figsize=(18, 8))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Main pipeline boxes
    steps = [
        {
            'title': 'Query Workload',
            'items': ['• Historical queries', '• User sessions', '• SQL logs'],
            'color': '#5DADE2',
            'x': 1, 'y': 4.5
        },
        {
            'title': 'Feature Extraction',
            'items': ['• Structural: AST', '• Semantic: Types', '• Context: Users'],
            'color': '#EC7063',
            'x': 4.5, 'y': 4.5
        },
        {
            'title': 'Vectorization',
            'items': ['• n-dimensional', '• One-hot encoding', '• Normalized'],
            'color': '#F5B041',
            'x': 8, 'y': 4.5
        },
        {
            'title': 'Distance Metrics',
            'items': ['• Euclidean', '• Cosine', '• Mahalanobis'],
            'color': '#F39C12',
            'x': 11.5, 'y': 4.5
        },
        {
            'title': 'Persistent Homology',
            'items': ['• Connected comp.', '• Loops & voids', '• Multi-scale'],
            'color': '#58D68D',
            'x': 4.5, 'y': 1.5
        },
        {
            'title': 'Recommendations',
            'items': ['• Top-k similar', '• Explanations', '• Confidence'],
            'color': '#45B7A8',
            'x': 8, 'y': 1.5
        },
        {
            'title': 'Visualizations',
            'items': ['• Diagrams', '• Barcodes', '• Projections'],
            'color': '#52BE80',
            'x': 11.5, 'y': 1.5
        }
    ]
    
    box_width = 2.8
    box_height = 2.2
    
    for step in steps:
        # Draw box
        box = FancyBboxPatch(
            (step['x'], step['y']), box_width, box_height,
            boxstyle="round,pad=0.15",
            linewidth=2,
            edgecolor='#2C3E50',
            facecolor=step['color'],
            alpha=0.75
        )
        ax.add_patch(box)
        
        # Title
        ax.text(
            step['x'] + box_width/2, step['y'] + box_height - 0.4,
            step['title'],
            ha='center', va='center',
            fontsize=12, fontweight='bold',
            color='white'
        )
        
        # Items
        for i, item in enumerate(step['items']):
            ax.text(
                step['x'] + 0.2, step['y'] + box_height - 1.0 - i*0.45,
                item,
                ha='left', va='center',
                fontsize=9,
                color='white'
            )
    
    # Add arrows
    arrows = [
        ((4.3, 5.6), (4.5, 4.5)),  # Workload to Features
        ((7.3, 5.6), (8, 4.5)),    # Features to Vectors
        ((10.8, 5.6), (11.5, 4.5)), # Vectors to Distances
        ((12.5, 4.5), (6.5, 3.7)),  # Distances to PH
        ((6.5, 3.7), (8, 1.5)),     # PH to Recommend
        ((10, 1.5), (11.5, 1.5))    # Recommend to Viz
    ]
    
    for start, end in arrows:
        arrow = FancyArrowPatch(
            start, end,
            arrowstyle='->,head_width=0.35,head_length=0.35',
            linewidth=2.5,
            color='#34495E',
            connectionstyle="arc3,rad=0.2"
        )
        ax.add_patch(arrow)
    
    # Title
    ax.text(
        9, 7.3,
        'TopoQuery: Detailed Architecture',
        ha='center', va='center',
        fontsize=20, fontweight='bold',
        color='#2C3E50'
    )
    
    ax.text(
        9, 6.85,
        'Topological Data Analysis for Query Understanding',
        ha='center', va='center',
        fontsize=11,
        color='#7F8C8D',
        style='italic'
    )
    
    plt.tight_layout()
    return fig

if __name__ == '__main__':
    # Create generalized version
    print("Creating generalized pipeline visualization...")
    fig1 = create_generalized_pipeline()
    fig1.savefig('outputs/visualizations/topoquery_pipeline_generalized.png',
                 dpi=200, bbox_inches='tight', facecolor='white')
    print("✓ Saved: topoquery_pipeline_generalized.png")
    
    # Create detailed version
    print("Creating detailed pipeline visualization...")
    fig2 = create_detailed_pipeline()
    fig2.savefig('outputs/visualizations/topoquery_pipeline_detailed.png',
                 dpi=200, bbox_inches='tight', facecolor='white')
    print("✓ Saved: topoquery_pipeline_detailed.png")
    
    plt.close('all')
    print("\n✓ All visualizations created!")

