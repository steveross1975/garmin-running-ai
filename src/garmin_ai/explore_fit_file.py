"""Complete FIT structure explorer - finds ALL message types."""
from pathlib import Path

import fitparse

from .garmin_client import get_recent_fit_files


def explore_complete_structure(fit_path: Path) -> None:
    """Explore ALL message types and ALL fields."""
    print(f"\n🔍 FULL ANALYSIS: {fit_path.name}")
    print("-" * 60)
    
    fitfile = fitparse.FitFile(
        str(fit_path),
        data_processor=fitparse.StandardUnitsDataProcessor()
    )
    
    message_stats = {}
    
    # Find ALL message types
    for message_type in fitfile.get_messages():
        msg_name = message_type.name
        message_stats[msg_name] = message_stats.get(msg_name, 0) + 1
        
        # Sample first record of each type
        first_record = next(fitfile.get_messages(msg_name), None)
        if first_record:
            fields = [f.name for f in first_record]
            print(f"📋 {msg_name:15} ({message_stats[msg_name]} records)")
            print(f"   Fields: {len(fields)} {fields[:10]}{'...' if len(fields) > 10 else ''}")
            
            # Check for running data
            running_fields = [f for f in fields if any(x in f.lower() for x in 
                ['cadence', 'heart', 'vertical', 'ground', 'stance', 'step'])]
            if running_fields:
                print(f"   🏃 RUNNING DATA: {running_fields}")
    
    print(f"\n📊 SUMMARY: {len(message_stats)} message types found")


def explore_sample_records(fit_path: Path) -> None:
    """Sample first 20 records from each message type."""
    print(f"\n🔬 RAW RECORD SAMPLE: {fit_path.name}")
    
    fitfile = fitparse.FitFile(str(fit_path))
    
    for msg_type in ['record', 'lap', 'session', 'activity']:
        records = list(fitfile.get_messages(msg_type))[:3]
        if records:
            print(f"\n📄 {msg_type.upper()} ({len(records)} samples):")
            for i, record in enumerate(records, 1):
                fields = {f.name: f.value for f in record}
                print(f"   {i}: {fields}")


if __name__ == "__main__":
    fit_files = get_recent_fit_files(1)
    if fit_files:
        explore_complete_structure(fit_files[0])
        explore_sample_records(fit_files[0])
    else:
        print("❌ No FIT files")
