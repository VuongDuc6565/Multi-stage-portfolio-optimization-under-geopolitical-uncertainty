"""
scenario.py
========================
Scenario tree construction for stochastic optimization
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

# =========================================
# TRANSITION MATRIX (MARKOV)
# =========================================
def estimate_transition_matrix(states):
    unique_states = ["N", "C", "W"]
    P = pd.DataFrame(0, index=unique_states, columns=unique_states)

    for t in range(len(states) - 1):
        i = states.iloc[t]
        j = states.iloc[t+1]
        P.loc[i, j] += 1

    P = P.div(P.sum(axis=1), axis=0)

    return P.fillna(0)


# =========================================
# K-MEANS (SIMPLE VERSION)
# =========================================
def cluster_returns(returns, n_clusters=3):
    """
    Simple clustering via quantiles (robust, no sklearn needed)
    """
    clusters = []

    for col in returns.columns:
        q = returns[col].quantile([0.33, 0.66])
        centers = [q.iloc[1], q.iloc[0], returns[col].min()]
        clusters.append(centers)

    return np.array(clusters).T  # shape (k, N)

def cluster_returns_3(
    returns,
    n_clusters=3,
    random_state=42
):
    """
    Cluster return vectors and map clusters to:
    W = worst
    C = middle
    N = best

    Returns
    -------
    cluster_centers : ndarray
        shape (3,N)
        row order:
        [N,C,W]
    """

    if isinstance(
        returns,
        pd.DataFrame
    ):
        X = returns.values
    else:
        X = np.array(returns)


    kmeans = KMeans(

        n_clusters=n_clusters,

        random_state=random_state,

        n_init=20
    )

    labels = kmeans.fit_predict(X)

    centers = kmeans.cluster_centers_


    # average return of each cluster
    center_mean = centers.mean(
        axis=1
    )


    # ascending:
    # worst → best
    order = np.argsort(
        center_mean
    )

    W_idx = order[0]
    C_idx = order[1]
    N_idx = order[2]


    cluster_centers = np.vstack([

        centers[N_idx],
        centers[C_idx],
        centers[W_idx]

    ])


    tickers = (
        returns.columns.tolist()
        if isinstance(
            returns,
            pd.DataFrame
        )
        else
        [f"A{i}" for i in range(
            X.shape[1]
        )]
    )

    df = pd.DataFrame(

        cluster_centers,

        index=["N","C","W"],

        columns=tickers
    )


    print(
        "\n===== Cluster Centers ====="
    )

    print(
        df.round(4)
    )

    return cluster_centers
    
# =========================================
# BUILD SCENARIO TREE
# =========================================
def build_scenario_tree(P, cluster_centers, T=3):
    """
    Returns:
    - nodes
    - transitions
    - probabilities
    """

    states = ["N", "C", "W"]

    tree = []
    probs = []

    # root
    tree.append([("N", 1.0)])

    for t in range(1, T+1):
        layer = []

        for state, prob in tree[t-1]:
            for next_state in states:
                p = P.loc[state, next_state]

                if p > 0:
                    layer.append((next_state, prob * p))

        tree.append(layer)

    return tree


# =========================================
# ASSIGN RETURNS TO NODES
# =========================================
def assign_returns(tree, cluster_centers):
    """
    Map states → return vectors
    """
    mapping = {"N": 0, "C": 1, "W": 2}

    node_returns = []

    for layer in tree:
        layer_returns = []
        for state, _ in layer:
            idx = mapping[state]
            layer_returns.append(cluster_centers[idx])

        node_returns.append(layer_returns)

    return node_returns