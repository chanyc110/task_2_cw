import matplotlib.pyplot as plt
import numpy as np
from graph_algorithms import strongest_associations
from matplotlib.patches import FancyArrowPatch

def draw_ego_network(center_item, graph, top_n=8):
    """
    Item-centred ego network:
    - Center node = selected item
    - Surrounding nodes = strongest co-purchases
    - Edge thickness = co-purchase frequency
    """

    neighbours = graph.get(center_item, {})
    if not neighbours:
        return None

    # Select top-N strongest neighbours
    sorted_neighbours = sorted(
        neighbours.items(), key=lambda x: x[1], reverse=True
    )[:top_n]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_title(f"Ego Network for '{center_item}'", fontsize=14)

    # Draw center node
    ax.scatter(0, 0, s=1000, color="#1f77b4", zorder=3)
    ax.text(0, 0, center_item, color="black", ha="center", va="center", fontsize=12)

    angles = np.linspace(0, 2*np.pi, len(sorted_neighbours), endpoint=False)
    radius = 4

    for i, (item, weight) in enumerate(sorted_neighbours):
        x = radius * np.cos(angles[i])
        y = radius * np.sin(angles[i])

        # Edge
        ax.plot([0, x], [0, y], linewidth=1 + weight * 0.15, color="gray", alpha=0.7)

        # Node
        ax.scatter(x, y, s=400, color="#aec7e8")
        ax.text(x * 1.1, y * 1.1, item, ha="center", va="center", fontsize=9)

    ax.axis("off")
    return fig


def draw_top_k_association_graph(graph, top_k=8):
    """
    Clean global relationship graph showing top-K strongest associations.
    Designed for readability and coursework presentation.
    """

    edges = strongest_associations(graph, top_n=top_k)
    if not edges:
        return None

    # Collect unique nodes
    nodes = list({item for a, b, _ in edges for item in (a, b)})

    # Compact figure (smaller frame)
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    ax.set_title(
        f"Top {top_k} Strongest Item Associations",
        fontsize=13,
        pad=10
    )

    # Manual layout (balanced, readable)
    angles = np.linspace(0, 2*np.pi, len(nodes), endpoint=False)
    radius = 3
    pos = {
        node: (radius * np.cos(a), radius * np.sin(a))
        for node, a in zip(nodes, angles)
    }

    # Draw edges FIRST (thin, subtle)
    for a, b, weight in edges:
        x1, y1 = pos[a]
        x2, y2 = pos[b]

        ax.plot(
            [x1, x2],
            [y1, y2],
            linewidth=0.8 + weight * 0.08,   # controlled scaling
            color="gray",
            alpha=0.6,
            zorder=1
        )

    # Draw nodes
    for node, (x, y) in pos.items():
        ax.scatter(
            x, y,
            s=420,
            color="#f2a900",    # warm highlight colour
            edgecolors="black",
            zorder=2
        )
        ax.text(
            x,
            y,
            node,
            fontsize=9,
            ha="center",
            va="center",
            zorder=3
        )

    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()
    return fig

def draw_top_k_association_graph(graph, top_k=8):
    """
    Clean, reference-style item relationship graph
    showing top-K strongest associations.
    """

    edges = strongest_associations(graph, top_n=top_k)
    if not edges:
        return None

    # Unique nodes
    nodes = list({n for a, b, _ in edges for n in (a, b)})

    # Compact figure (fits Streamlit window)
    fig, ax = plt.subplots(figsize=(5.8, 4.8))
    ax.set_title(
        f"Top {top_k} Strongest Item Associations",
        fontsize=12,
        pad=8
    )

    # Balanced circular layout
    angles = np.linspace(0, 2 * np.pi, len(nodes), endpoint=False)
    radius = 2.4
    pos = {
        node: (radius * np.cos(a), radius * np.sin(a))
        for node, a in zip(nodes, angles)
    }

    # Draw thin arrow edges
    for a, b, _ in edges:
        x1, y1 = pos[a]
        x2, y2 = pos[b]

        arrow = FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle='-|>',
            linewidth=0.8,
            color='gray',
            alpha=0.6,
            mutation_scale=10,
            zorder=1
        )
        ax.add_patch(arrow)

    # Draw nodes
    for node, (x, y) in pos.items():
        ax.scatter(
            x, y,
            s=520,
            color='#f2a900',
            edgecolors='black',
            linewidth=1.1,
            zorder=2
        )
        ax.text(
            x, y,
            node,
            ha='center',
            va='center',
            fontsize=9,
            fontweight='bold',
            zorder=3
        )

    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()
    return fig


