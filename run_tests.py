#!/usr/bin/env python3
"""
Test runner for INTENTRA
Runs all unit tests and displays results
"""
import sys
import unittest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def run_tests():
    """Run all tests and display results"""
    print("=" * 70)
    print("INTENTRA Test Suite")
    print("=" * 70)
    print()
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = str(project_root / "tests")
    suite = loader.discover(start_dir, pattern="test_*.py")
    
    # Run with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print()
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print()
    
    if result.wasSuccessful():
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
