#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import zipapp
from pathlib import Path
from datetime import datetime

# 1. Setup paths and import version
src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from dworshak_prompt._version import __version__

PROJECT_NAME = "dworshak-prompt"
ENTRY_POINT = "dworshak_prompt.__main__:run"
DIST_DIR = Path("dist") / "zipapp"
# Create a single temporary work directory
STAGING_DIR = Path("staging_tmp")

def run_build():
    print(f"--- PYZ Build: {PROJECT_NAME} v{__version__} ---")

    try:
        # Clean and create directories
        if STAGING_DIR.exists():
            shutil.rmtree(STAGING_DIR)
        DIST_DIR.mkdir(parents=True, exist_ok=True)

        # 2. Build the Wheel
        subprocess.run(["uv", "build", 
                        "--wheel", "--sdist", 
                        "--out-dir", str(DIST_DIR),
                        ],
                        check=True)

        # 3. Find and Stage
        wheel = next(DIST_DIR.glob(f"dworshak_prompt-{__version__}-*.whl"))
        subprocess.run([
            "uv", "pip", "install", str(wheel),
            "--target", str(STAGING_DIR), "--no-deps"
        ], check=True)

        # 4. Identity Stamp (Best Practice)
        # Allows the app to know it's in "portable mode"
        (STAGING_DIR / "dworshak_prompt" / "PYZ_BUILD").write_text(
            f"version={__version__}\nbuild_date={datetime.now().isoformat()}"
        )

        # 5. Build Compressed PYZ using the API (More control than CLI)
        output_pyz = DIST_DIR / f"{PROJECT_NAME}-v{__version__}.pyz"
        
        # Using the zipapp API allows for better integration in build scripts
        zipapp.create_archive(
            source=STAGING_DIR,
            target=output_pyz,
            interpreter="/usr/bin/env python3",
            main=ENTRY_POINT,
            compressed=True
        )

        # 6. Cleanup and Report
        output_pyz.chmod(0o755)
        #wheel.unlink() <-- suppressed so it stays for the GitHub Release
        size_kb = output_pyz.stat().st_size / 1024
        print(f"\n✅ Build Successful!")
        print(f"Artifact: {output_pyz.name}")
        print(f"Size:     {size_kb:.2f} KB")

    finally:
        # This runs even if the build crashes
        if STAGING_DIR.exists():
            shutil.rmtree(STAGING_DIR)
        if Path("build").exists():
            shutil.rmtree(Path("build"))

if __name__ == "__main__":
    run_build()