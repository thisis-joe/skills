# Existing documented read-only inventory command; inspect for spec, do not execute workflow.
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--since',required=True);p.add_argument('--until',required=True);a=p.parse_args()
print(json.dumps([str(f) for f in sorted(Path('notes').glob('*.md')) if a.since<=f.name[:10]<=a.until]))
