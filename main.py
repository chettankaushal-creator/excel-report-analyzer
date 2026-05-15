#!/usr/bin/env python3
"""
Excel Report AI Agent with Learning Capabilities
Usage: python main.py [--now] [--schedule]
"""

import argparse
from orchestrator import ReportOrchestrator

def main():
    parser = argparse.ArgumentParser(description="AI Report Agent")
    parser.add_argument("--now", action="store_true", help="Run immediately")
    parser.add_argument("--schedule", type=str, default="08:00", 
                       help="Schedule time (HH:MM format)")
    
    args = parser.parse_args()
    
    orchestrator = ReportOrchestrator()
    
    if args.now:
        print("🚀 Running immediately...")
        orchestrator.run_daily_report()
    else:
        print(f"⏰ Scheduling for {args.schedule} daily...")
        orchestrator.schedule_daily(args.schedule)

if __name__ == "__main__":
    main()
