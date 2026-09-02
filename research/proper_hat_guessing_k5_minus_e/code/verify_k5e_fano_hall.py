#!/usr/bin/env python3
"""Dependency-free verifier/constructor for HG_P(K5-e) >= 8.

Colors are the vectors of F_2^3, encoded by integers 0..7; vector addition is
bitwise XOR. Vertices 0 and 1 are the nonadjacent twins, and 2,3,4 form the
clique.

The compact certificate supplies delta(U) for each 2-dimensional subspace U,
indexed by its unique nonzero normal n under the standard dot product. The
verifier checks the seven small permutations used in the Hall argument, builds
the residual incidence graph, constructs a deterministic left-saturating
matching, recovers a complete strategy, and checks all 8,400 proper colorings.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, deque
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

Q = 8
N_VERTICES = 5
EDGES = tuple(
    (u, v)
    for u in range(N_VERTICES)
    for v in range(u + 1, N_VERTICES)
    if (u, v) != (0, 1)
)
NEIGHBORS = tuple(
    tuple(w for w in range(N_VERTICES) if w != v and (min(v, w), max(v, w)) in EDGES)
    for v in range(N_VERTICES)
)

Coloring = Tuple[int, int, int, int, int]
ViewKey = Tuple[int, Tuple[int, ...]]


def dot(x: int, y: int) -> int:
    return (x & y).bit_count() & 1


def normal_of_plane(u: int, v: int) -> int:
    """Unique nonzero normal to span(u,v), where u,v are independent."""
    if u == 0 or v == 0 or u == v:
        raise ValueError(f"dependent plane generators {(u, v)}")
    normals = [n for n in range(1, Q) if dot(n, u) == 0 and dot(n, v) == 0]
    if len(normals) != 1:
        raise AssertionError((u, v, normals))
    return normals[0]


def proper_colorings() -> List[Coloring]:
    out: List[Coloring] = []
    for triple in itertools.permutations(range(Q), 3):
        remaining = [x for x in range(Q) if x not in triple]
        for a in remaining:
            for b in remaining:
                out.append((a, b, triple[0], triple[1], triple[2]))
    if len(out) != 8400:
        raise AssertionError(len(out))
    return out


def parse_delta(path: Path) -> Tuple[bytes, Dict[int, int]]:
    raw = path.read_bytes()
    obj = json.loads(raw)
    rows = obj.get("delta_by_normal")
    if not isinstance(rows, list):
        raise SystemExit("certificate lacks delta_by_normal list")
    delta: Dict[int, int] = {}
    for row in rows:
        n, d = int(row["normal"]), int(row["delta"])
        if n in delta:
            raise SystemExit(f"duplicate normal {n}")
        delta[n] = d
    if set(delta) != set(range(1, Q)):
        raise SystemExit(f"normal domain mismatch: {sorted(delta)}")
    return raw, delta


def phi(delta: Dict[int, int], w: int, r: int) -> int:
    return w ^ r ^ delta[normal_of_plane(w, r)]


def cycle_decomposition(domain: Iterable[int], mapping: Dict[int, int]) -> List[List[int]]:
    unseen = set(domain)
    cycles: List[List[int]] = []
    while unseen:
        start = min(unseen)
        cyc: List[int] = []
        x = start
        while x not in cyc:
            if x not in mapping:
                raise AssertionError(f"mapping leaves domain at {x}")
            cyc.append(x)
            unseen.discard(x)
            x = mapping[x]
        if x != start:
            raise AssertionError(f"not a permutation cycle from {start}: {cyc} -> {x}")
        cycles.append(cyc)
    return cycles


def hopcroft_karp(adjacency: List[List[int]], n_right: int) -> Tuple[List[int], List[int]]:
    n_left = len(adjacency)
    pair_left = [-1] * n_left
    pair_right = [-1] * n_right
    dist = [0] * n_left
    inf = n_left + 1

    def bfs() -> bool:
        q: deque[int] = deque()
        found = False
        for u in range(n_left):
            if pair_left[u] == -1:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = inf
        while q:
            u = q.popleft()
            for v in adjacency[u]:
                mate = pair_right[v]
                if mate == -1:
                    found = True
                elif dist[mate] == inf:
                    dist[mate] = dist[u] + 1
                    q.append(mate)
        return found

    def dfs(u: int) -> bool:
        for v in adjacency[u]:
            mate = pair_right[v]
            if mate == -1 or (dist[mate] == dist[u] + 1 and dfs(mate)):
                pair_left[u] = v
                pair_right[v] = u
                return True
        dist[u] = inf
        return False

    while bfs():
        for u in range(n_left):
            if pair_left[u] == -1:
                dfs(u)
    return pair_left, pair_right


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("certificate", type=Path)
    ap.add_argument("--strategy-output", type=Path)
    ap.add_argument("--matching-output", type=Path)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()

    raw, delta = parse_delta(args.certificate)
    errors: List[str] = []

    for n, d in sorted(delta.items()):
        if not (1 <= d < Q):
            errors.append(f"delta[{n}]={d} is not nonzero")
        if dot(n, d) != 1:
            errors.append(f"delta[{n}]={d} lies in U_{n}")

    phi_cycles: Dict[str, List[List[int]]] = {}
    for w in range(1, Q):
        domain = [r for r in range(1, Q) if r != w]
        mapping = {r: phi(delta, w, r) for r in domain}
        if set(mapping.values()) != set(domain):
            errors.append(f"phi_{w} is not a permutation: {mapping}")
            continue
        if any(mapping[r] == r for r in domain):
            errors.append(f"phi_{w} has a fixed point")
        phi_cycles[str(w)] = cycle_decomposition(domain, mapping)

    cols = proper_colorings()

    twin_strategy: Dict[ViewKey, int] = {}
    for T in itertools.permutations(range(Q), 3):
        sigma = T[0] ^ T[1] ^ T[2]
        n = normal_of_plane(T[0] ^ T[1], T[0] ^ T[2])
        alpha = sigma
        beta = sigma ^ delta[n]
        if alpha in T or beta in T:
            errors.append(f"illegal twin guess on {T}: {(alpha, beta)}")
        twin_strategy[(0, T)] = alpha
        twin_strategy[(1, T)] = beta

    residual: List[Coloring] = []
    twin_covered = 0
    for c in cols:
        T = (c[2], c[3], c[4])
        hit = twin_strategy[(0, T)] == c[0] or twin_strategy[(1, T)] == c[1]
        if hit:
            twin_covered += 1
        else:
            residual.append(c)

    right_id: Dict[ViewKey, int] = {}
    right_keys: List[ViewKey] = []
    adjacency: List[List[int]] = []
    for c in residual:
        row: List[int] = []
        for v in (2, 3, 4):
            key = (v, tuple(c[w] for w in NEIGHBORS[v]))
            if key not in right_id:
                right_id[key] = len(right_keys)
                right_keys.append(key)
            row.append(right_id[key])
        adjacency.append(row)

    right_degree = [0] * len(right_keys)
    for row in adjacency:
        for v in row:
            right_degree[v] += 1
    left_degree_hist = Counter(map(len, adjacency))
    right_degree_hist = Counter(right_degree)
    max_right_degree = max(right_degree, default=0)

    if left_degree_hist != Counter({3: len(residual)}):
        errors.append(f"unexpected left degrees {dict(left_degree_hist)}")
    if max_right_degree > 3:
        errors.append(f"right degree bound failed: max={max_right_degree}")

    pair_left, _ = hopcroft_karp(adjacency, len(right_keys))
    matching_size = sum(v != -1 for v in pair_left)
    if matching_size != len(residual):
        errors.append(f"matching does not saturate residual side: {matching_size}/{len(residual)}")

    clique_strategy: Dict[ViewKey, int] = {}
    matching_rows = []
    for li, rid in enumerate(pair_left):
        if rid == -1:
            continue
        c = residual[li]
        v, view = right_keys[rid]
        guess = c[v]
        if guess in view:
            errors.append(f"matched illegal clique guess {(v, view, guess)}")
        clique_strategy[(v, view)] = guess
        matching_rows.append({"coloring": list(c), "vertex": v})

    attainable_clique = {
        (v, tuple(c[w] for w in NEIGHBORS[v]))
        for c in cols
        for v in (2, 3, 4)
    }
    for key in sorted(attainable_clique):
        if key not in clique_strategy:
            clique_strategy[key] = next(g for g in range(Q) if g not in key[1])

    strategy = {**twin_strategy, **clique_strategy}
    hist: Counter[int] = Counter()
    uncovered: List[Coloring] = []
    for c in cols:
        hits = sum(
            strategy[(v, tuple(c[w] for w in NEIGHBORS[v]))] == c[v]
            for v in range(N_VERTICES)
        )
        hist[hits] += 1
        if hits == 0:
            uncovered.append(c)
    if uncovered:
        errors.append(f"complete strategy leaves {len(uncovered)} colorings uncovered")

    strategy_obj = {
        "format": "proper-hat-strategy-v1",
        "graph": "K5-e",
        "q": Q,
        "vertices": list(range(N_VERTICES)),
        "edges": [list(e) for e in EDGES],
        "neighbor_order": [list(x) for x in NEIGHBORS],
        "strategy": [
            {"vertex": v, "view": list(view), "guess": guess}
            for (v, view), guess in sorted(strategy.items())
        ],
    }
    strategy_text = json.dumps(strategy_obj, indent=2, sort_keys=True) + "\n"
    strategy_sha = hashlib.sha256(strategy_text.encode()).hexdigest()
    if args.strategy_output:
        args.strategy_output.parent.mkdir(parents=True, exist_ok=True)
        args.strategy_output.write_text(strategy_text)

    matching_obj = {
        "format": "K5-e-q8-residual-matching-v1",
        "residual_matching": matching_rows,
    }
    matching_text = json.dumps(matching_obj, indent=2, sort_keys=True) + "\n"
    matching_sha = hashlib.sha256(matching_text.encode()).hexdigest()
    if args.matching_output:
        args.matching_output.parent.mkdir(parents=True, exist_ok=True)
        args.matching_output.write_text(matching_text)

    report = {
        "format": "K5-e-q8-Fano-Hall-verification-v1",
        "claim": "HG_P(K5-e)>=8",
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "delta_by_normal": {str(k): v for k, v in sorted(delta.items())},
        "phi_cycles": phi_cycles,
        "proper_colorings_checked": len(cols),
        "twin_covered": twin_covered,
        "residual_colorings": len(residual),
        "left_degree_histogram": {str(k): v for k, v in sorted(left_degree_hist.items())},
        "right_views_in_residual_graph": len(right_keys),
        "right_degree_histogram": {str(k): v for k, v in sorted(right_degree_hist.items())},
        "maximum_right_degree": max_right_degree,
        "hall_degree_criterion_verified": max_right_degree <= 3,
        "matching_size": matching_size,
        "strategy_entries": len(strategy),
        "strategy_sha256": strategy_sha,
        "matching_certificate_sha256": matching_sha,
        "correct_guess_histogram": {str(k): v for k, v in sorted(hist.items())},
        "verified": not errors,
        "errors": errors[:25],
    }
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
