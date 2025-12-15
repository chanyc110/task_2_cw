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

from graph_plotting import (
    draw_ego_network,
    draw_top_k_association_graph
)
from transaction_loader import build_graph_from_file
from graph_algorithms import (
    bfs_related_items,
    dfs_related_items,
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

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔍 Item Explorer",
    "📈 Recommendation Engine",
    "👥 Frequent Pairs",
    "🏆 Top Bundles",
    "🌐 Related Items (BFS / DFS)",
    "🧠 Item Relationship Graph"
])


# ============================================================
# TAB 1 — ITEM EXPLORER
# ============================================================
with tab1:
    st.header("🔍 Item Explorer (Pairwise Analysis)")

    col1, col2 = st.columns(2)

    with col1:
        item_a = st.selectbox("Select first item:", items, key="item_a")

    with col2:
        item_b = st.selectbox("Select second item:", items, key="item_b")

    if item_a == item_b:
        st.warning("Please select two different items to compare.")

    st.subheader("📌 Direct Relationship")

    weight = graph_obj.edge_weight(item_a, item_b)

    if weight > 0:
        st.success(
            f"**{item_a}** and **{item_b}** were co-purchased **{weight} times**."
        )
    else:
        st.info(
            f"**{item_a}** and **{item_b}** were never directly co-purchased."
        )

    # --------------------------------------------------
    # Shared neighbours (bridge items)
    # --------------------------------------------------
    st.subheader("🔗 Shared Associated Items")

    neighbours_a = set(graph_obj.neighbours(item_a).keys())
    neighbours_b = set(graph_obj.neighbours(item_b).keys())

    shared = neighbours_a.intersection(neighbours_b)

    if shared:
        st.table({
            "Shared Item": list(shared),
            "With A": [graph_obj.edge_weight(item_a, x) for x in shared],
            "With B": [graph_obj.edge_weight(item_b, x) for x in shared],
        })
    else:
        st.info("No shared associated items found.")

    # --------------------------------------------------
    # Focused visualisation (optional but useful)
    # --------------------------------------------------
    st.subheader("📊 Relationship Context (Ego View)")

    fig_a = draw_ego_network(item_a, graph, top_n=5)
    fig_b = draw_ego_network(item_b, graph, top_n=5)

    col3, col4 = st.columns(2)

    with col3:
        st.caption(f"Ego Network for **{item_a}**")
        if fig_a:
            st.pyplot(fig_a)
        else:
            st.info("No associations.")

    with col4:
        st.caption(f"Ego Network for **{item_b}**")
        if fig_b:
            st.pyplot(fig_b)
        else:
            st.info("No associations.")


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

    st.subheader("🔍 Direct Co-Purchases")
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

    # Optional: text display below
    st.subheader("📜 BFS Text Output")
    st.write(", ".join(bfs_all) if bfs_all else "None")

    st.subheader("📜 DFS Text Output")
    st.write(" → ".join(dfs_all) if dfs_all else "None")
    
    
with tab6:
    st.header("🧠 Item Relationship Graph (Strongest Associations)")

    k = st.slider("Number of strongest associations to display:", 5, 20, 10)

    fig = draw_top_k_association_graph(graph, top_k=k)
    if fig:
        st.pyplot(fig, width='content')
    else:
        st.info("No associations available to visualise.")




