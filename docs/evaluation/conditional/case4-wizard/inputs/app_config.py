import importlib.util
from pathlib import Path
p=Path(__file__).parents[1]/"helpers/env_store.py"
s=importlib.util.spec_from_file_location("env_store",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def load_env(path): return m.read(Path(path))
