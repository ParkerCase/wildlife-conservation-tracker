#!/usr/bin/env python3
"""
Test script to verify JSON file creation and identify upload issues
"""

import json
import os
from datetime import datetime


def test_json_creation():
    """Test creating the JSON files that the workflow needs"""

    print("🧪 Testing JSON file creation...")

    # Test 1: Create human_trafficking_results.json
    results_data = {
        "total_scanned": 0,
        "total_stored": 0,
        "human_trafficking_alerts": 0,
        "critical_alerts": 0,
        "human_review_required": 0,
        "vision_analyzed": 0,
        "platforms_scanned": ["craigslist", "gumtree", "olx"],
        "errors": ["Test error"],
        "scan_status": "test",
        "timestamp": datetime.now().isoformat(),
    }

    try:
        with open("human_trafficking_results.json", "w") as f:
            json.dump(results_data, f, indent=2)
        print("✅ human_trafficking_results.json created successfully")

        # Check file size
        size = os.path.getsize("human_trafficking_results.json")
        print(f"   File size: {size} bytes")

    except Exception as e:
        print(f"❌ Failed to create human_trafficking_results.json: {e}")

    # Test 2: Create human_trafficking_keyword_state.json
    keyword_state = {
        "last_index": 0,
        "total_keywords": 50,
        "last_run": datetime.now().isoformat(),
        "completed_cycles": 0,
        "high_priority_platforms": ["craigslist", "gumtree", "olx", "facebook"],
    }

    try:
        with open("human_trafficking_keyword_state.json", "w") as f:
            json.dump(keyword_state, f, indent=2)
        print("✅ human_trafficking_keyword_state.json created successfully")

        # Check file size
        size = os.path.getsize("human_trafficking_keyword_state.json")
        print(f"   File size: {size} bytes")

    except Exception as e:
        print(f"❌ Failed to create human_trafficking_keyword_state.json: {e}")

    # Test 3: Check if files exist and are readable
    print("\n📁 Checking file existence and permissions...")

    files_to_check = [
        "human_trafficking_results.json",
        "human_trafficking_keyword_state.json",
    ]

    for filename in files_to_check:
        if os.path.exists(filename):
            print(f"✅ {filename} exists")

            # Check permissions
            mode = os.stat(filename).st_mode
            print(f"   Permissions: {oct(mode)}")

            # Check if readable
            try:
                with open(filename, "r") as f:
                    content = f.read()
                print(f"   Readable: Yes ({len(content)} characters)")
            except Exception as e:
                print(f"   Readable: No - {e}")
        else:
            print(f"❌ {filename} does not exist")

    # Test 4: Check current working directory
    print(f"\n📂 Current working directory: {os.getcwd()}")

    # Test 5: List all files in current directory
    print("\n📋 Files in current directory:")
    for file in os.listdir("."):
        if file.endswith(".json"):
            size = os.path.getsize(file)
            print(f"   {file} ({size} bytes)")


if __name__ == "__main__":
    test_json_creation()
