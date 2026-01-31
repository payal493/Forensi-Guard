#!/usr/bin/env python3
"""
Test script to run suspicion classification for case_002
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'ui'))

from app import classify_case_suspicion

def main():
    print("Testing Suspicion Classification for case_002")
    print("=" * 50)
    
    result = classify_case_suspicion('case_002')
    
    print('Suspicion Classification:')
    print('  Level:', result['suspicion_level'])
    print('  Score:', result['score'])
    print('  Reasons:')
    for reason in result['reasons']:
        print('    -', reason)

if __name__ == "__main__":
    main()
