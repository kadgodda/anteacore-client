#!/usr/bin/env python3
"""
Test the AnteaCore client package with the live Railway API
"""

import json
from anteacore_client import AnteaCoreClient
from anteacore_client.identity import get_machine_id

def test_client():
    print("=== AnteaCore Client API Test ===\n")
    
    # Show machine ID
    machine_id = get_machine_id()
    print(f"Machine ID: {machine_id}")
    
    # Initialize client
    client = AnteaCoreClient()
    print(f"API URL: {client.api_url}\n")
    
    # Test 1: Connection test
    print("1. Testing connection...")
    result = client.test_connection()
    print(f"   Result: {json.dumps(result, indent=2)}\n")
    
    # Test 2: Search knowledge base
    print("2. Testing knowledge search...")
    search_result = client.search_knowledge("error handling", limit=5)
    print(f"   Found {len(search_result.get('results', []))} results")
    if search_result.get('results'):
        print("   First result:", search_result['results'][0].get('name', 'N/A'))
    print(f"   Full response: {json.dumps(search_result, indent=2)}\n")
    
    # Test 3: Add a test pattern
    print("3. Testing pattern contribution...")
    pattern_result = client.add_pattern(
        name="test-pattern-from-client",
        category="testing",
        problem="Testing the client API connection",
        solution="Successfully connected and submitted pattern",
        code_example="client = AnteaCoreClient()\nresult = client.test_connection()",
        tags=["test", "api", "client"]
    )
    print(f"   Result: {json.dumps(pattern_result, indent=2)}\n")
    
    # Test 4: Report an issue
    print("4. Testing issue reporting...")
    issue_result = client.report_issue(
        issue="Test issue from client API",
        error_message="No actual error - this is a test",
        context="Testing the live Railway deployment"
    )
    print(f"   Result: {json.dumps(issue_result, indent=2)}\n")
    
    # Test 5: Get contribution stats
    print("5. Testing contribution stats...")
    stats_result = client.get_stats()
    print(f"   Result: {json.dumps(stats_result, indent=2)}\n")
    
    print("=== All tests completed! ===")

if __name__ == "__main__":
    test_client()