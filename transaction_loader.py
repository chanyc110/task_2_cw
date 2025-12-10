# transaction_loader.py
"""
Utility functions for loading the supermarket dataset and building
a co-purchase graph based on (Member_number, Date) transaction grouping.
"""

import csv
from collections import defaultdict
from itertools import combinations
from typing import Dict, List, Tuple

from copurchase_graph import CoPurchaseGraph


def load_transactions(filename: str) -> Dict[Tuple[str, str], List[str]]:
    """
    Read the supermarket dataset and group items by (Member_number, Date).

    NOTE:
    This version is hardcoded for your dataset, which contains:
        - "Member_number"
        - "Date"
        - "itemDescription"
    """

    transactions = defaultdict(list)

    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Hardcoded column names for your dataset
        member_col = "Member_number"
        date_col = "Date"
        item_col = "itemDescription"

        # Check presence of columns
        if member_col not in reader.fieldnames or \
           date_col not in reader.fieldnames or \
           item_col not in reader.fieldnames:
            raise ValueError(
                f"CSV must contain: {member_col}, {date_col}, {item_col}. "
                f"Found: {reader.fieldnames}"
            )

        # Build baskets
        for row in reader:
            member = row[member_col].strip()
            date = row[date_col].strip()
            item = row[item_col].strip()

            if item:
                transactions[(member, date)].append(item)

    return transactions


def build_graph_from_file(filename: str) -> CoPurchaseGraph:
    """
    Build and return a CoPurchaseGraph using your dataset's columns.

    Steps:
        1. Load transactions grouped by (Member_number, Date)
        2. For each basket, generate item pairs
        3. Add/update edges in the graph
    """

    transactions = load_transactions(filename)

    graph = CoPurchaseGraph()

    for basket in transactions.values():
        unique_items = list(set(basket))  # remove duplicates within same transaction

        for item in unique_items:
            graph.add_item(item)

        for itemA, itemB in combinations(unique_items, 2):
            graph.add_co_purchase(itemA, itemB)

    return graph
