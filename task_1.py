from __future__ import annotations

from pathlib import Path

import networkx as nx

import matplotlib
matplotlib.use("Agg")  # щоб зберігати PNG без відкриття вікна
import matplotlib.pyplot as plt


def build_graph() -> nx.Graph:
    """
    Модель реальної мережі (спрощена транспортна мережа міста).
    Вузли — ключові точки, ребра — прямі з’єднання.
    """
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


def analyze_graph(G: nx.Graph) -> None:
    print("=== Аналіз графа ===")
    print(f"Кількість вершин (nodes): {G.number_of_nodes()}")
    print(f"Кількість ребер (edges):  {G.number_of_edges()}")
    print("\nСтупені вершин (degree):")
    degrees = dict(G.degree())
    for node in sorted(degrees.keys()):
        print(f" - {node}: {degrees[node]}")


def visualize_graph(G: nx.Graph, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=42)

    nx.draw_networkx_nodes(G, pos, node_size=1400)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, font_size=9)

    edge_labels = {(u, v): d["weight"] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    print(f"\n✅ Візуалізацію збережено у файл: {out_path}")


def main() -> None:
    G = build_graph()
    analyze_graph(G)

    base_dir = Path(__file__).parent
    img_path = base_dir / "graph.png"
    visualize_graph(G, img_path)


if __name__ == "__main__":
    main()
