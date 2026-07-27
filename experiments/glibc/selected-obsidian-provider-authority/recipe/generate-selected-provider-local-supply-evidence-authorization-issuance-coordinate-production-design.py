#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib
from pathlib import Path
SOURCE_DIGESTS={'selected-provider-local-supply-evidence-authorization-coordinate-contract-boundary-acceptance.tsv': '460a0e5133600a58467b5e736005700d835499476b4e19de147bd08d0507df8c', 'selected-provider-local-supply-evidence-owner-authorization-token-schema.json': '27d11e8bb8de3238b49aef77757f0328a2269a156f55fdcbdddcf4dcb4fd411b', 'selected-provider-local-supply-evidence-coordinate-receipt-schema.json': 'b94c25994ecc26e402607b9e61c0cee796c74b15435bc168a18821def9096f83', 'selected-provider-local-supply-evidence-authorization-coordinate-validation-contract.tsv': '64a6c168e30c7a559387c27d6baa7d3bd49953d7ea304d1bd98e4043cbb57f56'}
ARTIFACTS=['experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-input-contract.tsv', 'experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-state-machine.tsv', 'experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-operation-contract.tsv', 'experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-failure-contract.tsv', 'experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-receipt-contract.json', 'experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-evidence-authorization-issuance-coordinate-production-design-metadata.tsv']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path('.'));ap.add_argument('--output-root',type=Path,default=Path('.'));a=ap.parse_args();rr=a.repo_root.resolve();oo=a.output_root.resolve()
 src=rr/'experiments/glibc/selected-obsidian-provider-authority/review'
 for n,d in SOURCE_DIGESTS.items():
  if sha(src/n)!=d: raise SystemExit('source digest mismatch: '+n)
 for rel in ARTIFACTS:
  s=rr/rel;d=oo/rel;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(s.read_bytes())
if __name__=='__main__':main()
