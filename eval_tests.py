"""
Offline evaluation script for NotePilot.
Tests input validation, prompt injection detection, and input length guards.
"""
import json
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import validate_input, check_prompt_injection, MAX_INPUT_LENGTH


def load_tests():
    """Load test cases from tests.json."""
    with open('tests/tests.json', 'r') as f:
        data = json.load(f)
    return data['test_cases']


def run_test(test_case):
    """Run a single test case and return pass/fail."""
    test_id = test_case['id']
    test_type = test_case['type']
    input_text = test_case['input']
    expected = test_case['expected_behavior']
    description = test_case['description']
    
    # Handle repeated input for length tests
    if 'repeat' in test_case:
        input_text = input_text * test_case['repeat']
    
    # Run validation
    is_valid, error_msg = validate_input(input_text)
    
    # Determine actual behavior
    if not is_valid:
        if error_msg and 'empty' in error_msg.lower():
            actual = 'reject_empty'
        elif error_msg and 'too long' in error_msg.lower():
            actual = 'reject_length'
        elif error_msg and 'invalid input' in error_msg.lower():
            actual = 'reject_injection'
        else:
            actual = 'reject_other'
    else:
        actual = 'accept'
    
    # Check if test passed
    passed = (actual == expected)
    
    return {
        'id': test_id,
        'type': test_type,
        'description': description,
        'expected': expected,
        'actual': actual,
        'passed': passed
    }


def run_all_tests():
    """Run all tests and generate report."""
    print("=" * 70)
    print("NotePilot offline eval tests")
    print("=" * 70)
    print()
    
    test_cases = load_tests()
    results = []
    
    for test_case in test_cases:
        result = run_test(test_case)
        results.append(result)
    
    # Calculate statistics
    total = len(results)
    passed = sum(1 for r in results if r['passed'])
    failed = total - passed
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    # Print detailed results
    print("DETAILED RESULTS:")
    print("-" * 70)
    
    for result in results:
        status = "✓ PASS" if result['passed'] else "✗ FAIL"
        print(f"Test #{result['id']:2d} [{result['type']:20s}] {status}")
        print(f"  Description: {result['description']}")
        if not result['passed']:
            print(f"  Expected: {result['expected']}, Got: {result['actual']}")
        print()
    
    # Print summary
    print("=" * 70)
    print("SUMMARY:")
    print("-" * 70)
    print(f"Total Tests:  {total}")
    print(f"Passed:       {passed} ({pass_rate:.1f}%)")
    print(f"Failed:       {failed}")
    print()
    
    # Breakdown by category
    categories = {}
    for result in results:
        cat = result['type']
        if cat not in categories:
            categories[cat] = {'total': 0, 'passed': 0}
        categories[cat]['total'] += 1
        if result['passed']:
            categories[cat]['passed'] += 1
    
    print("CATEGORY BREAKDOWN:")
    print("-" * 70)
    for cat, stats in sorted(categories.items()):
        cat_pass_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"{cat:25s}: {stats['passed']}/{stats['total']} ({cat_pass_rate:.1f}%)")
    
    print("=" * 70)
    
    # Return exit code based on pass rate
    if pass_rate == 100:
        print("✓ All tests PASSED (100% pass rate)")
        return 0
    elif pass_rate >= 80:
        print("✓ Evaluation PASSED (≥80% pass rate)")
        return 0
    else:
        print("✗ Evaluation FAILED (<80% pass rate)")
        return 1


if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)
