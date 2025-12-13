# app.py
"""
Streamlit frontend for Task 2 – Market Basket Analysis using Graph Algorithms.

Features:
- Load the dataset and build CoPurchaseGraph
- Identify related items using BFS and DFS
- Top product bundles / frequent pairs
- Recommendation queries
- Inspect neighbours of an item
- Display strongest associations
"""

import streamlit as st


from transaction_loader import build_graph_from_file
from graph_algorithms import (
    bfs_related_items,
    dfs_related_items,
    recommend_items,
    top_product_bundles,
    frequent_pairs,
    strongest_associations,
)

import matplotlib.pyplot as plt
import numpy as np

def draw_bfs_graph(start_item, bfs_list):
    fig, ax = plt.subplots(figsize=(8, 8))

    # Center node (start item)
    ax.scatter(0, 0, s=600, color="blue")
    ax.text(0, 0, start_item, fontsize=14, ha='center', va='center', color="white")

    # Arrange related items in a circle
    n = len(bfs_list)
    angles = np.linspace(0, 2*np.pi, n, endpoint=False)

    for i, item in enumerate(bfs_list):
        x = 4 * np.cos(angles[i])
        y = 4 * np.sin(angles[i])

        ax.scatter(x, y, s=300, color="#66b3ff")
        ax.text(x, y, item, fontsize=10, ha='center', va='center')

        # Draw edge to the center
        ax.plot([0, x], [0, y], color="gray", linewidth=1)

    ax.set_title(f"BFS Related Items for '{start_item}'")
    ax.axis("off")
    return fig


def draw_dfs_graph(start_item, dfs_list):
    fig, ax = plt.subplots(figsize=(8, 8))

    # Start node
    ax.scatter(0, 0, s=600, color="red")
    ax.text(0, 0, start_item, fontsize=14, ha='center', va='center', color="white")

    # DFS chain = linear path
    x = 0
    y = 0
    dx = 3

    for i, item in enumerate(dfs_list):
        x_new = x + dx
        ax.scatter(x_new, y, s=300, color="#ff9999")
        ax.text(x_new, y, item, fontsize=10, ha='center', va='center')

        # draw line
        ax.plot([x, x_new], [y, y], color="gray", linewidth=1)

        x = x_new  # move to next

    ax.set_title(f"DFS Deep Association Chain for '{start_item}'")
    ax.axis("off")
    return fig


# ============================================================
# Streamlit App
# ============================================================

st.set_page_config(page_title="Supermarket Basket Graph Analysis", layout="wide")

st.title("🛒 Supermarket Basket Analysis (Task 2 – Graph Algorithms)")
st.write(
    """
    This interface uses a graph-based data structure to analyse supermarket transactions.
    Algorithms demonstrated include BFS, DFS, frequent-pair mining, and ranking/sorting 
    of product bundles.
    """
)

# -----------------------------
# Load Dataset & Build Graph
# -----------------------------
st.sidebar.header("📂 Data Loading")

filename = st.sidebar.text_input(
    "Dataset CSV file:",
    value="Supermarket_dataset_PAI.csv",
    help="Your file must be in the working directory.",
)

if st.sidebar.button("Build Graph"):
    try:
        graph_obj = build_graph_from_file(filename)
        graph = graph_obj.as_adjacency_dict()
        st.success(f"Graph built successfully: {graph_obj.num_items()} items, {graph_obj.num_edges()} edges.")
        st.session_state["graph"] = graph
        st.session_state["graph_obj"] = graph_obj
    except Exception as e:
        st.error(f"Error: {e}")

# Stop if graph hasn't been built yet
if "graph" not in st.session_state:
    st.info("Load the dataset to begin exploring the graph algorithms.")
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
    "🌐 Related Items (BFS / DFS)"
])


# ============================================================
# TAB 1 — ITEM EXPLORER
# ============================================================
with tab1:
    st.header("🔍 Item Explorer")
    selected_item = st.selectbox("Select an item:", items)

    st.subheader(f"Direct Neighbours of **{selected_item}**")
    neighbours = graph_obj.neighbours(selected_item)

    if neighbours:
        st.table({
            "Item": list(neighbours.keys()),
            "Co-purchase Count": list(neighbours.values())
        })
    else:
        st.info("This item has no direct co-purchases.")

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
    item = st.selectbox("Choose an item:", items, key="rec_item")
    n = st.slider("Number of recommendations:", 1, 10, 5)

    results = recommend_items(graph, item, top_n=n)

    if results:
        st.subheader(f"Items most frequently bought with **{item}**:")
        st.table({
            "Item": [i for i, _ in results],
            "Frequency": [f for _, f in results]
        })
    else:
        st.info("No recommendations available for this item.")


# ============================================================
# TAB 3 — FREQUENT PAIRS
# ============================================================
with tab3:
    st.header("👥 Frequent Item Pairs (Pairwise Counting Algorithm)")

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
        st.info("No item pairs meet the minimum support threshold.")


# ============================================================
# TAB 4 — TOP BUNDLES
# ============================================================
with tab4:
    st.header("🏆 Top Product Bundles (Sorting & Ranking Algorithm)")

    k = st.slider("Show top K bundles:", 1, 20, 5)

    bundles = top_product_bundles(graph, k=k)

    st.table({
        "Item A": [pair[0][0] for pair in bundles],
        "Item B": [pair[0][1] for pair in bundles],
        "Frequency": [pair[1] for pair in bundles],
    })


# ============================================================
# TAB 5 — BFS / DFS RELATED ITEMS
# ============================================================
with tab5:
    st.header("🌐 Related Items Using BFS & DFS")
    
    start_item = st.selectbox("Select starting item:", items, key="related_item")

    st.subheader("🔍 Direct Co-Purchases (Most Useful Insight)")
    direct = graph_obj.neighbours(start_item)
    if direct:
        st.table({
            "Item": list(direct.keys()),
            "Co-purchase Count": list(direct.values())
        })
    else:
        st.info("No direct associations found.")

    # BFS & DFS results
    bfs_all = bfs_related_items(graph, start_item)[:15]
    dfs_all = dfs_related_items(graph, start_item)[:15]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔵 BFS – Closest Related Items (Visual)")
        if bfs_all:
            fig = draw_bfs_graph(start_item, bfs_all)
            st.pyplot(fig)
        else:
            st.info("No BFS-related items found.")

    with col2:
        st.subheader("🔴 DFS – Deepest Association Chain (Visual)")
        if dfs_all:
            fig = draw_dfs_graph(start_item, dfs_all)
            st.pyplot(fig)
        else:
            st.info("No DFS-related items found.")

    # Optional: text display below
    st.subheader("📜 BFS Text Output")
    st.write(", ".join(bfs_all) if bfs_all else "None")

    st.subheader("📜 DFS Text Output")
    st.write(" → ".join(dfs_all) if dfs_all else "None")



