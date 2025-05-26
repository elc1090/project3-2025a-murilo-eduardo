#!/usr/bin/env python3
"""
Simple test script to verify the API endpoints are working correctly
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_login_and_components():
    print("Testing API endpoints...")

    # Test 1: Create a user via login
    print("\n1. Creating user via login...")
    login_data = {
        "username": "testuser",
        "password": "testpass"
    }

    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Login response: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"User created: {user_data}")
        user_id = user_data["id"]
    else:
        print(f"Login failed: {response.text}")
        return

    # Test 2: Get user's components (should be empty)
    print(f"\n2. Getting components for user {user_id}...")
    response = requests.get(f"{BASE_URL}/user/{user_id}/components")
    print(f"User components response: {response.status_code}")
    if response.status_code == 200:
        components = response.json()
        print(f"User components: {components}")
    else:
        print(f"Failed to get user components: {response.text}")

    # Test 3: Create a component with tags as list
    print(f"\n3. Creating a component for user {user_id} with tags as list...")
    component_data = {
        "user_id": user_id,
        "title": "Test Button",
        "description": "A test button component",
        "framework": "vue",
        "category": "ui",
        "tags": ["vue", "frontend", "tailwindcss", "toast"],  # Using list format
        "inputType": "vue",
        "includeTailwind": True,
        "code": "<button class='btn btn-primary'>Test Button</button>"
    }

    response = requests.post(f"{BASE_URL}/component", json=component_data)
    print(f"Create component response: {response.status_code}")
    if response.status_code == 200:
        component = response.json()
        print(f"Component created: {component}")
    else:
        print(f"Failed to create component: {response.text}")

    # Test 4: Create another component with tags as string
    print(f"\n4. Creating another component for user {user_id} with tags as string...")
    component_data_2 = {
        "user_id": user_id,
        "title": "Test Card",
        "description": "A test card component",
        "framework": "react",
        "category": "cards",
        "tags": "react, card, display",  # Using string format
        "inputType": "html",
        "includeTailwind": False,
        "code": "<div class='card'>Test Card</div>"
    }

    response = requests.post(f"{BASE_URL}/component", json=component_data_2)
    print(f"Create second component response: {response.status_code}")
    if response.status_code == 200:
        component = response.json()
        print(f"Second component created: {component}")
    else:
        print(f"Failed to create second component: {response.text}")

    # Test 5: Get user's components again (should have 2 components)
    print(f"\n5. Getting components for user {user_id} again...")
    response = requests.get(f"{BASE_URL}/user/{user_id}/components")
    print(f"User components response: {response.status_code}")
    if response.status_code == 200:
        components = response.json()
        print(f"User components: {components}")
        print(f"Number of components: {len(components)}")

        # Check tags format
        for i, comp in enumerate(components):
            print(f"Component {i+1} tags: {comp['tags']} (type: {type(comp['tags'])})")
    else:
        print(f"Failed to get user components: {response.text}")

if __name__ == "__main__":
    try:
        test_login_and_components()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the Flask server. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"Error: {e}")
