#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, os
from pathlib import Path
from typing import Iterable, NoReturn

EXPECTED_ROOTS = 28
CLAIM = "PROVENANCE_LOCATOR_RECEIPT_ONLY_NO_BUILD_ATTESTATION_OR_AUTHORITY_EFFECT"
FILES = ("build-invocation-record.json", "build-environment-record.json", "build-output-manifest.tsv")

def fail(msg: str) -> NoReturn:
    raise SystemExit(f"sup-02 provenance locator: FAIL: {msg}")

def read_tsv(path: Path) -> list[dict[str,str]]:
    if not path.is_file() or path.is_symlink(): fail(f"missing regular input: {path}")
    with path.open(encoding="utf-8", newline="") as f:
        r=csv.DictReader(f, delimiter="\t")
        if not r.fieldnames: fail(f"missing header: {path}")
        return [{k:(v or "") for k,v in row.items()} for row in r]

def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str,object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w=csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        w.writeheader(); [w.writerow({k:row.get(k,"") for k in fields}) for row in rows]

def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024), b""): h.update(b)
    return h.hexdigest()

def safe_json(path: Path) -> str:
    try:
        obj=json.loads(path.read_text(encoding="utf-8"))
    except Exception: return "INVALID_JSON"
    return "VALID_JSON_OBJECT" if isinstance(obj, dict) else "VALID_JSON_NONOBJECT"

def safe_tsv(path: Path) -> str:
    try:
        rows=read_tsv(path)
    except SystemExit:
        return "INVALID_TSV"
    return "VALID_TSV_WITH_ROWS" if rows else "VALID_TSV_HEADER_ONLY"

def load_json_state(path: Path|None, label: str) -> tuple[str,int,str]:
    if path is None: return "NOT_CAPTURED",0,"-"
    if not path.is_file() or path.is_symlink(): return "UNAVAILABLE",0,"-"
    try: obj=json.loads(path.read_text(encoding="utf-8"))
    except Exception: return "INVALID_JSON",0,sha(path)
    if isinstance(obj, dict):
        for key in ("workflows","workflow_runs","releases"):
            if isinstance(obj.get(key), list): return "CAPTURED",len(obj[key]),sha(path)
        return "CAPTURED",1,sha(path)
    if isinstance(obj, list): return "CAPTURED",len(obj),sha(path)
    return "CAPTURED",1,sha(path)

def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--root-request-set", required=True, type=Path)
    p.add_argument("--record-root", action="append", type=Path, default=[])
    p.add_argument("--github-repository-metadata", type=Path)
    p.add_argument("--github-workflows", type=Path)
    p.add_argument("--github-releases", type=Path)
    p.add_argument("--out", required=True, type=Path)
    a=p.parse_args()
    if a.out.exists() or a.out.is_symlink(): fail("refusing existing output")
    roots=read_tsv(a.root_request_set)
    if len(roots)!=EXPECTED_ROOTS: fail(f"root denominator drift: {len(roots)}")
    for r in roots:
        if "SUP-02" not in r.get("batch_ids","").split(";"): fail(f"SUP-02 missing from root: {r.get('root_review_id')}")
        if r.get("manifest_scope_kind")!="ROOT" or r.get("authority_state")!="OPEN_NO_ACCEPTANCE": fail("root scope/authority drift")
    a.out.mkdir(parents=True)
    record_roots=[]
    seen=set()
    for rr in a.record_root:
        key=str(rr)
        if key not in seen: seen.add(key); record_roots.append(rr)
    inv=[]; root_rows=[]; complete=partial=absent=0
    for row in roots:
        rid=row["root_review_id"]; unit=row["acquisition_unit_id"]; recipe=row["recipe_root"]
        found={name:[] for name in FILES}
        candidates=[]
        for rr in record_roots:
            candidates += [rr/rid, rr/unit.replace(":","__"), rr/recipe.replace("/","__")]
        unique=[]; us=set()
        for c in candidates:
            s=str(c)
            if s not in us: us.add(s); unique.append(c)
        for d in unique:
            if not d.exists(): continue
            if not d.is_dir() or d.is_symlink(): fail(f"unsafe record directory: {d}")
            for name in FILES:
                f=d/name
                if f.exists():
                    if not f.is_file() or f.is_symlink(): fail(f"unsafe record file: {f}")
                    if f.stat().st_size > 64*1024*1024: fail(f"oversize record file: {f}")
                    found[name].append(f)
        present=sum(1 for x in found.values() if x)
        state="COMPLETE_CUSTODIAN_EXPORT_FOUND" if present==3 else ("PARTIAL_CUSTODIAN_EXPORT_FOUND" if present else "NO_CUSTODIAN_EXPORT_FOUND")
        complete += state.startswith("COMPLETE"); partial += state.startswith("PARTIAL"); absent += state.startswith("NO_")
        for name, paths in found.items():
            for f in paths:
                validation=safe_tsv(f) if name.endswith(".tsv") else safe_json(f)
                inv.append({"root_review_id":rid,"acquisition_unit_id":unit,"recipe_root":recipe,"record_kind":name,"path":str(f),"sha256":sha(f),"size_bytes":f.stat().st_size,"validation_state":validation,"claim_boundary":CLAIM})
        root_rows.append({"acquisition_unit_id":unit,"root_review_id":rid,"recipe_root":recipe,"recipe_tree":row["recipe_tree"],"build_invocation_records":len(found[FILES[0]]),"build_environment_records":len(found[FILES[1]]),"build_output_manifests":len(found[FILES[2]]),"locator_state":state,"ba_001_state":"CANDIDATE_LOCATED_REVIEW_REQUIRED" if found[FILES[0]] else "OPEN_NO_RECORD_LOCATED","ba_002_state":"CANDIDATE_LOCATED_REVIEW_REQUIRED" if found[FILES[1]] else "OPEN_NO_RECORD_LOCATED","ba_003_state":"CANDIDATE_LOCATED_REVIEW_REQUIRED" if found[FILES[2]] else "OPEN_NO_RECORD_LOCATED","authority_state":"OPEN_NO_ACCEPTANCE","claim_boundary":CLAIM})
    repo_state,repo_count,repo_sha=load_json_state(a.github_repository_metadata,"repository")
    wf_state,wf_count,wf_sha=load_json_state(a.github_workflows,"workflows")
    rel_state,rel_count,rel_sha=load_json_state(a.github_releases,"releases")
    write_tsv(a.out/"sup-02-local-record-inventory.tsv", ["root_review_id","acquisition_unit_id","recipe_root","record_kind","path","sha256","size_bytes","validation_state","claim_boundary"], inv)
    write_tsv(a.out/"sup-02-root-provenance-locator.tsv", ["acquisition_unit_id","root_review_id","recipe_root","recipe_tree","build_invocation_records","build_environment_records","build_output_manifests","locator_state","ba_001_state","ba_002_state","ba_003_state","authority_state","claim_boundary"], root_rows)
    write_tsv(a.out/"sup-02-custodian-surface.tsv", ["surface","state","item_count","sha256","evidentiary_effect"], [
        {"surface":"github_repository_metadata","state":repo_state,"item_count":repo_count,"sha256":repo_sha,"evidentiary_effect":"LOCATOR_ONLY"},
        {"surface":"github_actions_workflows","state":wf_state,"item_count":wf_count,"sha256":wf_sha,"evidentiary_effect":"LOCATOR_ONLY_NOT_BUILD_PROVENANCE"},
        {"surface":"github_releases","state":rel_state,"item_count":rel_count,"sha256":rel_sha,"evidentiary_effect":"LOCATOR_ONLY_NOT_BUILD_PROVENANCE"},
    ])
    write_tsv(a.out/"summary.tsv", ["field","value"], [
        {"field":"root_rows","value":len(roots)}, {"field":"record_roots","value":len(record_roots)},
        {"field":"complete_custodian_exports","value":complete}, {"field":"partial_custodian_exports","value":partial}, {"field":"absent_custodian_exports","value":absent},
        {"field":"record_files_located","value":len(inv)}, {"field":"build_attestations_accepted","value":0}, {"field":"final_provider_decisions_accepted","value":0}, {"field":"target_rows_populated","value":0},
        {"field":"next_state","value":"REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_PROVENANCE_LOCATOR_RECEIPT"},
    ])
    (a.out/"analysis.status").write_text("PASS\n")
    (a.out/"claim-boundary.txt").write_text(CLAIM+"\n")
    (a.out/"next-state.txt").write_text("REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_PROVENANCE_LOCATOR_RECEIPT\n")
    print(f"SUP02_PROVENANCE_LOCATOR=PASS roots={len(roots)} complete={complete} partial={partial} absent={absent} files={len(inv)}")
if __name__=="__main__": main()
