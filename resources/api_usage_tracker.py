"""
Persistent API Usage Tracker
Prevents quota exhaustion across script executions

Features:
- Persistent state file (survives restarts)
- Multi-key support with auto-rotation
- Per-key billing cycle tracking
- Usage warnings (75%, 90%, 100%)
- 60-second warning before key switch
- Historical usage logging
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional, List


class PersistentAPIUsageTracker:
    """
    Tracks cumulative API usage across script executions.

    State File: log/api_usage_state.json
    Format:
    {
        "api_keys": {
            "primary-SerpAPI": {
                "total_calls_used": 150,
                "monthly_limit": 250,
                "billing_cycle_day": 1,
                "last_reset": "2025-10-01",
                "current_month": "2025-10",
                "daily_usage": {"2025-10-29": 25}
            }
        },
        "metadata": {
            "tracking_start": "2025-10-01",
            "last_updated": "2025-10-29T19:30:00Z",
            "current_key": "primary-SerpAPI"
        }
    }
    """

    def __init__(self, config: Dict, state_file: str = "log/api_usage_state.json"):
        """
        Initialize API usage tracker.

        Args:
            config: Configuration dictionary (from config.json)
            state_file: Path to persistent state file
        """
        self.config = config
        self.state_file = state_file
        self.state = self.load_state()
        self.current_key = self.state['metadata'].get('current_key', None)

        # Ensure log directory exists
        os.makedirs(os.path.dirname(state_file), exist_ok=True)

    def load_state(self) -> Dict:
        """Load persistent state or initialize new"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    # Check for monthly resets
                    self.check_monthly_resets(state)
                    return state
            except json.JSONDecodeError:
                print(f"⚠️ Corrupted state file, reinitializing...")
                return self.initialize_state()

        return self.initialize_state()

    def initialize_state(self) -> Dict:
        """Create new state structure"""
        state = {
            "api_keys": {},
            "metadata": {
                "tracking_start": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "current_key": None
            }
        }

        # Initialize each API key
        for key_info in self.config['api_keys']:
            label = key_info['label']
            state['api_keys'][label] = {
                "total_calls_used": 0,
                "monthly_limit": key_info['monthly_limit'],
                "billing_cycle_day": key_info.get('billing_cycle_day', 1),
                "last_reset": datetime.now().replace(day=1).strftime("%Y-%m-%d"),
                "current_month": datetime.now().strftime("%Y-%m"),
                "daily_usage": {}
            }

        return state

    def save_state(self):
        """Save state to disk"""
        self.state['metadata']['last_updated'] = datetime.now().isoformat()

        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def check_monthly_resets(self, state: Dict):
        """Check if any keys need monthly reset"""
        today = datetime.now()

        for label, key_state in state['api_keys'].items():
            billing_day = key_state.get('billing_cycle_day', 1)
            last_reset_month = key_state.get('current_month', '')
            current_month = today.strftime("%Y-%m")

            # Check if we've passed billing day in new month
            if current_month != last_reset_month and today.day >= billing_day:
                print(f"✅ Monthly reset for API key '{label}' (billing cycle day: {billing_day})")
                key_state['total_calls_used'] = 0
                key_state['current_month'] = current_month
                key_state['last_reset'] = today.strftime("%Y-%m-%d")
                key_state['daily_usage'] = {}

    def get_available_key(self) -> Tuple[Optional[Dict], int]:
        """
        Return API key with remaining quota.
        Auto-rotates to next key when current exhausted.

        Returns:
            (key_info dict, remaining_calls int) or (None, 0) if all exhausted
        """
        # Sort keys by priority
        sorted_keys = sorted(self.config['api_keys'], key=lambda x: x['priority'])

        for key_info in sorted_keys:
            label = key_info['label']
            used = self.state['api_keys'][label]['total_calls_used']
            limit = key_info['monthly_limit']
            remaining = limit - used

            if remaining > 0:
                # Check if we need to announce key switch
                if self.current_key and self.current_key != label:
                    self.announce_key_switch(label, remaining, limit)
                elif self.current_key is None:
                    print(f"🔑 Using API key: {label} ({remaining}/{limit} calls remaining)")

                self.current_key = label
                self.state['metadata']['current_key'] = label
                self.save_state()

                return key_info, remaining

        # All keys exhausted
        return None, 0

    def announce_key_switch(self, new_key_label: str, remaining: int, limit: int):
        """
        Announce API key switch with 60-second warning period.
        Allows user to press Ctrl+C to stop safely.
        """
        print("\n" + "="*70)
        print("🔄 API KEY SWITCH REQUIRED")
        print("="*70)
        print(f"Previous key exhausted. Switching to: {new_key_label}")
        print(f"Remaining calls on new key: {remaining}/{limit}")
        print("\n⚠️  WAITING 60 SECONDS BEFORE CONTINUING")
        print("\n📋 Your Options:")
        print("   1. Wait 60 seconds → Script continues with new API key")
        print("   2. Press Ctrl+C NOW → Stop script safely")
        print("\n⚠️  RISKS OF STOPPING NOW:")
        print("   - Partial results (data collected so far IS saved)")
        print("   - Companies remaining will not be processed")
        print("   - Must restart script to process remaining companies")
        print("   - Checkpoint saves prevent data loss (safe to stop)")
        print("\n✅ SAFE TO STOP: Results saved every 25 companies")
        print("="*70)

        # 60-second countdown with Ctrl+C detection
        try:
            for remaining_time in range(60, 0, -10):
                print(f"   ⏳ Continuing in {remaining_time} seconds... (Ctrl+C to stop)")
                time.sleep(10)

            print(f"\n▶️  RESUMING with new API key: {new_key_label}\n")

        except KeyboardInterrupt:
            print("\n\n🛑 USER STOPPED SCRIPT (Ctrl+C detected)")
            print("="*70)
            print("✅ Safe stop - checkpoint data is saved")
            print("\n💡 To resume processing remaining companies:")
            print("   1. Restart script with same settings")
            print("   2. Script will process companies not yet completed")
            print("="*70)
            sys.exit(0)

    def increment_usage(self, key_label: str, calls: int = 1):
        """
        Increment usage counter and save state.

        Args:
            key_label: API key label
            calls: Number of calls to add (default: 1)
        """
        if key_label not in self.state['api_keys']:
            print(f"⚠️ Warning: Key '{key_label}' not in state, initializing...")
            # Find key info from config
            key_info = next((k for k in self.config['api_keys'] if k['label'] == key_label), None)
            if key_info:
                self.state['api_keys'][key_label] = {
                    "total_calls_used": 0,
                    "monthly_limit": key_info['monthly_limit'],
                    "billing_cycle_day": key_info.get('billing_cycle_day', 1),
                    "last_reset": datetime.now().replace(day=1).strftime("%Y-%m-%d"),
                    "current_month": datetime.now().strftime("%Y-%m"),
                    "daily_usage": {}
                }

        # Increment total
        self.state['api_keys'][key_label]['total_calls_used'] += calls

        # Update daily usage
        today = datetime.now().strftime("%Y-%m-%d")
        daily = self.state['api_keys'][key_label]['daily_usage']
        daily[today] = daily.get(today, 0) + calls

        # Save state
        self.save_state()

        # Check warnings
        self.check_warnings(key_label)

    def check_warnings(self, key_label: str):
        """
        Warn at 75%, 90%, 100% thresholds.
        """
        used = self.state['api_keys'][key_label]['total_calls_used']
        limit = self.state['api_keys'][key_label]['monthly_limit']
        pct = (used / limit) * 100

        if pct >= 100:
            print(f"\n⚠️ API KEY EXHAUSTED: {key_label} ({used}/{limit} = 100%)")
            print(f"   Will auto-rotate to next key on next call")
        elif pct >= 90:
            remaining = limit - used
            print(f"\n⚠️ API KEY 90% USED: {key_label} ({used}/{limit} = {pct:.1f}%)")
            print(f"   {remaining} calls remaining")
        elif pct >= 75:
            remaining = limit - used
            print(f"\n⚠️ API KEY 75% USED: {key_label} ({used}/{limit} = {pct:.1f}%)")
            print(f"   {remaining} calls remaining")

    def get_usage_report(self) -> str:
        """Generate formatted usage report"""
        report = []
        report.append("\n" + "="*70)
        report.append("API USAGE REPORT")
        report.append("="*70)

        for label, key_state in self.state['api_keys'].items():
            used = key_state['total_calls_used']
            limit = key_state['monthly_limit']
            pct = (used / limit) * 100
            remaining = limit - used

            status = "🟢 Available"
            if pct >= 100:
                status = "🔴 Exhausted"
            elif pct >= 90:
                status = "🟠 Critical"
            elif pct >= 75:
                status = "🟡 Warning"

            report.append(f"\n{status} {label}:")
            report.append(f"  Used: {used}/{limit} ({pct:.1f}%)")
            report.append(f"  Remaining: {remaining}")
            report.append(f"  Billing Cycle: Day {key_state['billing_cycle_day']} of month")
            report.append(f"  Last Reset: {key_state['last_reset']}")

            # Show recent daily usage (last 7 days)
            daily = key_state['daily_usage']
            if daily:
                report.append(f"  Recent Usage:")
                for day, calls in sorted(daily.items())[-7:]:
                    report.append(f"    {day}: {calls} calls")

        report.append("\n" + "="*70)
        report.append("OPTIONS:")
        report.append("  - Wait for monthly reset (check billing cycle)")
        report.append("  - Request premium usage limits (contact serpapi.com/support)")
        report.append("  - Add more API keys to config.json")
        report.append("="*70 + "\n")

        return "\n".join(report)


# ======================================================
# COMMAND-LINE INTERFACE
# ======================================================

if __name__ == "__main__":
    """
    Command-line tool for checking API usage.

    Usage:
        python resources/api_usage_tracker.py --report
    """
    import argparse

    parser = argparse.ArgumentParser(description='API Usage Tracker')
    parser.add_argument('--report', action='store_true', help='Show usage report')
    parser.add_argument('--reset', type=str, help='Reset usage for specific key')
    args = parser.parse_args()

    # Load config
    config_file = "resources/config.json"
    if not os.path.exists(config_file):
        print(f"❌ Config file not found: {config_file}")
        sys.exit(1)

    with open(config_file, 'r') as f:
        config = json.load(f)

    tracker = PersistentAPIUsageTracker(config)

    if args.report:
        print(tracker.get_usage_report())
    elif args.reset:
        if args.reset in tracker.state['api_keys']:
            tracker.state['api_keys'][args.reset]['total_calls_used'] = 0
            tracker.state['api_keys'][args.reset]['daily_usage'] = {}
            tracker.save_state()
            print(f"✅ Reset usage for: {args.reset}")
        else:
            print(f"❌ Key not found: {args.reset}")
            print(f"Available keys: {', '.join(tracker.state['api_keys'].keys())}")
    else:
        print("Usage: python resources/api_usage_tracker.py --report")
