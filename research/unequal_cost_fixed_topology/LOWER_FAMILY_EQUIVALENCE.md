# Equivalence of the Local and Released Lower Families

The follow-on theorem is self-contained and uses the local definition in
`lower_family.py` and `EVERY_PAIR_CELL_THEOREM.md`.

`RELEASE_FAMILY_PIN.json` records the extraction from immutable release
`v0.1.0`, commit
`087204eda4cc490cb59dd1988d7383c406288d2e`, file
`paper/ssuf_four_terminal_note_v5.tex`, Git blob
`b28b334395f89aa9424cb875a3739b2ba7c9b840`, and TeX SHA-256
`3b9c5963ad2da2cbaa99621202e5b50ad3c2525f2bb5f6fdf7f649568c3e1154`.

## Equivalence lemma

The local and pinned definitions have identical:

- parameter domains;
- demand vector \((1,q^2,q,1)\);
- cheap-fraction vector;
- equal positive route-cost differences;
- sum \(1+\varepsilon\);
- witness function \(R(q,\varepsilon)\);
- limiting function;
- maximizing \(q_*\); and
- limiting value \(L\).

Thus they define the same parametric family componentwise.

`release_family_equivalence_check.py` compares the local machine-readable object
with the pinned extraction and checks that the theorem still contains the
corresponding formulas. The copied-directory replay contains no `paper/`
directory and does not read the release at runtime.

## Residual limitation

The extraction from the pinned TeX into `RELEASE_FAMILY_PIN.json` is
human-auditable, not automatically reparsed from TeX during replay. The release
hash makes drift detectable but does not itself prove the extraction was
transcribed correctly.
