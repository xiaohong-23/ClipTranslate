"""Build script for ClipTranslate.

This script handles the PyInstaller build for Conda environments, where several
system DLLs are not picked up automatically. It also copies the resource
folder to the correct location inside the bundled app.
"""

import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.resolve()
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"
RESOURCE_DIR = PROJECT_ROOT / "resource"

# DLLs required when bundling from a Conda environment.
CONDA_DLLS = [
    "tcl86t.dll",
    "tk86t.dll",
    "ffi.dll",
    "liblzma.dll",
    "libbz2.dll",
    "zlib.dll",
]


def _get_conda_bin_dir() -> Path:
    """Return the Conda Library/bin directory for the active Python."""
    prefix = Path(sys.prefix)
    conda_bin = prefix / "Library" / "bin"
    if not conda_bin.is_dir():
        raise RuntimeError(
            f"Could not find Conda bin directory: {conda_bin}\n"
            "This script is intended for Conda environments."
        )
    return conda_bin


def _collect_add_binary_args(conda_bin: Path) -> list[str]:
    """Build --add-binary arguments for required Conda DLLs."""
    args: list[str] = []
    for dll_name in CONDA_DLLS:
        dll_path = conda_bin / dll_name
        if not dll_path.exists():
            raise RuntimeError(f"Required DLL not found: {dll_path}")
        # Destination '.' puts the DLL next to the executable inside _internal.
        args.extend(["--add-binary", f"{dll_path};."])
    return args


def _clean_build_artifacts() -> None:
    """Remove previous build/dist directories to avoid permission conflicts."""
    for directory in (BUILD_DIR, DIST_DIR):
        if directory.exists():
            shutil.rmtree(directory, ignore_errors=True)


def _copy_resources_to_bundle() -> None:
    """Copy the resource folder to the bundled _internal/resource location."""
    bundle_resource = DIST_DIR / "ClipTranslate" / "_internal" / "resource"
    if bundle_resource.exists():
        shutil.rmtree(bundle_resource, ignore_errors=True)
    shutil.copytree(RESOURCE_DIR, bundle_resource)


def main() -> int:
    """Run the PyInstaller build and copy resources."""
    conda_bin = _get_conda_bin_dir()
    add_binary_args = _collect_add_binary_args(conda_bin)

    _clean_build_artifacts()

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--windowed",
        "--icon",
        str(RESOURCE_DIR / "logo.ico"),
        "--noconsole",
        *add_binary_args,
        str(PROJECT_ROOT / "ClipTranslate.py"),
    ]

    print("Running:")
    print(" ".join(cmd))
    result = subprocess.run(cmd, cwd=PROJECT_ROOT, check=False)
    if result.returncode != 0:
        print("PyInstaller build failed.", file=sys.stderr)
        return result.returncode

    _copy_resources_to_bundle()

    print("\nBuild complete!")
    print(f"Output: {DIST_DIR / 'ClipTranslate'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
