#!/bin/bash
# Clean script for explainable-recs project
# Removes all generated files and outputs

echo "Cleaning explainable-recs project..."

# Remove generated data
echo "  - Removing database..."
rm -f data/penguins.db

# Remove generated queries
echo "  - Removing queries..."
rm -f queries/sample_queries.json
rm -f queries/parsed_features.json

# Remove outputs
echo "  - Removing visualizations..."
rm -f outputs/visualizations/*.png

echo "  - Removing recommendations..."
rm -f outputs/recommendations/recommendations.json
rm -f outputs/recommendations/recommendations_summary.txt

echo "  - Removing topological features..."
rm -f outputs/topological_features.json
rm -f outputs/INTERPRETATION_GUIDE.md

# Remove Python cache
echo "  - Removing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.pyo" -delete 2>/dev/null

# Remove log files
echo "  - Removing log files..."
rm -f *.log

# Keep directory structure but remove contents
echo "  - Ensuring directory structure exists..."
mkdir -p data
mkdir -p queries
mkdir -p outputs/visualizations
mkdir -p outputs/recommendations

echo "✓ Project cleaned!"
echo ""
echo "To regenerate everything, run: python run_pipeline.py"

