"""Local FIT file handler - Handles ZIP exports + FIT files."""
import zipfile
from pathlib import Path
from typing import List

import fitparse
from config import FIT_DIR, is_pipeline_mode


def unzip_garmin_exports() -> List[Path]:
    """
    Automatically unzip Garmin Connect ZIP exports to extract FIT files.
    """
    unzipped_files = []
    
    # Look for ZIP files
    zip_files = list(FIT_DIR.glob("*.zip"))
    
    for zip_path in zip_files:
        print(f"📦 Unzipping {zip_path.name}...")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(FIT_DIR)
            print(f"   ✅ Extracted to {FIT_DIR}")
            
            # Find extracted FIT files
            extracted_fits = list(FIT_DIR.glob(f"{zip_path.stem}*.fit"))
            unzipped_files.extend(extracted_fits)
            print(f"   📁 Found {len(extracted_fits)} FIT files")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return unzipped_files


def get_local_fit_files() -> List[Path]:
    """
    Get all valid FIT files (handles ZIP auto-extraction).
    """
    # First, unzip any ZIP files
    unzip_garmin_exports()
    
    # Then find all FIT files
    fit_files = list(FIT_DIR.glob("*.fit"))
    
    if not fit_files:
        print("❌ No .fit files found in data/fit/")
        print("💡 Steps:")
        print("   1. Garmin Connect → Activities → Export Original")
        print("   2. Copy .zip file to data/fit/")
        print("   3. This script auto-unzips → extracts FIT")
        return []
    
    print(f"📁 Found {len(fit_files)} FIT files:")
    valid_files = []
    
    for fit_file in fit_files:
        try:
            fitparse.FitFile(str(fit_file), data_processor=fitparse.StandardUnitsDataProcessor())
            valid_files.append(fit_file)
            print(f"   ✅ {fit_file.name}")
        except Exception as e:
            print(f"   ❌ {fit_file.name}: {e}")
    
    print(f"\n🎉 {len(valid_files)} valid FIT files ready")
    return valid_files


def get_recent_fit_files(n_recent: int = 5, by_modified: bool = True) -> List[Path]:
    """
    Get N most recent FIT files (auto-unzips ZIPs first).
    """
    all_files = get_local_fit_files()
    if not all_files:
        return []
    
    if by_modified:
        sorted_files = sorted(all_files, key=lambda f: f.stat().st_mtime, reverse=True)
    else:
        sorted_files = sorted(all_files, key=lambda f: f.name, reverse=True)
    
    recent = sorted_files[:n_recent]
    print(f"\n📋 Most recent {len(recent)}:")
    for i, f in enumerate(recent, 1):
        print(f"   {i}. {f.name}")
    
    return recent


if __name__ == "__main__":
    """Test local FIT handler with ZIP support."""
    if is_pipeline_mode():
        print("🚫 Use pipeline.py instead")
    exit(1)
    print("🚀 Garmin Running AI - Local FIT Handler (ZIP + FIT)")
    print("=" * 50)
    
    recent = get_recent_fit_files(n_recent=3)
    print(f"\n✅ Ready! Found {len(recent)} recent FIT files")
