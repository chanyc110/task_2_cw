# app.py
"""
Streamlit frontend for Task 2 – Market Basket Analysis using Graph Algorithms.

Features:
- Load the dataset and build CoPurchaseGraph
- BFS and DFS traversal
- Top product bundles / frequent pairs
- Recommendation queries
- Inspect neighbours of an item
- Simple visualisation of strongest associations (text-based/list)
"""

import streamlit as st
import matplotlib.pyplot as plt

from transaction_loader import build_graph_from_file
from graph_algorithms import (
    bfs,
    dfs,
    recommend_items,
    top_product_bundles,
    frequent_pairs,
    strongest_associations,
)


# ============================================================
# Streamlit App
# ============================================================

st.set_page_config(page_title="Supermarket Basket Graph Analysis", layout="wide")

st.title("🛒 Supermarket Basket Analysis (Task 2 – Graph Algorithms)")
st.write(
    """
    This tool visualises and analyses supermarket customer purchase patterns using 
    graph-based algorithms such as BFS/DFS, frequent pair mining, and item recommendations.
    """
)

# -----------------------------
# Load Dataset & Build Graph
# -----------------------------
st.sidebar.header("📂 Data Loading")

filename = st.sidebar.text_input(
    "Dataset CSV file:",
    value="Supermarket_dataset_PAI.csv",
    help="Upload or place the dataset in the working directory.",
)

if st.sidebar.button("Build Graph"):
    try:
        graph_obj = build_graph_from_file(filename)
        graph = graph_obj.as_adjacency_dict()
        st.success(f"Graph successfully built with {graph_obj.num_items()} items and {graph_obj.num_edges()} edges.")
        st.session_state["graph"] = graph
        st.session_state["graph_obj"] = graph_obj
    except Exception as e:
        st.error(f"Error: {e}")

# Stop if no graph loaded yet
if "graph" not in st.session_state:
    st.info("Load the dataset to begin exploring the algorithms.")
    st.stop()

graph = st.session_state["graph"]
graph_obj = st.session_state["graph_obj"]
items = sorted(graph.keys())


# ============================================================
# Tabs for Algorithms
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 Item Explorer",
    "📈 Recommendation Engine",
    "👥 Frequent Pairs",
    "🏆 Top Bundles",
    "🌐 Graph Traversal (BFS / DFS)"
])


# ============================================================
# TAB 1 — ITEM EXPLORER
# ============================================================
with tab1:
    st.header("🔍 Item Explorer")
    selected_item = st.selectbox("Select an item:", items)

    st.subheader(f"Neighbours of **{selected_item}** (Co-purchase counts)")
    neighbours = graph_obj.neighbours(selected_item)

    if neighbours:
        st.table({
            "Item": list(neighbours.keys()),
            "Co-purchase Count": list(neighbours.values())
        })
    else:
        st.info("This item has no co-purchases.")

    st.subheader("Top Associations Across All Items")
    top_assoc = strongest_associations(graph, top_n=10)
    st.table({
        "Item A": [a for a, _, _ in top_assoc],
        "Item B": [b for _, b, _ in top_assoc],
        "Weight": [w for _, _, w in top_assoc],
    })


# ============================================================
# TAB 2 — RECOMMENDATION ENGINE
# ============================================================
with tab2:
    st.header("📈 Recommendation Engine")
    item = st.selectbox("Choose an item to get recommendations:", items, key="rec_item")
    n = st.slider("Number of recommendations:", 1, 10, 5)

    results = recommend_items(graph, item, top_n=n)

    if results:
        st.subheader(f"Items frequently bought with **{item}**:")
        st.table({
            "Item": [i for i, _ in results],
            "Frequency": [f for _, f in results]
        })
    else:
        st.info("This item has no recorded co-purchases.")


# ============================================================
# TAB 3 — FREQUENT PAIRS
# ============================================================
with tab3:
    st.header("👥 Frequent Item Pairs (Simplified Apriori)")
    
    min_support = st.slider(
        "Minimum co-purchase count:",
        1, 20, 2
    )

    fpairs = frequent_pairs(graph, min_support=min_support)

    if fpairs:
        st.table({
            "Item A": [pair[0][0] for pair in fpairs],
            "Item B": [pair[0][1] for pair in fpairs],
            "Support": [pair[1] for pair in fpairs],
        })
    else:
        st.info("No item pairs meet the support threshold.")


# ============================================================
# TAB 4 — TOP BUNDLES
# ============================================================
with tab4:
    st.header("🏆 Top Product Bundles")

    k = st.slider("Show top K bundles:", 1, 20, 5)

    bundles = top_product_bundles(graph, k=k)

    st.table({
        "Item A": [pair[0][0] for pair in bundles],
        "Item B": [pair[0][1] for pair in bundles],
        "Frequency": [pair[1] for pair in bundles],
    })


# ============================================================
# TAB 5 — BFS / DFS TRAVERSAL
# ============================================================
with tab5:
    st.header("🌐 Graph Traversal (BFS / DFS)")
    
    start = st.selectbox("Select starting item:", items, key="traverse_item")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Breadth-First Search (BFS)")
        bfs_result = bfs(graph, start)
        st.write(", ".join(bfs_result))

    with col2:
        st.subheader("Depth-First Search (DFS)")
        dfs_result = dfs(graph, start)
        st.write(", ".join(dfs_result))
