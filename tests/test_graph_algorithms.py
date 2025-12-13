import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph_algorithms import (
    bfs_related_items,
    dfs_related_items,
    frequent_pairs,
    top_product_bundles,
    recommend_items,
    strongest_associations,
)


# ============================================================
# FIXTURE: SMALL DETERMINISTIC GRAPH
# ============================================================
@pytest.fixture
def sample_graph():
    """
    A small, deterministic co-purchase graph for testing.

    Graph structure:
        bread -- milk (3)
        bread -- butter (2)
        milk -- eggs (1)
        butter -- jam (4)
    """
    return {
        "bread": {"milk": 3, "butter": 2},
        "milk": {"bread": 3, "eggs": 1},
        "butter": {"bread": 2, "jam": 4},
        "eggs": {"milk": 1},
        "jam": {"butter": 4},
    }


# ============================================================
# 1. BFS TESTS
# ============================================================

def test_bfs_related_items_basic(sample_graph):
    result = bfs_related_items(sample_graph, "bread")
    assert "milk" in result
    assert "butter" in result


def test_bfs_related_items_reaches_indirect_nodes(sample_graph):
    result = bfs_related_items(sample_graph, "bread")
    # eggs is indirectly connected via milk
    assert "eggs" in result


def test_bfs_nonexistent_start_item(sample_graph):
    result = bfs_related_items(sample_graph, "nonexistent")
    assert result == []


# ============================================================
# 2. DFS TESTS
# ============================================================

def test_dfs_related_items_basic(sample_graph):
    result = dfs_related_items(sample_graph, "bread")
    assert "milk" in result
    assert "butter" in result


def test_dfs_deep_association(sample_graph):
    result = dfs_related_items(sample_graph, "bread")
    # jam is deeper via butter
    assert "jam" in result


def test_dfs_nonexistent_start_item(sample_graph):
    result = dfs_related_items(sample_graph, "nonexistent")
    assert result == []


# ============================================================
# 3. FREQUENT PAIR MINING TESTS
# ============================================================

def test_frequent_pairs_min_support_2(sample_graph):
    result = frequent_pairs(sample_graph, min_support=2)
    pairs = [pair for pair, _ in result]

    assert ("bread", "milk") in pairs
    assert ("bread", "butter") in pairs
    assert ("butter", "jam") in pairs


def test_frequent_pairs_high_support(sample_graph):
    result = frequent_pairs(sample_graph, min_support=4)
    pairs = [pair for pair, _ in result]

    assert ("butter", "jam") in pairs
    assert ("bread", "milk") not in pairs


def test_frequent_pairs_no_results(sample_graph):
    result = frequent_pairs(sample_graph, min_support=10)
    assert result == []


# ============================================================
# 4. TOP PRODUCT BUNDLES (SORTING) TESTS
# ============================================================

def test_top_product_bundles_order(sample_graph):
    result = top_product_bundles(sample_graph, k=2)

    # butter-jam has highest weight (4)
    assert result[0][0] == ("butter", "jam")
    assert result[0][1] == 4


def test_top_product_bundles_limit(sample_graph):
    result = top_product_bundles(sample_graph, k=1)
    assert len(result) == 1


# ============================================================
# 5. RECOMMENDATION TESTS
# ============================================================

def test_recommend_items_basic(sample_graph):
    result = recommend_items(sample_graph, "bread", top_n=2)
    items = [item for item, _ in result]

    assert items[0] == "milk"  # highest frequency
    assert "butter" in items


def test_recommend_items_nonexistent(sample_graph):
    result = recommend_items(sample_graph, "nonexistent")
    assert result == []


# ============================================================
# 6. STRONGEST ASSOCIATIONS TESTS
# ============================================================

def test_strongest_associations_top(sample_graph):
    result = strongest_associations(sample_graph, top_n=1)

    assert result[0] == ("butter", "jam", 4)


def test_strongest_associations_count(sample_graph):
    result = strongest_associations(sample_graph, top_n=3)
    assert len(result) == 3
