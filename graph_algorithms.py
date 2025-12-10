# graph_algorithms.py
"""
Algorithms for operating on the CoPurchaseGraph structure.

Includes:
- BFS (Breadth-First Search)
- DFS (Depth-First Search)
- Frequent item-pair mining
- Ranking & sorting algorithms (top product bundles)
- Recommendation algorithm
- Graph visualisation helpers (text-based)

All algorithms operate on the adjacency-list structure exposed by:
    CoPurchaseGraph.as_adjacency_dict()
"""

from collections import deque
from typing import Dict, List, Tuple


# Type alias for readability
GraphAdj = Dict[str, Dict[str, int]]


# ============================================================
# 1. GRAPH TRAVERSAL ALGORITHMS
# ============================================================

# -----------------------------
# Breadth-First Search (BFS)
# -----------------------------
def bfs(graph: GraphAdj, start_item: str) -> List[str]:
    """
    Perform a BFS traversal starting from start_item.

    Returns the order in which nodes (items) are visited.

    BFS is useful for:
    - Finding connected components
    - Exploring items related to a given item
    - Performing level-order exploration
    """
    if start_item not in graph:
        return []

    visited = set()
    queue = deque([start_item])
    order = []

    while queue:
        current = queue.popleft()

        if current not in visited:
            visited.add(current)
            order.append(current)

            # Add neighbours to queue
            for neighbour in graph[current]:
                if neighbour not in visited:
                    queue.append(neighbour)

    return order


# -----------------------------
# Depth-First Search (DFS)
# -----------------------------
def dfs(graph: GraphAdj, start_item: str) -> List[str]:
    """
    Perform a Depth-First Search traversal using recursion.

    DFS is useful for:
    - Exploring associations deeply
    - Path-like exploration of graph structure
    """
    visited = set()
    order = []

    def _dfs(node: str):
        if node in visited:
            return
        visited.add(node)
        order.append(node)
        for neighbour in graph.get(node, {}):
            _dfs(neighbour)

    if start_item in graph:
        _dfs(start_item)

    return order


# ============================================================
# 2. FREQUENT PAIR / ITEMSET MINING
# ============================================================

def frequent_pairs(graph: GraphAdj, min_support: int = 2) -> List[Tuple[Tuple[str, str], int]]:
    """
    Return all item pairs (A, B) whose co-purchase frequency >= min_support.

    Equivalent to extremely simplified Apriori for pair itemsets.
    """
    results = []

    for item in graph:
        for neighbour, weight in graph[item].items():
            if item < neighbour:  # avoid duplicates
                if weight >= min_support:
                    results.append(((item, neighbour), weight))

    # Can add optional sorting here
    results.sort(key=lambda x: x[1], reverse=True)
    return results


# ============================================================
# 3. SORTING / RANKING ALGORITHMS
# ============================================================

def top_product_bundles(graph: GraphAdj, k: int = 5) -> List[Tuple[Tuple[str, str], int]]:
    """
    Return the top-k most frequent item pairs across all transactions.

    Uses sorting (O(E log E)) where E = number of edges.
    """
    all_pairs = []

    for item in graph:
        for neighbour, weight in graph[item].items():
            if item < neighbour:
                all_pairs.append(((item, neighbour), weight))

    # Sort descending by weight
    all_pairs.sort(key=lambda x: x[1], reverse=True)
    return all_pairs[:k]


# ============================================================
# 4. RECOMMENDER ALGORITHM
# ============================================================

def recommend_items(graph: GraphAdj, item: str, top_n: int = 5) -> List[Tuple[str, int]]:
    """
    Given an item, return the top_n items most frequently co-purchased with it.

    Works by sorting the neighbours of the node.
    """
    if item not in graph:
        return []

    neighbours = graph[item]
    ranked = sorted(neighbours.items(), key=lambda x: x[1], reverse=True)
    return ranked[:top_n]


# ============================================================
# 5. GRAPH VISUALISATION HELPERS (TEXT-BASED)
# ============================================================

def strongest_associations(graph: GraphAdj, top_n: int = 10) -> List[Tuple[str, str, int]]:
    """
    Return a text-friendly list of strongest associations.

    Equivalent to top edges in descending order of weight.
    """
    edges = []

    for item in graph:
        for neighbour, weight in graph[item].items():
            if item < neighbour:
                edges.append((item, neighbour, weight))

    edges.sort(key=lambda x: x[2], reverse=True)
    return edges[:top_n]


def print_graph(graph: GraphAdj) -> None:
    """
    Print adjacency list for debugging.
    """
    for item, neighbours in graph.items():
        print(f"{item}: {neighbours}")
