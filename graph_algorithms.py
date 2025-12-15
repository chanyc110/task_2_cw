"""
Algorithms for operating on the CoPurchaseGraph structure.

Algorithms implemented from module content:
- BFS (Breadth-First Search) → identify related items in the graph
- DFS (Depth-First Search) → explore deep associations
- Frequent pair mining → counting-based algorithm (pairwise frequency)
- Sorting algorithm → rank bundles by frequency
"""

from collections import deque
from typing import Dict, List, Tuple

GraphAdj = Dict[str, Dict[str, int]]


# ============================================================
# 1. GRAPH TRAVERSAL ALGORITHMS FOR RELATED ITEM DISCOVERY
# ============================================================

def bfs_related_items(graph: GraphAdj, start_item: str) -> List[str]:
    """
    Uses BFS to identify all items related to `start_item` by co-purchases.

    BFS explores the graph level-by-level, meaning:
    - Items directly co-purchased with start_item appear early
    - Items indirectly related (via paths) appear later

    This satisfies: "Use BFS to identify related items"
    """
    if start_item not in graph:
        return []

    visited = set()
    queue = deque([start_item])
    related = []  # all reachable items except start_item

    while queue:
        current = queue.popleft()

        for neighbour in graph[current]:
            if neighbour not in visited:
                visited.add(neighbour)
                related.append(neighbour)
                queue.append(neighbour)

    return related


def dfs_related_items(graph: GraphAdj, start_item: str) -> List[str]:
    """
    Uses DFS to identify deep associations from start_item.

    DFS explores long chains of relationships, revealing:
    - Items connected through deeper co-purchase paths
    - Associations not found by looking only at direct neighbours

    This satisfies: "Use DFS to identify related items"
    """
    visited = set()
    related = []

    def _dfs(node: str):
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                related.append(neighbour)
                _dfs(neighbour)

    if start_item in graph:
        _dfs(start_item)

    return related


# ============================================================
# 2. FREQUENT PAIR MINING ALGORITHM
# ============================================================

def frequent_pairs(graph: GraphAdj, min_support: int = 2) -> List[Tuple[Tuple[str, str], int]]:
    """
    Frequent item-pair mining using a COUNTING algorithm.

    ALGORITHM:
    ----------
    For each edge (A, B) in the graph:
        - The edge weight represents how many times A and B appear in the same transaction
        - We filter pairs whose weight >= min_support

    This is equivalent to a simplified Apriori algorithm (size-2 itemsets).
    """

    results = []

    for item in graph:
        for neighbour, weight in graph[item].items():
            if item < neighbour:  # avoid duplicates
                if weight >= min_support:
                    results.append(((item, neighbour), weight))

    return results


# ============================================================
# 3. SORTING / RANKING ALGORITHM FOR TOP BUNDLES
# ============================================================

def quick_sort_items(pairs: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    if len(pairs) <= 1:
        return pairs

    pivot = pairs[len(pairs) // 2][1]

    left = [p for p in pairs if p[1] > pivot]
    middle = [p for p in pairs if p[1] == pivot]
    right = [p for p in pairs if p[1] < pivot]

    return quick_sort_items(left) + middle + quick_sort_items(right)



def top_product_bundles(graph: GraphAdj, k: int = 5) -> List[Tuple[Tuple[str, str], int]]:
    """
    Identifies the top-K strongest product bundles.

    ALGORITHM (Quick Sort Based Ranking):
    -------------------------------------
    Step 1: Extract all item pairs and their co-purchase frequency
    Step 2: Sort pairs using Quick Sort (descending by frequency)
    Step 3: Return the top K results
    """

    all_pairs = []

    for item in graph:
        for neighbour, weight in graph[item].items():
            if item < neighbour:  # avoid duplicate pairs
                all_pairs.append(((item, neighbour), weight))

    # Apply Quick Sort instead of Python's built-in sort
    sorted_pairs = quick_sort_items(all_pairs)

    return sorted_pairs[:k]



# ============================================================
# 4. RECOMMENDATION ALGORITHM
# ============================================================

def recommend_items(graph: GraphAdj, item: str, top_n: int = 5) -> List[Tuple[str, int]]:
    """
    Recommendation query:
    - Return top-N items most frequently bought with `item`.

    ALGORITHM:
    ----------
    Step 1: Look up graph[item]
    Step 2: Sort all neighbours by descending weight
    Step 3: Return first N

    Sorting → O(d log d), where d = number of neighbours.
    """
    if item not in graph:
        return []

    neighbour_pairs = list(graph[item].items())
    sorted_pairs = quick_sort_items(neighbour_pairs)
    
    return sorted_pairs[:top_n]


# ============================================================
# 5. STRONGEST ASSOCIATION VISUALISATION HELPER
# ============================================================

def strongest_associations(graph: GraphAdj, top_n: int = 10) -> List[Tuple[str, str, int]]:
    """
    Returns the strongest edges in the graph:
    (itemA, itemB, frequency)

    Used for simple graph-based visualisation.
    """
    edges = []

    for item in graph:
        for neighbour, weight in graph[item].items():
            if item < neighbour:
                edges.append((item, neighbour, weight))

    edges.sort(key=lambda x: x[2], reverse=True)
    return edges[:top_n]

