#!/usr/bin/env python3
"""Exact arithmetic checks for the non-all-positive cost-difference theorem."""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations, product
import json
from pathlib import Path

N=4
ARCS=range(5)
SUPPORTS=(
 frozenset({0,1,2}),
 frozenset({0,1,2,3,4}),
 frozenset({1,2,3,4}),
 frozenset({2,3}),
)
CHAIN_MISSING={1,2,3}  # zero-based missing terminals 2,3,4 in paper labels
NESTED_MISSING={0}

def feasible(mask,k,p):
 return sum((k[i]*((1 if mask>>i&1 else 0)-p[i]) for i in range(N)),Q(0))>=0

def route_deviations(mask,d,p):
 vals=[]
 for a in ARCS:
  vals.append(sum((d[i]*((1 if mask>>i&1 else 0)-p[i]) for i in range(N) if a in SUPPORTS[i]),Q(0)))
 for i in range(N):
  vals.append(d[i]*((1-p[i]) if mask>>i&1 else p[i]))
 return vals

def route_max(mask,d,p):return max(route_deviations(mask,d,p))

def chain_lower(missing,eps):
 P=[i for i in range(N) if i!=missing]
 # middle index in each chain type
 middle={1:2,2:1,3:1}[missing] # missing t2->t3; missing t3/t4->t2
 outer=[i for i in P if i!=middle]
 k=[Q(1)]*N
 k[missing]=Q(-3)
 p=[Q(0)]*N
 p[outer[0]]=p[outer[1]]=(1+eps)/4
 p[middle]=(1+eps)/2
 p[missing]=Q(0)
 d=[Q(1)]*N
 d[middle]=(3-eps)/4
 d[missing]=Q(1,7)
 F=[m for m in range(16) if feasible(m,tuple(k),tuple(p))]
 assert all(not (m>>missing&1) for m in F)
 assert {sum(1 for i in P if m>>i&1) for m in F}=={2,3}
 optimum=min(route_max(m,tuple(d),tuple(p)) for m in F)
 expected=(3-eps)**2/8
 assert optimum==expected,(missing,optimum,expected,F)
 return {'missing_terminal':missing+1,'optimum':str(optimum),'expected':str(expected),'feasible_routes':F}

def zero_chain_lower(missing,eps,eta):
 P=[i for i in range(N) if i!=missing]
 middle={1:2,2:1,3:1}[missing]
 outer=[i for i in P if i!=middle]
 k=[Q(1)]*N;k[missing]=Q(0)
 p=[Q(0)]*N
 p[outer[0]]=p[outer[1]]=(1+eps)/4;p[middle]=(1+eps)/2;p[missing]=Q(1,2)
 d=[Q(1)]*N;d[middle]=(3-eps)/4;d[missing]=eta
 F=[m for m in range(16) if feasible(m,tuple(k),tuple(p))]
 opt=min(route_max(m,tuple(d),tuple(p)) for m in F)
 base=(3-eps)**2/8
 assert opt>=base-eta
 return {'missing_terminal':missing+1,'optimum':str(opt),'base_minus_eta':str(base-eta)}

def verify_chain_identity():
 # Exact grid check of the one-variable bound V(p)=1+p/2-p^2/2 <= 9/8.
 for numerator in range(1001):
  p=Q(numerator,1000)
  value=1+p/2-p*p/2
  assert value<=Q(9,8)
  assert Q(9,8)-value==(p-Q(1,2))**2/2

def verify_nested_identity():
 # For pA+pB+pC=1, qB*T_AC+pB*T_BC has coefficient pC on dA,
 # zero on dB, and qC on dC, hence <=1. Check exact coefficients.
 for a in range(21):
  for b in range(21-a):
   pA=Q(a,20);pB=Q(b,20);pC=1-pA-pB
   qA=1-pA;qB=1-pB;qC=1-pC
   coeffA=qB*qA-pB*pA
   coeffB=qB*(-pB)+pB*qB
   coeffC=(qB+pB)*qC
   assert coeffA==pC
   assert coeffB==0
   assert coeffC==qC
   assert coeffA+coeffC==1

def verify_two_pair_scalar_lemma():
 # Exhaustive small rational search for the contradiction pattern. This is a
 # regression check for the human algebra, not its proof.
 vals=[Q(i,8) for i in range(9)]
 checked=0
 for pA in vals:
  for pB in vals:
   for pC in vals:
    for wA in (Q(1),Q(2),Q(3)):
     for wB in (Q(1),Q(2),Q(3)):
      for wC in (Q(1),Q(2),Q(3)):
       tau=wA*pA+wB*pB+wC*pC
       # AB and AC feasible, all singletons and BC infeasible.
       if not (wA+wB>=tau and wA+wC>=tau):continue
       if not (wA<tau and wB<tau and wC<tau and wB+wC<tau):continue
       checked+=1
       assert pA+pB>=1 or pA+pC>=1
 assert checked>0
 return checked


def verify_value_one_lower_strata(eps):
 patterns=0
 for signs in product((-1,0,1),repeat=4):
  if signs in ((0,0,0,0),(1,1,1,1)):continue
  positive=[i for i,s in enumerate(signs) if s>0]
  nonpositive=[i for i,s in enumerate(signs) if s<=0]
  chain=len(positive)==3 and nonpositive[0] in CHAIN_MISSING
  if chain:continue
  nonzero=[i for i,s in enumerate(signs) if s]
  j=nonzero[0]
  k=tuple(Q(s) for s in signs)
  # Unique oriented generator equal to all nonzero coordinates.
  p=[]
  for i,s in enumerate(signs):
   if s==0:p.append(Q(1,2))
   else:
    q=eps if i==j else Q(1)
    p.append(q if s>0 else 1-q)
  p=tuple(p)
  F=[m for m in range(16) if feasible(m,k,p)]
  assert F
  for m in F:
   oriented_j=bool(m&(1<<j)) if signs[j]>0 else not bool(m&(1<<j))
   assert oriented_j
  d=tuple(Q(1) if i==j else Q(1,7) for i in range(4))
  assert min(route_max(m,d,p) for m in F)>=1-eps
  patterns+=1
 assert patterns==73
 return patterns

def main():
 verify_chain_identity();verify_nested_identity();checked=verify_two_pair_scalar_lemma()
 eps=Q(1,1000)
 value_one_patterns=verify_value_one_lower_strata(eps)
 chain=[chain_lower(m,eps) for m in sorted(CHAIN_MISSING)]
 zero=[zero_chain_lower(m,eps,Q(1,10000)) for m in sorted(CHAIN_MISSING)]
 # 9/8 is strictly below the all-positive value L: 263 > 41 sqrt(41).
 assert 263*263>41**3
 out={
  'status':'PASS',
  'chain_missing_terminals':[2,3,4],
  'nested_missing_terminal':1,
  'value_one_sign_zero_strata':value_one_patterns,
  'chain_sign_zero_strata':6,
  'chain_lower_witnesses':chain,
  'zero_boundary_lower_witnesses':zero,
  'two_pair_grid_instances_checked':checked,
  'exact_chain_supremum':'9/8',
  'exact_nested_supremum':'1',
  'comparison_to_L':'9/8 < (299-41*sqrt(41))/32',
  'nonclaims':['human inequalities remain the proof','all-positive 83-cell frontier remains open','all-zero cost vector not assigned a separate exact value'],
 }
 target=Path(__file__).with_name('nonpositive_difference_results.json')
 target.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print('PASS: chain all-pairs formula has exact supremum 9/8')
 print('PASS: nested all-pairs convex combination is at most 1')
 print('PASS: two-pair scalar lemma checked on',checked,'exact rational instances')
 print('PASS: exact negative and zero missing-terminal lower sequences check')
 print('PASS: exact value-one lower sequences check on all 73 remaining strata')
 print('PASS: every non-all-positive nonzero/zero stratum reduces to these cases')
 print('WROTE:',target)
if __name__=='__main__':main()
