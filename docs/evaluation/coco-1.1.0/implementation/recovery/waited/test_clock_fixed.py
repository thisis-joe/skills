"""Real two-process pacing check, no native model calls."""
import importlib.util,json,subprocess,sys,tempfile,unittest
from datetime import datetime
from pathlib import Path
HERE=Path(__file__).resolve().parent
CHILD="""import importlib.util,json,sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('clock_fixed',sys.argv[1])
run=importlib.util.module_from_spec(spec);spec.loader.exec_module(run)
print(json.dumps(run.await_admission(Path(sys.argv[2]),lambda:False)))
"""
class CrossProcessClock(unittest.TestCase):
    def test_real_processes_keep_thirty_second_start_gap(self):
        with tempfile.TemporaryDirectory() as directory:
            command=[sys.executable,'-c',CHILD,str(HERE/'clock_fixed_run.py'),directory]
            first=json.loads(subprocess.check_output(command,text=True))
            second=json.loads(subprocess.check_output(command,text=True))
            gap=(datetime.fromisoformat(second['utc'])-datetime.fromisoformat(first['utc'])).total_seconds()
            print(json.dumps({'first':first,'second':second,'actual_gap_seconds':gap}),flush=True)
            self.assertGreaterEqual(gap,30)
            self.assertLess(gap,35)
            self.assertGreater(second['requested_wait_seconds'],29)
if __name__=='__main__':unittest.main()
