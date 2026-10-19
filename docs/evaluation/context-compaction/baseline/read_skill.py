import json
from pathlib import Path
import sys
root = Path(__file__).resolve().parent
skills = (root / 'skills').resolve()
target = (skills / sys.argv[1]).resolve()
target.relative_to(skills)
text = target.read_text()
with (root / 'reads.jsonl').open('a') as log:
    log.write(json.dumps({'path': str(target.relative_to(skills)), 'characters': len(text)}) + '\n')
print(text, end='')
