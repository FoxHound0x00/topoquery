"""
Parse SQL queries and extract features
"""
import json
import re
import sqlparse
import numpy as np
from typing import List, Dict, Any, Tuple

class SQLFeatureExtractor:
    """Extract structural, semantic, and contextual features from SQL queries"""
    
    def parse_query(self, query_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Parse SQL query and extract features"""
        sql = query_dict['sql']
        parsed = sqlparse.parse(sql)[0]
        
        features = {
            'sql': sql,
            'description': query_dict['description'],
            'user': query_dict['user'],
            'timestamp': query_dict['timestamp'],
            
            # Structural features
            'tables': self._extract_tables(parsed),
            'columns': self._extract_columns(parsed),
            'has_join': self._has_join(parsed),
            'has_where': self._has_where(parsed),
            'has_group_by': self._has_group_by(parsed),
            'has_order_by': self._has_order_by(parsed),
            'has_limit': self._has_limit(parsed),
            'num_conditions': self._count_conditions(parsed),
            'aggregations': self._extract_aggregations(parsed),
            
            # Semantic features
            'query_type': self._get_query_type(parsed),
            'column_types': self._infer_column_types(parsed),
        }
        
        return features
    
    def _extract_tables(self, parsed) -> List[str]:
        """Extract table names"""
        tables = []
        sql_str = str(parsed).upper()
        
        # Simple pattern matching for FROM and JOIN clauses
        from_pattern = r'FROM\s+(\w+)'
        join_pattern = r'JOIN\s+(\w+)'
        
        tables.extend(re.findall(from_pattern, sql_str))
        tables.extend(re.findall(join_pattern, sql_str))
        
        return list(set([t.lower() for t in tables]))
    
    def _extract_columns(self, parsed) -> List[str]:
        """Extract column names"""
        columns = []
        sql_str = str(parsed)
        
        # Extract from SELECT clause
        select_match = re.search(r'SELECT\s+(.*?)\s+FROM', sql_str, re.IGNORECASE)
        if select_match:
            select_clause = select_match.group(1)
            if '*' not in select_clause:
                # Parse column names
                col_parts = select_clause.split(',')
                for col in col_parts:
                    col = col.strip()
                    # Remove functions
                    col = re.sub(r'\w+\((.*?)\)', r'\1', col)
                    # Remove aliases
                    col = re.sub(r'\s+as\s+\w+', '', col, flags=re.IGNORECASE)
                    # Remove table prefixes
                    col = col.split('.')[-1].strip()
                    if col and col != '*':
                        columns.append(col)
        
        # Extract from WHERE, GROUP BY, ORDER BY
        for keyword in ['WHERE', 'GROUP BY', 'ORDER BY']:
            pattern = f'{keyword}\\s+(.*?)(?:GROUP BY|ORDER BY|LIMIT|$)'
            match = re.search(pattern, sql_str, re.IGNORECASE)
            if match:
                clause = match.group(1)
                col_names = re.findall(r'\b([a-z_][a-z0-9_]*)\b', clause, re.IGNORECASE)
                columns.extend([c for c in col_names if c.upper() not in 
                               ['AND', 'OR', 'NOT', 'IN', 'IS', 'NULL', 'BETWEEN', 'DESC', 'ASC']])
        
        return list(set(columns))
    
    def _has_join(self, parsed) -> bool:
        return 'JOIN' in str(parsed).upper()
    
    def _has_where(self, parsed) -> bool:
        return 'WHERE' in str(parsed).upper()
    
    def _has_group_by(self, parsed) -> bool:
        return 'GROUP BY' in str(parsed).upper()
    
    def _has_order_by(self, parsed) -> bool:
        return 'ORDER BY' in str(parsed).upper()
    
    def _has_limit(self, parsed) -> bool:
        return 'LIMIT' in str(parsed).upper()
    
    def _count_conditions(self, parsed) -> int:
        """Count WHERE conditions"""
        sql_str = str(parsed).upper()
        if 'WHERE' not in sql_str:
            return 0
        where_clause = sql_str.split('WHERE')[1].split('GROUP BY')[0] if 'GROUP BY' in sql_str else sql_str.split('WHERE')[1]
        return where_clause.count('AND') + where_clause.count('OR') + 1
    
    def _extract_aggregations(self, parsed) -> List[str]:
        """Extract aggregation functions"""
        sql_str = str(parsed).upper()
        agg_functions = []
        for func in ['COUNT', 'AVG', 'SUM', 'MAX', 'MIN']:
            if func in sql_str:
                agg_functions.append(func)
        return agg_functions
    
    def _get_query_type(self, parsed) -> str:
        """Determine query type"""
        sql_str = str(parsed).upper()
        if 'JOIN' in sql_str:
            return 'JOIN'
        elif 'GROUP BY' in sql_str:
            return 'AGGREGATION'
        elif 'WHERE' in sql_str:
            return 'FILTER'
        else:
            return 'SELECT'
    
    def _infer_column_types(self, parsed) -> Dict[str, str]:
        """Infer semantic types of columns"""
        types = {}
        columns = self._extract_columns(parsed)
        
        for col in columns:
            col_lower = col.lower()
            if 'date' in col_lower or 'time' in col_lower:
                types[col] = 'temporal'
            elif any(measure in col_lower for measure in ['length', 'depth', 'mass', 'weight', 'area']):
                types[col] = 'measurement'
            elif any(cat in col_lower for cat in ['species', 'island', 'sex', 'name', 'researcher']):
                types[col] = 'categorical'
            else:
                types[col] = 'unknown'
        
        return types


def create_feature_vectors(parsed_queries: List[Dict[str, Any]]) -> Tuple[np.ndarray, List[str], Dict]:
    """Convert parsed queries into numerical feature vectors"""
    
    # Build vocabularies
    all_tables = set()
    all_columns = set()
    all_users = set()
    all_agg_functions = set()
    
    for q in parsed_queries:
        all_tables.update(q['tables'])
        all_columns.update(q['columns'])
        all_users.add(q['user'])
        all_agg_functions.update(q['aggregations'])
    
    table_list = sorted(list(all_tables))
    column_list = sorted(list(all_columns))
    user_list = sorted(list(all_users))
    agg_list = sorted(list(all_agg_functions))
    
    vocabularies = {
        'tables': table_list,
        'columns': column_list,
        'users': user_list,
        'aggregations': agg_list
    }
    
    feature_vectors = []
    
    for q in parsed_queries:
        vector = []
        
        # Table one-hot encoding
        for table in table_list:
            vector.append(1 if table in q['tables'] else 0)
        
        # Column one-hot encoding
        for col in column_list:
            vector.append(1 if col in q['columns'] else 0)
        
        # Structural features
        vector.append(1 if q['has_join'] else 0)
        vector.append(1 if q['has_where'] else 0)
        vector.append(1 if q['has_group_by'] else 0)
        vector.append(1 if q['has_order_by'] else 0)
        vector.append(1 if q['has_limit'] else 0)
        vector.append(q['num_conditions'])
        
        # Aggregation one-hot encoding
        for agg in agg_list:
            vector.append(1 if agg in q['aggregations'] else 0)
        
        # Query type one-hot
        query_types = ['SELECT', 'FILTER', 'AGGREGATION', 'JOIN']
        for qtype in query_types:
            vector.append(1 if q['query_type'] == qtype else 0)
        
        # User one-hot encoding
        for user in user_list:
            vector.append(1 if q['user'] == user else 0)
        
        # Semantic features - column type counts
        type_counts = {'temporal': 0, 'measurement': 0, 'categorical': 0, 'unknown': 0}
        for col_type in q['column_types'].values():
            type_counts[col_type] += 1
        for t in ['temporal', 'measurement', 'categorical', 'unknown']:
            vector.append(type_counts[t])
        
        feature_vectors.append(vector)
    
    # Build feature names
    feature_names = (
        [f'table_{t}' for t in table_list] +
        [f'column_{c}' for c in column_list] +
        ['has_join', 'has_where', 'has_group_by', 'has_order_by', 'has_limit', 'num_conditions'] +
        [f'agg_{a}' for a in agg_list] +
        [f'type_{qt}' for qt in query_types] +
        [f'user_{u}' for u in user_list] +
        ['semantic_temporal', 'semantic_measurement', 'semantic_categorical', 'semantic_unknown']
    )
    
    feature_matrix = np.array(feature_vectors, dtype=float)
    
    return feature_matrix, feature_names, vocabularies


def parse_and_save():
    """Parse queries and save features"""
    print("Parsing SQL queries...")
    
    # Load queries
    with open('queries/sample_queries.json', 'r') as f:
        queries = json.load(f)
    
    # Parse queries
    extractor = SQLFeatureExtractor()
    parsed_queries = [extractor.parse_query(q) for q in queries]
    
    # Create feature vectors
    feature_matrix, feature_names, vocabularies = create_feature_vectors(parsed_queries)
    
    # Save results
    output = {
        'parsed_queries': parsed_queries,
        'feature_matrix': feature_matrix.tolist(),
        'feature_names': feature_names,
        'vocabularies': vocabularies
    }
    
    with open('queries/parsed_features.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"✓ Parsed {len(parsed_queries)} queries")
    print(f"✓ Feature matrix shape: {feature_matrix.shape}")
    print(f"✓ Vocabularies:")
    print(f"  - Tables: {vocabularies['tables']}")
    print(f"  - Users: {vocabularies['users']}")
    print(f"  - Aggregations: {vocabularies['aggregations']}")
    print(f"✓ Saved to: queries/parsed_features.json")
    print()

if __name__ == '__main__':
    parse_and_save()

