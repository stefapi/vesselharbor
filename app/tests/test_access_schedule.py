#!/usr/bin/env python3

"""
Test script to verify the access_schedule functionality in permissions.py
"""

#  Copyright (c) 2025.  VesselHarbor
#
#  ____   ____                          .__    ___ ___             ___.
#  \   \ /   /____   ______ ______ ____ |  |  /   |   \_____ ______\_ |__   ___________
#   \   Y   // __ \ /  ___//  ___// __ \|  | /    ~    \__  \\_  __ \ __ \ /  _ \_  __ \
#    \     /\  ___/ \___ \ \___ \\  ___/|  |_\    Y    // __ \|  | \/ \_\ (  <_> )  | \/
#     \___/  \___  >____  >____  >\___  >____/\___|_  /(____  /__|  |___  /\____/|__|
#                \/     \/     \/     \/            \/      \/          \/
#
#
#  MIT License
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from datetime import datetime
import json
from helper.permissions import is_in_cron_interval, is_rule_accessible_now

class MockRule:
    """Mock rule class for testing"""
    def __init__(self, access_schedule=None):
        self.access_schedule = access_schedule

def test_cron_interval():
    """Test the cron interval function"""
    print("Testing cron interval function...")

    # Test case 1: Current time should be in a 24/7 interval
    test_dt = datetime.now()
    # Cron for every minute: "* * * * *"
    # This should always be true for any current time
    result = is_in_cron_interval(test_dt, "* * * * *", "59 23 * * *")  # Start any minute, end at 23:59
    print(f"24/7 access test: {result}")

    # Test case 2: Test with specific time ranges
    # Business hours: 9 AM to 5 PM on weekdays
    business_start = "0 9 * * 1-5"  # 9 AM Monday to Friday
    business_end = "0 17 * * 1-5"   # 5 PM Monday to Friday

    # Create a test datetime for Tuesday at 2 PM
    tuesday_2pm = datetime(2024, 1, 2, 14, 0, 0)  # January 2nd, 2024 is a Tuesday
    result = is_in_cron_interval(tuesday_2pm, business_start, business_end)
    print(f"Business hours test (Tuesday 2 PM): {result}")

    # Create a test datetime for Saturday at 2 PM
    saturday_2pm = datetime(2024, 1, 6, 14, 0, 0)  # January 6th, 2024 is a Saturday
    result = is_in_cron_interval(saturday_2pm, business_start, business_end)
    print(f"Business hours test (Saturday 2 PM): {result}")

def test_rule_accessibility():
    """Test the rule accessibility function"""
    print("\nTesting rule accessibility function...")

    # Test case 1: Rule without access_schedule (should always be accessible)
    rule_no_schedule = MockRule()
    result = is_rule_accessible_now(rule_no_schedule)
    print(f"Rule without schedule: {result}")

    # Test case 2: Rule with 24/7 access schedule
    schedule_24_7 = {"start": "* * * * *", "end": "59 23 * * *"}
    rule_24_7 = MockRule(access_schedule=json.dumps(schedule_24_7))
    result = is_rule_accessible_now(rule_24_7)
    print(f"Rule with 24/7 schedule: {result}")

    # Test case 3: Rule with business hours schedule
    schedule_business = {"start": "0 9 * * 1-5", "end": "0 17 * * 1-5"}
    rule_business = MockRule(access_schedule=json.dumps(schedule_business))
    result = is_rule_accessible_now(rule_business)
    print(f"Rule with business hours schedule: {result}")

    # Test case 4: Rule with dict access_schedule (not JSON string)
    rule_dict = MockRule(access_schedule=schedule_24_7)
    result = is_rule_accessible_now(rule_dict)
    print(f"Rule with dict schedule: {result}")

    # Test case 5: Rule with invalid JSON (should default to accessible)
    rule_invalid = MockRule(access_schedule="invalid json")
    result = is_rule_accessible_now(rule_invalid)
    print(f"Rule with invalid JSON: {result}")

    # Test case 6: Rule with missing keys (should default to accessible)
    schedule_incomplete = {"start": "0 9 * * 1-5"}  # Missing 'end' key
    rule_incomplete = MockRule(access_schedule=json.dumps(schedule_incomplete))
    result = is_rule_accessible_now(rule_incomplete)
    print(f"Rule with incomplete schedule: {result}")

if __name__ == "__main__":
    print("Testing access_schedule functionality")
    print("=" * 50)

    try:
        test_cron_interval()
        test_rule_accessibility()
        print("\n" + "=" * 50)
        print("All tests completed successfully!")
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
