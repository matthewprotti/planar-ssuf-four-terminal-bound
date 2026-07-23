#!/usr/bin/env python3
"""Exact graph-native verifier for the 335/294 four-terminal SSUF witness.

The script uses only the Python standard library.  It reconstructs all
source-terminal paths from the directed edge list, checks acyclicity,
connectedness, and a supplied genus-zero rotation system, verifies a K4-minor
certificate, builds the fractional flow from path amounts, checks legal
commodity-independent per-unit arc costs and flow conservation, and enumerates
all 2^4 unsplittable routings on all 13 arcs using exact integers.

The CSV and JSON files are outputs; neither is read by the verifier.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from typing import Mapping, Sequence
import csv
import hashlib
import json

Arc = tuple[str, str]
PathType = tuple[Arc, ...]


class VerificationError(RuntimeError):
    """Raised when a certificate check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


@dataclass(frozen=True)
class InstanceData:
    source: str
    vertices: tuple[str, ...]
    terminals: tuple[str, ...]
    trunk: tuple[Arc, ...]
    arcs: tuple[Arc, ...]
    demands: Mapping[str, int]
    cheap_amounts: Mapping[str, int]
    charged_expensive_arc: Mapping[str, Arc]
    costs: Mapping[Arc, int]
    full_expensive_cost: int
    rotation: Mapping[str, tuple[str, ...]]
    k4_branch_sets: Mapping[str, frozenset[str]]


@dataclass(frozen=True)
class ExpectedData:
    d_max: int
    trunk_loads: tuple[int, ...]
    private_loads: tuple[int, ...]
    fractional_cost: int
    three_expensive_cost: int
    feasible_routing_count: int
    min_max_overload: int
    ratio: Fraction
    exactly_two_cases: Mapping[str, tuple[int, str]]
    exact_witness_choices: str
    exact_witness_deltas: tuple[int, ...]


SOURCE = "s"
VERTICES = ("s", "v1", "v2", "v3", "v4", "v5", "t1", "t2", "t3", "t4")
TERMINALS = ("t1", "t2", "t3", "t4")
TRUNK: tuple[Arc, ...] = (
    ("s", "v1"),
    ("v1", "v2"),
    ("v2", "v3"),
    ("v3", "v4"),
    ("v4", "v5"),
)
ARCS: tuple[Arc, ...] = TRUNK + (
    ("s", "t1"), ("v3", "t1"),
    ("s", "t2"), ("v5", "t2"),
    ("v1", "t3"), ("v5", "t3"),
    ("v2", "t4"), ("v4", "t4"),
)
DEMAND = {"t1": 294, "t2": 216, "t3": 252, "t4": 294}
CHEAP_AMOUNT = {"t1": 78, "t2": 97, "t3": 36, "t4": 42}
CHARGED_EXPENSIVE_ARC = {
    "t1": ("s", "t1"),
    "t2": ("s", "t2"),
    "t3": ("v1", "t3"),
    "t4": ("v2", "t4"),
}
COST = {arc: 0 for arc in ARCS}
COST.update({
    ("s", "t1"): 36,
    ("s", "t2"): 49,
    ("v1", "t3"): 42,
    ("v2", "t4"): 36,
})
ROTATION = {
    "s":  ("v1", "t2", "t1"),
    "v1": ("s", "v2", "t3"),
    "v2": ("v1", "v3", "t4"),
    "v3": ("v2", "t1", "v4"),
    "v4": ("v3", "v5", "t4"),
    "v5": ("v4", "t2", "t3"),
    "t1": ("v3", "s"),
    "t2": ("v5", "s"),
    "t3": ("v5", "v1"),
    "t4": ("v4", "v2"),
}
K4_BRANCH_SETS = {
    "A": frozenset({"s", "t1", "t2"}),
    "B": frozenset({"v1", "v2", "t3", "t4"}),
    "C": frozenset({"v3", "v4"}),
    "D": frozenset({"v5"}),
}

DEFAULT_INSTANCE = InstanceData(
    source=SOURCE,
    vertices=VERTICES,
    terminals=TERMINALS,
    trunk=TRUNK,
    arcs=ARCS,
    demands=DEMAND,
    cheap_amounts=CHEAP_AMOUNT,
    charged_expensive_arc=CHARGED_EXPENSIVE_ARC,
    costs=COST,
    full_expensive_cost=10_584,
    rotation=ROTATION,
    k4_branch_sets=K4_BRANCH_SETS,
)

EXPECTED = ExpectedData(
    d_max=294,
    trunk_loads=(721, 505, 253, 175, 133),
    private_loads=(216, 78, 119, 97, 216, 36, 252, 42),
    fractional_cost=31_751,
    three_expensive_cost=31_752,
    feasible_routing_count=11,
    min_max_overload=335,
    ratio=Fraction(335, 294),
    exactly_two_cases={
        "CCEE": (335, "s->v1"),
        "CECE": (335, "v1->v2"),
        "CEEC": (335, "v2->v3"),
        "ECCE": (335, "v4->v5"),
        "ECEC": (335, "v3->v4"),
        "EECC": (371, "v3->v4"),
    },
    exact_witness_choices="CCEE",
    exact_witness_deltas=(
        335, 299, 257, 41, 83,
        -216, 216, -119, 119, 36, -36, 42, -42,
    ),
)


def directed_adjacency(data: InstanceData) -> dict[str, tuple[str, ...]]:
    adjacency: dict[str, list[str]] = {v: [] for v in data.vertices}
    for u, v in data.arcs:
        require(u in adjacency and v in adjacency, f"arc {u}->{v} uses an unknown vertex")
        adjacency[u].append(v)
    return {v: tuple(adjacency[v]) for v in data.vertices}


def topological_order(data: InstanceData) -> tuple[str, ...]:
    adjacency = directed_adjacency(data)
    indegree = {v: 0 for v in data.vertices}
    for _, v in data.arcs:
        indegree[v] += 1
    queue = deque(v for v in data.vertices if indegree[v] == 0)
    order: list[str] = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adjacency[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    require(len(order) == len(data.vertices), "directed graph contains a cycle")
    return tuple(order)


def underlying_adjacency(data: InstanceData) -> dict[str, set[str]]:
    adjacency = {v: set() for v in data.vertices}
    for u, v in data.arcs:
        require(u != v, f"loop {u}->{v} is not allowed")
        adjacency[u].add(v)
        adjacency[v].add(u)
    return adjacency


def check_connected(data: InstanceData) -> None:
    adjacency = underlying_adjacency(data)
    reached = {data.source}
    queue = deque([data.source])
    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if v not in reached:
                reached.add(v)
                queue.append(v)
    require(reached == set(data.vertices), "underlying graph is disconnected")


def all_simple_paths(data: InstanceData, target: str) -> tuple[PathType, ...]:
    adjacency = directed_adjacency(data)
    paths: list[PathType] = []

    def dfs(vertex: str, visited: set[str], path: list[Arc]) -> None:
        if vertex == target:
            paths.append(tuple(path))
            return
        for nxt in adjacency[vertex]:
            if nxt in visited:
                continue
            path.append((vertex, nxt))
            visited.add(nxt)
            dfs(nxt, visited, path)
            visited.remove(nxt)
            path.pop()

    dfs(data.source, {data.source}, [])
    return tuple(paths)


def classify_paths(data: InstanceData) -> dict[str, dict[str, PathType]]:
    paths: dict[str, dict[str, PathType]] = {}
    for terminal in data.terminals:
        found = all_simple_paths(data, terminal)
        require(len(found) == 2, f"{terminal} has {len(found)} source paths, expected 2")
        charged = data.charged_expensive_arc[terminal]
        expensive = [path for path in found if charged in path]
        cheap = [path for path in found if charged not in path]
        require(len(expensive) == 1 and len(cheap) == 1,
                f"could not classify the two paths for {terminal}")
        paths[terminal] = {"E": expensive[0], "C": cheap[0]}
    return paths


def check_genus_zero_rotation(data: InstanceData) -> tuple[tuple[Arc, ...], ...]:
    """Verify that the supplied rotation system defines a spherical embedding."""
    check_connected(data)
    undirected_edges = {frozenset(arc) for arc in data.arcs}
    require(len(undirected_edges) == len(data.arcs),
            "parallel or antiparallel arcs collapse in the undirected graph")
    adjacency = underlying_adjacency(data)

    require(set(data.rotation) == set(data.vertices), "rotation omits or adds a vertex")
    for vertex in data.vertices:
        require(set(data.rotation[vertex]) == adjacency[vertex],
                f"rotation at {vertex} does not match its undirected neighbors")
        require(len(data.rotation[vertex]) == len(adjacency[vertex]),
                f"rotation at {vertex} repeats a neighbor")

    darts: set[Arc] = set()
    for edge in undirected_edges:
        u, v = sorted(edge)
        darts.add((u, v))
        darts.add((v, u))

    seen: set[Arc] = set()
    faces: list[tuple[Arc, ...]] = []
    for start in sorted(darts):
        if start in seen:
            continue
        face: list[Arc] = []
        current = start
        while current not in seen:
            seen.add(current)
            face.append(current)
            u, v = current
            neighbors = data.rotation[v]
            index = neighbors.index(u)
            w = neighbors[(index - 1) % len(neighbors)]
            current = (v, w)
        require(current == start, "face walk closed into a different orbit")
        faces.append(tuple(face))

    require(seen == darts, "not every directed edge-side belongs to a face orbit")
    require(sum(len(face) for face in faces) == 2 * len(undirected_edges),
            "face lengths do not sum to twice the edge count")
    euler = len(data.vertices) - len(undirected_edges) + len(faces)
    require(euler == 2, f"rotation has Euler characteristic {euler}, not 2")
    return tuple(faces)


def check_k4_minor(data: InstanceData) -> None:
    adjacency = underlying_adjacency(data)
    branch_sets = list(data.k4_branch_sets.items())
    require(len(branch_sets) == 4, "K4 certificate must have four branch sets")
    used: set[str] = set()
    for label, branch in branch_sets:
        require(bool(branch), f"branch set {label} is empty")
        require(not (used & set(branch)), f"branch set {label} overlaps a previous set")
        require(set(branch) <= set(data.vertices), f"branch set {label} uses an unknown vertex")
        used |= set(branch)
        start = next(iter(branch))
        reached = {start}
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adjacency[u] & set(branch):
                if v not in reached:
                    reached.add(v)
                    queue.append(v)
        require(reached == set(branch), f"branch set {label} is disconnected")

    for (label_a, branch_a), (label_b, branch_b) in combinations(branch_sets, 2):
        adjacent = any(v in branch_b for u in branch_a for v in adjacency[u])
        require(adjacent, f"branch sets {label_a} and {label_b} are not adjacent")


def path_cost(data: InstanceData, path: PathType) -> int:
    return sum(data.costs[arc] for arc in path)


def add_path(load: dict[Arc, int], path: PathType, amount: int, arc_set: set[Arc]) -> None:
    require(amount >= 0, "path amount is negative")
    for arc in path:
        require(arc in arc_set, f"path uses unknown arc {arc}")
        load[arc] += amount


def fractional_load(data: InstanceData, paths: Mapping[str, Mapping[str, PathType]]) -> dict[Arc, int]:
    load: defaultdict[Arc, int] = defaultdict(int)
    arc_set = set(data.arcs)
    for terminal in data.terminals:
        demand = data.demands[terminal]
        cheap = data.cheap_amounts[terminal]
        require(0 <= cheap <= demand, f"invalid cheap amount for {terminal}")
        add_path(load, paths[terminal]["C"], cheap, arc_set)
        add_path(load, paths[terminal]["E"], demand - cheap, arc_set)
    return {arc: load[arc] for arc in data.arcs}


def unsplittable_load(
    data: InstanceData,
    paths: Mapping[str, Mapping[str, PathType]],
    choices: Mapping[str, str],
) -> dict[Arc, int]:
    load: defaultdict[Arc, int] = defaultdict(int)
    arc_set = set(data.arcs)
    for terminal in data.terminals:
        add_path(load, paths[terminal][choices[terminal]], data.demands[terminal], arc_set)
    return {arc: load[arc] for arc in data.arcs}


def flow_cost(data: InstanceData, load: Mapping[Arc, int]) -> int:
    return sum(data.costs[arc] * load[arc] for arc in data.arcs)


def check_flow_conservation(data: InstanceData, load: Mapping[Arc, int]) -> None:
    net_out: defaultdict[str, int] = defaultdict(int)
    for (u, v), amount in load.items():
        require(amount >= 0, f"negative load on {u}->{v}")
        net_out[u] += amount
        net_out[v] -= amount
    total_demand = sum(data.demands.values())
    require(net_out[data.source] == total_demand, "source balance is wrong")
    for terminal in data.terminals:
        require(net_out[terminal] == -data.demands[terminal],
                f"terminal balance is wrong at {terminal}")
    for vertex in set(data.vertices) - {data.source, *data.terminals}:
        require(net_out[vertex] == 0, f"flow is not conserved at {vertex}")


def enumerate_routings(
    data: InstanceData,
    paths: Mapping[str, Mapping[str, PathType]],
    x: Mapping[Arc, int],
) -> list[dict[str, object]]:
    x_cost = flow_cost(data, x)
    rows: list[dict[str, object]] = []
    for bits in product(("E", "C"), repeat=len(data.terminals)):
        choices = dict(zip(data.terminals, bits, strict=True))
        y = unsplittable_load(data, paths, choices)
        check_flow_conservation(data, y)
        deltas = {arc: y[arc] - x[arc] for arc in data.arcs}
        witness_arc = max(data.arcs, key=lambda arc: (deltas[arc], -data.arcs.index(arc)))
        cost = flow_cost(data, y)
        row: dict[str, object] = {
            "choices_t1_t2_t3_t4": "".join(bits),
            "cheap_count": bits.count("C"),
            "cost": cost,
            "cost_feasible": cost <= x_cost,
            "max_overload": deltas[witness_arc],
            "witness_arc": f"{witness_arc[0]}->{witness_arc[1]}",
        }
        for u, v in data.arcs:
            row[f"load_{u}_{v}"] = y[(u, v)]
            row[f"delta_{u}_{v}"] = deltas[(u, v)]
        rows.append(row)
    return rows


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(rows: Sequence[Mapping[str, object]], path: Path) -> None:
    require(bool(rows), "cannot write an empty routing table")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def verify_instance(
    data: InstanceData = DEFAULT_INSTANCE,
    expected: ExpectedData = EXPECTED,
    output_dir: Path | None = None,
) -> dict[str, object]:
    require(len(set(data.vertices)) == len(data.vertices), "vertex list has duplicates")
    require(len(set(data.arcs)) == len(data.arcs), "arc list has duplicates")
    require(set(data.terminals) <= set(data.vertices), "terminal list uses unknown vertices")
    require(all(t not in {u for u, _ in data.arcs} for t in data.terminals),
            "a terminal has an outgoing arc")
    require(set(data.costs) == set(data.arcs), "cost vector is not defined on exactly all arcs")
    require(all(cost >= 0 for cost in data.costs.values()), "a per-unit arc cost is negative")
    require(set(data.demands) == set(data.terminals), "demands do not match terminals")
    require(set(data.cheap_amounts) == set(data.terminals), "path amounts do not match terminals")

    order = topological_order(data)
    faces = check_genus_zero_rotation(data)
    check_k4_minor(data)
    paths = classify_paths(data)

    for terminal in data.terminals:
        require(path_cost(data, paths[terminal]["C"]) == 0,
                f"cheap path for {terminal} has nonzero cost")
        expensive_per_unit = path_cost(data, paths[terminal]["E"])
        require(expensive_per_unit * data.demands[terminal] == data.full_expensive_cost,
                f"full expensive cost is not equalized for {terminal}")

    x = fractional_load(data, paths)
    check_flow_conservation(data, x)
    x_cost = flow_cost(data, x)
    rows = enumerate_routings(data, paths, x)
    feasible = [row for row in rows if bool(row["cost_feasible"])]
    infeasible = [row for row in rows if not bool(row["cost_feasible"])]
    min_max_overload = min(int(row["max_overload"]) for row in feasible)
    d_max = max(data.demands.values())
    ratio = Fraction(min_max_overload, d_max)

    require(d_max == expected.d_max, f"d_max={d_max}, expected {expected.d_max}")
    require(tuple(x[arc] for arc in data.trunk) == expected.trunk_loads,
            "fractional trunk-load vector differs from the certificate")
    private_arcs = tuple(arc for arc in data.arcs if arc not in set(data.trunk))
    require(tuple(x[arc] for arc in private_arcs) == expected.private_loads,
            "fractional private-arc loads differ from the certificate")
    require(x_cost == expected.fractional_cost,
            f"fractional cost {x_cost}, expected {expected.fractional_cost}")
    require(3 * data.full_expensive_cost == expected.three_expensive_cost,
            "three-expensive threshold differs from the certificate")
    require(expected.three_expensive_cost > x_cost,
            "three expensive choices are not excluded by cost")
    require(len(rows) == 16, "routing enumeration did not produce 16 choices")
    require(len(feasible) == expected.feasible_routing_count,
            f"found {len(feasible)} cost-feasible routings")
    require(len(infeasible) == 16 - expected.feasible_routing_count,
            "wrong number of cost-infeasible routings")
    require(all(int(row["cheap_count"]) >= 2 for row in feasible),
            "a cost-feasible routing has fewer than two cheap choices")
    require(all(int(row["cheap_count"]) <= 1 for row in infeasible),
            "a cost-infeasible routing has at least two cheap choices")
    require(min_max_overload == expected.min_max_overload,
            f"minimum maximum overload {min_max_overload}, expected {expected.min_max_overload}")
    require(ratio == expected.ratio, f"ratio {ratio}, expected {expected.ratio}")

    exactly_two = {
        str(row["choices_t1_t2_t3_t4"]): (
            int(row["max_overload"]), str(row["witness_arc"])
        )
        for row in feasible
        if int(row["cheap_count"]) == 2
    }
    require(exactly_two == dict(expected.exactly_two_cases),
            "exactly-two-cheap routing table differs from the certificate")

    witness_rows = [row for row in feasible
                    if row["choices_t1_t2_t3_t4"] == expected.exact_witness_choices]
    require(len(witness_rows) == 1, "exact finite-optimum witness is missing")
    witness = witness_rows[0]
    witness_deltas = tuple(int(witness[f"delta_{u}_{v}"]) for u, v in data.arcs)
    require(witness_deltas == expected.exact_witness_deltas,
            "full deviation vector of the exact witness differs")
    require(int(witness["max_overload"]) == min_max_overload,
            "displayed witness does not attain the finite optimum")

    require(max(int(row[f"delta_{u}_{v}"])
                for row in rows for u, v in private_arcs) <= d_max,
            "a private-arc positive deviation exceeds d_max")

    summary: dict[str, object] = {
        "vertices": list(data.vertices),
        "arcs": [list(arc) for arc in data.arcs],
        "topological_order": list(order),
        "underlying_graph_connected": True,
        "number_of_embedding_faces": len(faces),
        "euler_characteristic": len(data.vertices) - len(data.arcs) + len(faces),
        "embedding_faces_as_darts": [[list(dart) for dart in face] for face in faces],
        "demands": dict(data.demands),
        "cheap_amounts": dict(data.cheap_amounts),
        "expensive_amounts": {
            terminal: data.demands[terminal] - data.cheap_amounts[terminal]
            for terminal in data.terminals
        },
        "fractional_loads": {f"{u}->{v}": x[(u, v)] for u, v in data.arcs},
        "fractional_cost": x_cost,
        "full_expensive_cost_per_terminal": data.full_expensive_cost,
        "minimum_max_overload_among_cost_feasible_routings": min_max_overload,
        "d_max": d_max,
        "ratio": str(ratio),
        "ratio_decimal": float(ratio),
        "number_of_routings": len(rows),
        "number_of_cost_feasible_routings": len(feasible),
        "exactly_two_cheap_cases": exactly_two,
        "exact_finite_optimum_witness": {
            "choices": expected.exact_witness_choices,
            "deltas_in_arc_order": list(witness_deltas),
        },
        "k4_minor_branch_sets": {
            key: sorted(value) for key, value in data.k4_branch_sets.items()
        },
    }

    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        csv_path = output_dir / "concrete_16_routings.csv"
        json_path = output_dir / "concrete_verification_summary.json"
        write_csv(rows, csv_path)
        json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        summary["csv_sha256"] = sha256(csv_path)
        summary["json_sha256"] = sha256(json_path)

    return summary


def main() -> None:
    output_dir = Path(__file__).resolve().parent
    summary = verify_instance(output_dir=output_dir)
    print("PASS: directed graph is acyclic.")
    print("PASS: underlying graph is connected.")
    print(
        "PASS: supplied rotation system defines a genus-zero embedding "
        f"with {summary['number_of_embedding_faces']} faces."
    )
    print("PASS: each terminal is a sink and has exactly two source-terminal paths.")
    print("PASS: the underlying graph contains the stated K4 minor.")
    print("PASS: costs are legal nonnegative commodity-independent per-unit arc costs.")
    print("PASS: fractional flow conservation holds at every vertex.")
    print(
        f"Fractional cost = {summary['fractional_cost']}; "
        f"three expensive choices cost {EXPECTED.three_expensive_cost}."
    )
    print(
        f"Cost-feasible routings = {summary['number_of_cost_feasible_routings']} of 16; "
        "all have at least two cheap choices."
    )
    print(
        "Minimum max overload over all cost-feasible routings = "
        f"{summary['minimum_max_overload_among_cost_feasible_routings']}."
    )
    print(f"Certificate ratio = {summary['ratio']} = {summary['ratio_decimal']:.12f}.")
    print("PASS: CCEE attains the exact finite optimum with the displayed full deviation vector.")
    print(f"Wrote concrete_16_routings.csv (sha256 {summary['csv_sha256']}).")
    print(f"Wrote concrete_verification_summary.json (sha256 {summary['json_sha256']}).")


if __name__ == "__main__":
    main()
