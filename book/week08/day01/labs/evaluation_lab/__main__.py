import argparse
import json
from pathlib import Path
from .core import evaluate, read_rows

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--dataset",required=True);parser.add_argument("--predictions",required=True);parser.add_argument("--output",required=True)
    args=parser.parse_args()
    try: report=evaluate(read_rows(args.dataset),read_rows(args.predictions))
    except (ValueError,KeyError,TypeError,OSError) as exc:
        print("Invalid evaluation input:",type(exc).__name__);return 2
    target=Path(args.output);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({k:report[k] for k in ("rate","coverage","critical_ok","accepted")}))
    return 0 if report["accepted"] else 1
if __name__=="__main__": raise SystemExit(main())
