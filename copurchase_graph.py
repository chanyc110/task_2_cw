
"""


An undirected, weighted graph where:
- Each node is an item (string, e.g. "BREAD", "MILK").
- An edge between two items represents that they were bought together
  in at least one transaction.
- The edge weight is the number of times they were co-purchased.

This structure will later allow:
- BFS/DFS traversals,
- queries like "items bought with X",
- and mining of frequent item pairs.
"""

from typing import Dict, List, Tuple, Optional


class CoPurchaseGraph:
    def __init__(self) -> None:
        # Adjacency list representation:
        # { item: { other_item: weight, ... }, ... }
        self._adjacency: Dict[str, Dict[str, int]] = {}

    # -------------------------------------------------
    # Basic node & edge operations
    # -------------------------------------------------
    def add_item(self, item: str) -> None:
        """
        Ensure an item exists as a node in the graph.
        Does nothing if the item is already present.
        """
        if item not in self._adjacency:
            self._adjacency[item] = {}

    def add_co_purchase(self, item1: str, item2: str) -> None:
        """
        Add or update an undirected edge between item1 and item2.
        Increments the edge weight by 1 to record another co-purchase.

        Self-edges (item1 == item2) are ignored.
        """
        if item1 == item2:
            return

        # Make sure both items exist as nodes
        if item1 not in self._adjacency:
            self._adjacency[item1] = {}
        if item2 not in self._adjacency:
            self._adjacency[item2] = {}

        # Increase weight in both directions (undirected graph)
        self._adjacency[item1][item2] = self._adjacency[item1].get(item2, 0) + 1
        self._adjacency[item2][item1] = self._adjacency[item2].get(item1, 0) + 1

    # -------------------------------------------------
    # Query methods
    # -------------------------------------------------
    def items(self) -> List[str]:
        """
        Return a sorted list of all items (nodes) in the graph.
        """
        return sorted(self._adjacency.keys())

    def neighbours(self, item: str) -> Dict[str, int]:
        """
        Return a dictionary of neighbours and weights for a given item.

        Example:
            graph.neighbours("BREAD") -> {"MILK": 12, "BUTTER": 5}
        """
        return self._adjacency.get(item, {})

    def edge_weight(self, item1: str, item2: str) -> int:
        """
        Return the co-purchase count (edge weight) between two items.
        Returns 0 if there is no edge.
        """
        if item1 not in self._adjacency:
            return 0
        return self._adjacency[item1].get(item2, 0)

    def has_item(self, item: str) -> bool:
        """
        Check if an item is present as a node in the graph.
        """
        return item in self._adjacency

    def has_edge(self, item1: str, item2: str) -> bool:
        """
        Check if there is an edge between item1 and item2.
        """
        if item1 not in self._adjacency:
            return False
        return item2 in self._adjacency[item1]

    # -------------------------------------------------
    # Graph statistics
    # -------------------------------------------------
    def num_items(self) -> int:
        """Return the number of distinct items (nodes) in the graph."""
        return len(self._adjacency)

    def num_edges(self) -> int:
        """
        Return the number of undirected edges in the graph.
        Each pair is stored twice in the adjacency list (A->B, B->A),
        so we divide by 2.
        """
        total = 0
        for item in self._adjacency:
            total += len(self._adjacency[item])
        return total // 2

    def top_neighbours(self, item: str, k: int = 5) -> List[Tuple[str, int]]:
        """
        Convenience method: return the top-k neighbours of an item,
        sorted by descending co-purchase count.

        This will be used later for recommendation-style queries.
        """
        neighbours = self.neighbours(item)
        # Sort by weight descending
        sorted_neighbours = sorted(
            neighbours.items(),
            key=lambda pair: pair[1],
            reverse=True,
        )
        return sorted_neighbours[:k]

    # -------------------------------------------------
    # Utility / debug
    # -------------------------------------------------
    def as_adjacency_dict(self) -> Dict[str, Dict[str, int]]:
        """
        Expose the raw adjacency dictionary.
        Useful for algorithms like BFS that operate directly on the graph.
        """
        return self._adjacency

    def __repr__(self) -> str:
        return f"CoPurchaseGraph(num_items={self.num_items()}, num_edges={self.num_edges()})"

