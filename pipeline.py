"""
Unified Pipeline Orchestrator - Run all phases with a single command.

This script automatically executes:
  Phase 1: Data Ingestion (FIT → CSV → Activities Summary)
  Phase 2: Data Analysis (Form Analysis → Target Profiles → Synthetic Data)
  Phase 3: Machine Learning (Train models on synthetic data)
  Phase 4: Generative AI (Generate personalized tips)

Usage:
    python pipeline.py                          # Run all phases
    python pipeline.py --phase 1                # Run only Phase 1
    python pipeline.py --phase 2                # Run only Phase 2
    python pipeline.py --phase 3                # Run only Phase 3
    python pipeline.py --phase 4                # Run only Phase 4
    python pipeline.py --phase 1,2              # Run phases 1 and 2
    python pipeline.py --skip-phase 3           # Run all except phase 3
"""

import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime
import json

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.garmin_ai.config import DATA_DIR, MODELS_DIR, SYNTHETIC_DIR
from src.garmin_ai import (
    garmin_client,
    fit_converter,
    activities_analyzer,
    form_analyzer,
    target_profiles,
    synthetic_data_generator,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(DATA_DIR / 'pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PipelineOrchestrator:
    """Orchestrates the complete AI pipeline."""
    
    def __init__(self, phases=None, skip_phases=None, dry_run=False):
        """
        Initialize orchestrator.
        
        Args:
            phases: List of phases to run (1, 2, 3, 4) or None for all
            skip_phases: List of phases to skip
            dry_run: If True, print plan without executing
        """
        self.all_phases = [1, 2, 3, 4]
        self.phases = phases or self.all_phases
        self.skip_phases = skip_phases or []
        self.phases = [p for p in self.phases if p not in self.skip_phases]
        self.dry_run = dry_run
        self.results = {}
        self.start_time = datetime.now()
        
    def log_section(self, phase, status="START"):
        """Log phase header."""
        symbol = "▶" if status == "START" else "✅" if status == "COMPLETE" else "❌"
        print(f"\n{symbol} {'=' * 80}")
        print(f"{symbol} PHASE {phase}: {self._get_phase_name(phase)} [{status}]")
        print(f"{symbol} {'=' * 80}\n")
        
    def _get_phase_name(self, phase):
        """Get phase name."""
        names = {
            1: "Data Ingestion & Foundation",
            2: "Data Analysis & Baselines",
            3: "Machine Learning Models",
            4: "Generative AI Tips"
        }
        return names.get(phase, "Unknown")
    
    # ═══════════════════════════════════════════════════════════════════
    # PHASE 1: Data Ingestion
    # ═══════════════════════════════════════════════════════════════════
    
    def run_phase_1(self):
        """Phase 1: Extract FIT → Convert to CSV → Analyze Activities."""
        if 1 not in self.phases:
            return
            
        self.log_section(1)
        logger.info("Starting Phase 1: Data Ingestion")
        
        try:
            # Step 1.1: Check for FIT files
            fit_dir = DATA_DIR / "fit"
            fit_files = list(fit_dir.glob("*.fit"))
            
            if not fit_files:
                logger.warning(f"No FIT files found in {fit_dir}")
                logger.info("Skipping FIT conversion (no source files)")
                self.results[1] = {"status": "skipped", "reason": "no_fit_files"}
                return
            
            logger.info(f"Found {len(fit_files)} FIT files")
            
            # Step 1.2: Convert FIT to CSV
            logger.info("Converting FIT files to CSV...")
            if not self.dry_run:
                for fit_file in fit_files:
                    logger.info(f"  Converting: {fit_file.name}")
                    fit_converter.convert_fit_to_csv(str(fit_file))
            
            # Step 1.3: Analyze activities and create summary
            logger.info("Analyzing activities...")
            if not self.dry_run:
                activities_analyzer.analyze_all_activities()
            
            logger.info("✅ Phase 1 complete: Data ingested and analyzed")
            self.results[1] = {"status": "success"}
            
        except Exception as e:
            logger.error(f"❌ Phase 1 failed: {str(e)}")
            self.results[1] = {"status": "error", "error": str(e)}
            raise
    
    # ═══════════════════════════════════════════════════════════════════
    # PHASE 2: Data Analysis
    # ═══════════════════════════════════════════════════════════════════
    
    def run_phase_2(self):
        """Phase 2: Form Analysis → Target Profiles → Synthetic Data."""
        if 2 not in self.phases:
            return
        
        self.log_section(2)
        logger.info("Starting Phase 2: Data Analysis & Baselines")
        
        try:
            # Check if Activities.csv exists (from Phase 1)
            activities_file = DATA_DIR / "Activities.csv"
            if not activities_file.exists():
                logger.warning("Activities.csv not found. Running Phase 1 first...")
                self.run_phase_1()
            
            # Step 2.1: Form Analysis
            logger.info("Step 2.1: Analyzing running form...")
            if not self.dry_run:
                form_analyzer.analyze_and_score_form()
            
            # Step 2.2: Target Profiles
            logger.info("Step 2.2: Generating target profiles...")
            if not self.dry_run:
                target_profiles.print_profiles()
            
            # Step 2.3: Synthetic Data
            logger.info("Step 2.3: Generating synthetic training data...")
            if not self.dry_run:
                current = form_analyzer.load_current_profile()
                targets = target_profiles.load_target_profiles()
                
                if current and targets:
                    results = synthetic_data_generator.generate_all_profiles(
                        current, targets, output_csv=True
                    )
                    synthetic_data_generator.print_summary(results)
            
            logger.info("✅ Phase 2 complete: Form analysis, profiles, synthetic data ready")
            self.results[2] = {"status": "success"}
            
        except Exception as e:
            logger.error(f"❌ Phase 2 failed: {str(e)}")
            self.results[2] = {"status": "error", "error": str(e)}
            raise
    
    # ═══════════════════════════════════════════════════════════════════
    # PHASE 3: Machine Learning (Placeholder)
    # ═══════════════════════════════════════════════════════════════════
    
    def run_phase_3(self):
        """Phase 3: Train ML models on synthetic data."""
        if 3 not in self.phases:
            return
        
        self.log_section(3)
        logger.info("Starting Phase 3: Machine Learning Models")
        logger.warning("⚠️  Phase 3 modules not yet implemented")
        logger.info("Placeholder: Will train 3 models in final implementation")
        logger.info("  - Form Efficiency Predictor (LSTM)")
        logger.info("  - Running Dynamics Approximator (Regression)")
        logger.info("  - Zone Optimizer (Clustering)")
        
        self.results[3] = {"status": "not_implemented"}
    
    # ═══════════════════════════════════════════════════════════════════
    # PHASE 4: Generative AI (Placeholder)
    # ═══════════════════════════════════════════════════════════════════
    
    def run_phase_4(self):
        """Phase 4: Generate personalized AI tips."""
        if 4 not in self.phases:
            return
        
        self.log_section(4)
        logger.info("Starting Phase 4: Generative AI Tips")
        logger.warning("⚠️  Phase 4 modules not yet implemented")
        logger.info("Placeholder: Will generate personalized tips in final implementation")
        logger.info("  - Input: Current metrics + model predictions + target profile")
        logger.info("  - Output: Personalized form improvement tips")
        
        self.results[4] = {"status": "not_implemented"}
    
    # ═══════════════════════════════════════════════════════════════════
    # Execution
    # ═══════════════════════════════════════════════════════════════════
    
    def run(self):
        """Execute all selected phases."""
        print("\n")
        print("╔" + "=" * 78 + "╗")
        print("║" + " " * 78 + "║")
        print("║" + "  🏃 GARMIN RUNNING AI - UNIFIED PIPELINE ORCHESTRATOR  ".center(78) + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "=" * 78 + "╝")
        
        logger.info(f"Pipeline starting: {self.start_time.isoformat()}")
        logger.info(f"Phases to run: {self.phases}")
        
        if self.dry_run:
            logger.info("🔍 DRY RUN MODE - No actual execution")
        
        try:
            # Run selected phases
            if 1 in self.phases:
                self.run_phase_1()
            if 2 in self.phases:
                self.run_phase_2()
            if 3 in self.phases:
                self.run_phase_3()
            if 4 in self.phases:
                self.run_phase_4()
            
            # Print summary
            self.print_summary()
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            self.print_summary()
            sys.exit(1)
    
    def print_summary(self):
        """Print execution summary."""
        elapsed = datetime.now() - self.start_time
        
        print("\n")
        print("╔" + "=" * 78 + "╗")
        print("║" + " PIPELINE EXECUTION SUMMARY ".center(78) + "║")
        print("╚" + "=" * 78 + "╝")
        
        for phase in [1, 2, 3, 4]:
            if phase in self.results:
                result = self.results[phase]
                status = result.get("status")
                
                if status == "success":
                    symbol = "✅"
                    color = ""
                elif status == "skipped":
                    symbol = "⏭️ "
                    color = ""
                elif status == "not_implemented":
                    symbol = "⏸️ "
                    color = ""
                else:
                    symbol = "❌"
                    color = ""
                
                print(f"{symbol} Phase {phase}: {self._get_phase_name(phase)}")
                if "reason" in result:
                    print(f"   Reason: {result['reason']}")
        
        print(f"\n⏱️  Total time: {elapsed.total_seconds():.1f}s")
        print(f"📊 Output directory: {DATA_DIR}")
        
        # List generated files
        print("\n📁 Generated files:")
        for category, patterns in {
            "Analysis": ["form_analysis.json", "target_profiles.json"],
            "Data": ["Activities.csv", "running_profile.json"],
            "Synthetic": ["synthetic_*.csv"],
            "Models": ["models/*.pkl", "models/*.h5"]
        }.items():
            files = []
            for pattern in patterns:
                files.extend(DATA_DIR.glob(pattern))
            
            if files:
                print(f"\n  {category}:")
                for f in sorted(files):
                    size = f.stat().st_size if f.is_file() else "dir"
                    if isinstance(size, int):
                        size_str = f"{size:,} bytes" if size < 1024*1024 else f"{size/(1024*1024):.1f} MB"
                    else:
                        size_str = size
                    print(f"    - {f.name} ({size_str})")
        
        print("\n" + "=" * 80 + "\n")


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Unified Garmin Running AI Pipeline Orchestrator",
        epilog=__doc__
    )
    
    parser.add_argument(
        "--phase",
        type=str,
        default=None,
        help="Phases to run (comma-separated: 1,2,3,4). Default: all"
    )
    
    parser.add_argument(
        "--skip-phase",
        type=str,
        default=None,
        help="Phases to skip (comma-separated: 1,2,3,4). Default: none"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run mode: show plan without executing"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Parse phases
    phases = None
    if args.phase:
        phases = [int(p.strip()) for p in args.phase.split(",")]
    
    skip_phases = None
    if args.skip_phase:
        skip_phases = [int(p.strip()) for p in args.skip_phase.split(",")]
    
    # Create and run orchestrator
    orchestrator = PipelineOrchestrator(
        phases=phases,
        skip_phases=skip_phases,
        dry_run=args.dry_run
    )
    
    orchestrator.run()


if __name__ == "__main__":
    main()
