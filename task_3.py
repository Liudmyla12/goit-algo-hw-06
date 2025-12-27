from __future__ import annotations

import heapq
from typing import Dict, List, Optional, Tuple

import networkx as nx


def build_graph() -> nx.Graph:
    G = nx.Graph()
    edges = [
        ("Hbf", "Europaplatz", 5),
        ("Europaplatz", "Marktplatz", 2),
        ("Marktplatz", "KIT", 4),
        ("Europaplatz", "Knielingen", 7),
        ("Hbf", "Messe", 12),
        ("Messe", "Ettlingen", 8),
        ("Ettlingen", "Durlach", 15),
        ("Europaplatz", "Durlach", 10),
        ("Durlach", "Stutensee", 18),
        ("Stutensee", "Bruchsal", 20),
        ("Hbf", "Ettlingen", 10),
        ("KIT", "Durlach", 12),
        ("Knielingen", "Hbf", 9),
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    return G


def dijkstra(G: nx.Graph, start: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    """
    Власна реалізація Дейкстри.
    Повертає:
      - dist: найкоротші відстані від start до всіх вершин
      - prev: попередник для відновлення шляху
    """
    dist: Dict[str, float] = {node: float("inf") for node in G.nodes()}
    prev: Dict[str, Optional[str]] = {node: None for node in G.nodes()}
    dist[start] = 0.0

    pq: List[Tuple[float, str]] = [(0.0, start)]

    while pq:
        cur_dist, u = heapq.heappop(pq)

        if cur_dist > dist[u]:
            continue

        for v, attrs in G[u].items():
            w = float(attrs.get("weight", 1))
            nd = cur_dist + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    return dist, prev


def restore_path(prev: Dict[str, Optional[str]], start: str, goal: str) -> Optional[List[str]]:
    if start == goal:
        return [start]

    cur = goal
    path = []
    while cur is not None:
        path.append(cur)
        if cur == start:
            path.reverse()
            return path
        cur = prev[cur]

    return None


def main() -> None:
    G = build_graph()
    nodes = sorted(G.nodes())

    print("=== Дейкстра: найкоротші шляхи між усіма вершинами ===\n")

    # короткий приклад: один старт -> до всіх
    start = "Hbf"
    dist, prev = dijkstra(G, start)
    print(f"Стартова вершина: {start}")
    for node in nodes:
        print(f" - до {node:12}: {dist[node]:6.1f}")

    # приклад відновлення конкретного маршруту
    a, b = "Marktplatz", "Bruchsal"
    dist2, prev2 = dijkstra(G, a)
    path = restore_path(prev2, a, b)
    print("\nПриклад маршруту:")
    print(f"{a} -> {b}: distance={dist2[b]:.1f}, path={path}")

    # “між усіма вершинами” — запускаємо Дейкстру для кожної вершини
    # (граф маленький, тому це ок)
    all_pairs: Dict[str, Dict[str, float]] = {}
    for s in nodes:
        d, _ = dijkstra(G, s)
        all_pairs[s] = d

    print("\n✅ Готово: відстані пораховано для всіх стартових вершин (all-pairs).")


if __name__ == "__main__":
    main()
