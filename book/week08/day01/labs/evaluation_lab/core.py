import hashlib
import json
import re
import unicodedata
from pathlib import Path
RUBRIC = {"version": "1.0", "answer": "all phrases with word boundaries", "json": "strict canonical equality", "tool": "strict name and arguments", "refusal": "strict decision and reason", "minimum": 0.8, "critical": "all pass"}
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(",", ":")).encode()).hexdigest()
def pairs(items):
    result = {}
    for key,value in items:
        if key in result: raise ValueError("duplicate JSON key")
        result[key] = value
    return result
def invalid_constant(value):
    raise ValueError("non-finite JSON number")
def read_rows(path):
    rows = [json.loads(line,object_pairs_hook=pairs,parse_constant=invalid_constant) for line in Path(path).read_text().splitlines() if line.strip()]
    if not rows: raise ValueError("empty file")
    ids = [row.get("id") for row in rows]
    if any(not isinstance(i,str) or not i.strip() for i in ids) or len(ids)!=len(set(ids)): raise ValueError("invalid or duplicate ids")
    return rows
def normalize(text):
    return " ".join(unicodedata.normalize("NFKC",text).casefold().split())
def score(case,output):
    expected = case["expected"]
    if case["kind"] == "answer":
        if not isinstance(output,str): return False
        text = normalize(output)
        return all(re.search(r"(?<!\w)"+re.escape(normalize(phrase))+r"(?!\w)",text) is not None for phrase in expected)
    return digest(output)==digest(expected)
def evaluate(dataset,predictions):
    for c in dataset:
        if c.get("kind") not in {"answer","json","tool","refusal"}: raise ValueError("unknown kind")
        if not isinstance(c.get("critical"),bool) or not isinstance(c.get("category"),str) or not c["category"].strip(): raise ValueError("invalid case metadata")
        if "expected" not in c: raise ValueError("missing expected")
        if c["kind"]=="answer" and (not isinstance(c["expected"],list) or not c["expected"] or any(not isinstance(p,str) or not p.strip() for p in c["expected"])): raise ValueError("invalid phrases")
        if c["kind"]!="answer" and not isinstance(c["expected"],dict): raise ValueError("expected object required")
    expected_ids={c["id"] for c in dataset}; outputs={p["id"]:p for p in predictions}
    if set(outputs)-expected_ids: raise ValueError("unknown prediction id")
    results=[]
    for c in dataset:
        p=outputs.get(c["id"]); present=p is not None and "output" in p
        results.append({"id":c["id"],"category":c["category"],"critical":c["critical"],"present":present,"passed":score(c,p["output"]) if present else False})
    segments={}
    for category in sorted({c["category"] for c in results}):
        group=[c for c in results if c["category"]==category]
        segments[category]={"passed":sum(c["passed"] for c in group),"total":len(group)}
        segments[category]["rate"]=segments[category]["passed"]/len(group)
    rate=sum(c["passed"] for c in results)/len(results)
    coverage=sum(c["present"] for c in results)/len(results)
    critical_ok=all(c["passed"] for c in results if c["critical"])
    return {"schema_version":1,"dataset_hash":digest(dataset),"predictions_hash":digest(predictions),"rubric_hash":digest(RUBRIC),"rubric":RUBRIC,"cases":results,"segments":segments,"rate":rate,"macro_rate":sum(s["rate"] for s in segments.values())/len(segments),"coverage":coverage,"critical_ok":critical_ok,"accepted":coverage==1 and critical_ok and rate>=RUBRIC["minimum"]}
def compare(a,b):
    if any(a[k]!=b[k] for k in ("dataset_hash","rubric_hash")): raise ValueError("incompatible evaluation protocol")
    left={c["id"]:c for c in a["cases"]};right={c["id"]:c for c in b["cases"]}
    if left.keys()!=right.keys(): raise ValueError("different cases")
    return {"delta":b["rate"]-a["rate"],"regressions":[i for i in left if left[i]["passed"] and not right[i]["passed"]],"improvements":[i for i in left if not left[i]["passed"] and right[i]["passed"]],"candidate_accepted":b["accepted"]}
