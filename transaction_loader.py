# transaction_loader.py
"""
Utility functions for loading the supermarket dataset and building
a co-purchase graph based on (member_id, date) transaction grouping.
"""

import csv
from collections import defaultdict
from itertools import combinations
from typing import Dict, List, Tuple

from copurchase_graph import CoPurchaseGraph


def load_transactions(filename: str) -> Dict[Tuple[str, str], List[str]]:
    """
    Read the supermarket dataset and group items by (member_id, date).

    Returns:
        transactions: dict where key = (member_id, date)
                      value = list of itemDescriptions for that transaction

    Example:
        {
            ("1001", "2024-01-01") : ["BREAD", "MILK", "EGGS"],
            ("2002", "2024-01-01") : ["BANANAS", "APPLES"]
        }
    """

    transactions = defaultdict(list)

    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Ensure dataset has the required fields
        required = {"member_id", "date", "itemDescription"}
        if not required.issubset(reader.fieldnames):
            raise ValueError(
                f"CSV must contain columns: {required}. Found: {reader.fieldnames}"
            )

        for row in reader:
            member = row["member_id"].strip()
            date = row["date"].strip()
            item = row["itemDescription"].strip()

            if item:  # ignore empty rows
                transactions[(member, date)].append(item)

    return transactions


def build_graph_from_file(filename: str) -> CoPurchaseGraph:
    """
    Build and return a CoPurchaseGraph from the CSV dataset.

    Steps:
        1. Load transactions grouped by (member_id, date)
        2. For each transaction basket, generate all item pairs
        3. Add co-purchases to the graph

    Returns:
        CoPurchaseGraph instance filled with item co-occurrence edges.
    """

    transactions = load_transactions(filename)

    graph = CoPurchaseGraph()

    for basket in transactions.values():
        # Remove exact duplicates within the same basket
        unique_items = list(set(basket))

        # Ensure nodes exist
        for item in unique_items:
            graph.add_item(item)

        # Add co-purchase edges for every unordered pair
        for itemA, itemB in combinations(unique_items, 2):
            graph.add_co_purchase(itemA, itemB)

    return graph
