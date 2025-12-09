"""
Generate query recommendations with explanations
"""
import json
import numpy as np
from typing import List, Tuple, Dict, Any

class QueryRecommender:
    """Topological query recommendation engine"""
    
    def __init__(self, distance_matrices: Dict[str, np.ndarray], 
                 parsed_queries: List[Dict[str, Any]]):
        self.distance_matrices = distance_matrices
        self.queries = parsed_queries
        
    def recommend(self, query_idx: int, top_k: int = 3, 
                 metric: str = 'euclidean') -> List[Tuple[int, float, str]]:
        """
        Recommend top-k similar queries based on topological proximity
        
        Returns: List of (query_idx, distance, explanation)
        """
        if metric not in self.distance_matrices:
            metric = list(self.distance_matrices.keys())[0]
        
        dist_matrix = self.distance_matrices[metric]
        distances = dist_matrix[query_idx]
        
        # Get top-k nearest neighbors (excluding self)
        nearest_indices = np.argsort(distances)[1:top_k+1]
        
        recommendations = []
        query = self.queries[query_idx]
        
        for idx in nearest_indices:
            rec_query = self.queries[idx]
            distance = distances[idx]
            
            # Generate explanation
            explanation = self._generate_explanation(query, rec_query, distance, metric)
            recommendations.append((int(idx), float(distance), explanation))
        
        return recommendations
    
    def _generate_explanation(self, query: Dict, rec_query: Dict, 
                            distance: float, metric: str) -> str:
        """Generate natural language explanation for recommendation"""
        
        explanations = []
        
        # Compare query types
        if query['query_type'] == rec_query['query_type']:
            explanations.append(f"same query pattern ({query['query_type']})")
        
        # Compare structural features
        if query['has_join'] and rec_query['has_join']:
            explanations.append("both use joins")
        
        if query['has_group_by'] and rec_query['has_group_by']:
            explanations.append("both aggregate data")
        
        # Compare columns
        common_cols = set(query['columns']) & set(rec_query['columns'])
        if common_cols:
            cols_str = ', '.join(sorted(list(common_cols))[:3])
            explanations.append(f"share columns: {cols_str}")
        
        # Compare aggregations
        common_aggs = set(query['aggregations']) & set(rec_query['aggregations'])
        if common_aggs:
            explanations.append(f"use similar aggregations ({', '.join(common_aggs)})")
        
        # User pattern
        if query['user'] == rec_query['user']:
            explanations.append(f"same analyst ({query['user']})")
        
        if not explanations:
            explanations.append("topologically similar query structure")
        
        explanation = f"Topologically similar ({metric} distance: {distance:.3f}): " + "; ".join(explanations)
        
        return explanation


def generate_recommendations():
    """Generate recommendations for example queries"""
    print("Generating query recommendations...")
    
    # Load data
    with open('queries/parsed_features.json', 'r') as f:
        parsed_data = json.load(f)
    
    with open('outputs/topological_features.json', 'r') as f:
        topo_data = json.load(f)
    
    parsed_queries = parsed_data['parsed_queries']
    distance_matrices = {k: np.array(v) for k, v in topo_data['distance_matrices'].items()}
    
    # Initialize recommender
    recommender = QueryRecommender(distance_matrices, parsed_queries)
    
    # Generate recommendations for example queries
    example_queries = [0, 5, 12, 15, 20]  # Different query types
    
    all_recommendations = {}
    
    for idx in example_queries:
        query = parsed_queries[idx]
        query_recommendations = {
            'query': query,
            'recommendations_by_metric': {}
        }
        
        for metric in distance_matrices.keys():
            recommendations = recommender.recommend(idx, top_k=3, metric=metric)
            query_recommendations['recommendations_by_metric'][metric] = [
                {
                    'query_idx': rec_idx,
                    'distance': dist,
                    'explanation': expl,
                    'recommended_query': {
                        'sql': parsed_queries[rec_idx]['sql'],
                        'description': parsed_queries[rec_idx]['description'],
                        'user': parsed_queries[rec_idx]['user']
                    }
                }
                for rec_idx, dist, expl in recommendations
            ]
        
        all_recommendations[f'query_{idx}'] = query_recommendations
    
    # Save recommendations
    with open('outputs/recommendations/recommendations.json', 'w') as f:
        json.dump(all_recommendations, f, indent=2)
    
    print(f"✓ Generated recommendations for {len(example_queries)} example queries")
    print(f"✓ Using {len(distance_matrices)} distance metrics")
    print(f"✓ Saved to: outputs/recommendations/recommendations.json")
    print()

if __name__ == '__main__':
    generate_recommendations()

