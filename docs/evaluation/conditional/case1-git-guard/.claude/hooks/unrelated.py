from pathlib import Path
import os
Path(os.environ["CLAUDE_PROJECT_DIR"], "other-hook-ran").write_text("ran\n")
