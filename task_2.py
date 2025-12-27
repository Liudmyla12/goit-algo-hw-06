from __future__ import annotations

from collections import deque
from typing import Dict, List, Optional, Set

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


def bfs_path(G: nx.Graph, start: str, goal: str) -> Optional[List[str]]:
    """
    BFS знаходить шлях у порядку “найменша кількість ребер” (у незваженому сенсі).
    """
    if start == goal:
        return [start]

    q = deque([start])
    visited: Set[str] = {start}
    parent: Dict[str, str] = {}

    while q:
        cur = q.popleft()
        for nb in sorted(G.neighbors(cur)):  # sorted -> стабільний результат
            if nb in visited:
                continue
            visited.add(nb)
            parent[nb] = cur
            if nb == goal:
                # відновлення шляху
                path = [goal]
                while path[-1] != start:
                    path.append(parent[path[-1]])
                path.reverse()
                return path
            q.append(nb)

    return None


def dfs_path(G: nx.Graph, start: str, goal: str) -> Optional[List[str]]:
    """
    DFS йде “вглиб” по першому доступному сусіду (порядок залежить від обходу).
    Повертає перший знайдений шлях.
    """
    visited: Set[str] = set()

    def rec(cur: str, path: List[str]) -> Optional[List[str]]:
        if cur == goal:
            return path
        visited.add(cur)
        for nb in sorted(G.neighbors(cur)):
            if nb in visited:
                continue
            res = rec(nb, path + [nb])
            if res is not None:
                return res
        return None

    return rec(start, [start])


def main() -> None:
    G = build_graph()

    start, goal = "Marktplatz", "Messe"

    bfs = bfs_path(G, start, goal)
    dfs = dfs_path(G, start, goal)

    print(f"Start: {start} -> Goal: {goal}\n")
    print(f"BFS path: {bfs}")
    print(f"DFS path: {dfs}\n")

    print("Пояснення (коротко):")
    print("- BFS зазвичай знаходить шлях з меншою кількістю кроків (ребер).")
    print("- DFS може дати інший (часто довший) шлях, бо спочатку “занурюється” в один напрямок.")
    print("- Конкретний шлях залежить від порядку перебору сусідів (тут він зафіксований через sorted()).")


if __name__ == "__main__":
    main()
