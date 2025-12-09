"""
Run the complete explainable query recommendation pipeline
"""
import sys
import subprocess

def run_step(script_name, description):
    """Run a pipeline step"""
    print()
    print("="*80)
    print(f"RUNNING: {description}")
    print("="*80)
    print()
    
    result = subprocess.run([sys.executable, script_name], 
                          capture_output=False, text=True)
    
    if result.returncode != 0:
        print(f"\n❌ Error running {script_name}")
        sys.exit(1)
    
    return result.returncode == 0

def main():
    """Run complete pipeline"""
    print()
    print("="*80)
    print(" EXPLAINABLE QUERY RECOMMENDATIONS PIPELINE")
    print(" Using Topological Data Analysis on Palmer Penguins")
    print("="*80)
    
    steps = [
        ("create_database.py", "Step 1: Create Palmer Penguins Database"),
        ("generate_queries.py", "Step 2: Generate Sample SQL Queries"),
        ("parse_queries.py", "Step 3: Parse Queries and Extract Features"),
        ("topological_analysis.py", "Step 4: Compute Topological Features"),
        ("recommend_queries.py", "Step 5: Generate Query Recommendations"),
        ("visualize_results.py", "Step 6: Create Visualizations"),
    ]
    
    for script, description in steps:
        if not run_step(script, description):
            print(f"\n❌ Pipeline failed at: {description}")
            return
    
    print()
    print("="*80)
    print(" ✓ PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*80)
    print()
    print("Check the following directories for outputs:")
    print("  - data/              : SQLite database")
    print("  - queries/           : Generated queries and features")
    print("  - outputs/visualizations/  : Plots and heatmaps")
    print("  - outputs/recommendations/ : Recommendation results")
    print()

if __name__ == '__main__':
    main()

