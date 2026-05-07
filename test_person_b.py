"""
PERSON B - LOCAL TEST SUITE
Run this to verify all AI/NLP services work correctly before integration.

Command: python test_person_b.py
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import your services
from services.intent_service import IntentService, IntentType
from services.ai_service import AIService
from services.response_service import ResponseGenerator
from utils.regex_utils import RegexUtils

# ===== COLOR OUTPUT =====
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'

def success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

# ===== TEST SUITE =====

def test_intent_detection():
    """Test intent detection on various messages"""
    print("\n" + "=" * 70)
    print("TEST 1: INTENT DETECTION (Regex-based routing)")
    print("=" * 70)
    
    test_cases = [
        ("Need 200 titanium flanges by Friday", IntentType.CREATE_ORDER),
        ("Create order for 100 steel brackets", IntentType.CREATE_ORDER),
        ("Mark order 1 as accepted", IntentType.UPDATE_STATUS),
        ("Update status of order 5 to rejected", IntentType.UPDATE_STATUS),
        ("Order 3 passed thermal inspection", IntentType.QUALITY_REPORT),
        ("Log quality check for order 2", IntentType.QUALITY_REPORT),
        ("Show all accepted orders", IntentType.SHOW_ACCEPTED),
        ("List all orders", IntentType.SHOW_ACCEPTED),
    ]
    
    passed = 0
    for message, expected_intent in test_cases:
        detected_intent = IntentService.detect_intent(message)
        if detected_intent == expected_intent:
            success(f"'{message}' → {detected_intent.value}")
            passed += 1
        else:
            error(f"'{message}' → Got {detected_intent.value}, expected {expected_intent.value}")
    
    info(f"Passed: {passed}/{len(test_cases)}")
    return passed == len(test_cases)

def test_regex_utilities():
    """Test regex extraction utilities"""
    print("\n" + "=" * 70)
    print("TEST 2: REGEX UTILITIES (Pattern matching)")
    print("=" * 70)
    
    test_cases = [
        ("Order 5 needs 200 steel brackets", 5, 200, "Steel"),
        ("Order #10 with 500 titanium flanges", 10, 500, "Titanium"),
        ("Need 100 aluminum rods by Friday July 20", None, 100, "Aluminum"),
        ("Mark order 3 as accepted", 3, None, None),
    ]
    
    passed = 0
    for message, exp_id, exp_qty, exp_material in test_cases:
        order_id = RegexUtils.extract_order_id(message)
        quantity = RegexUtils.extract_quantity(message)
        material = RegexUtils.extract_material(message)
        
        id_ok = order_id == exp_id
        qty_ok = quantity == exp_qty
        mat_ok = material == exp_material
        
        if id_ok and qty_ok and mat_ok:
            success(f"'{message}'")
            print(f"    → ID: {order_id}, Qty: {quantity}, Material: {material}")
            passed += 1
        else:
            error(f"'{message}'")
            print(f"    → ID: {order_id} (expected {exp_id})")
            print(f"    → Qty: {quantity} (expected {exp_qty})")
            print(f"    → Material: {material} (expected {exp_material})")
    
    info(f"Passed: {passed}/{len(test_cases)}")
    return passed == len(test_cases)

def test_response_generation():
    """Test response formatting"""
    print("\n" + "=" * 70)
    print("TEST 3: RESPONSE GENERATION (Cinematic formatting)")
    print("=" * 70)
    
    try:
        # Mock order
        mock_order = {
            "id": 1,
            "part_name": "Titanium Flange",
            "material": "Titanium",
            "quantity": 200,
            "deadline": "Friday",
            "status": "PENDING"
        }
        
        # Test different response types
        responses = [
            ("ORDER_CREATED", ResponseGenerator.order_created_response(mock_order)),
            ("STATUS_UPDATED", ResponseGenerator.status_updated_response(mock_order, "PENDING", "ACCEPTED")),
            ("QUALITY_LOGGED", ResponseGenerator.quality_logged_response(mock_order, "THERMAL")),
            ("ORDERS_LIST", ResponseGenerator.orders_list_response([mock_order])),
            ("ERROR", ResponseGenerator.error_response("Test error")),
        ]
        
        all_valid = True
        for response_type, response in responses:
            # Check required fields
            required_fields = ["type", "status", "message", "data", "ui_hint", "timestamp"]
            has_all_fields = all(field in response for field in required_fields)
            
            if has_all_fields and response["type"] == response_type:
                success(f"{response_type} response valid")
                info(f"  Message: {response['message'][:50]}...")
                info(f"  UI Hint: {response['ui_hint']}")
            else:
                error(f"{response_type} response missing fields")
                all_valid = False
        
        return all_valid
        
    except Exception as e:
        error(f"Response generation failed: {e}")
        return False

def test_ai_service():
    """Test AI service (optional - requires API key)"""
    print("\n" + "=" * 70)
    print("TEST 4: AI SERVICE (Optional - requires Groq API key)")
    print("=" * 70)
    
    try:
        ai_service = AIService()
        
        # Test extraction
        test_message = "Need 500 aluminum rods delivered by next Wednesday"
        info(f"Testing extraction: '{test_message}'")
        
        result = ai_service.extract_order_data(test_message)
        
        if result.get("success"):
            success("AI extraction successful")
            print(f"  → Part: {result.get('part_name')}")
            print(f"  → Material: {result.get('material')}")
            print(f"  → Quantity: {result.get('quantity')}")
            print(f"  → Deadline: {result.get('deadline')}")
            return True
        else:
            warning(f"AI extraction returned success=False: {result.get('error')}")
            return False
            
    except ValueError as e:
        warning(f"API key not found or invalid: {e}")
        return None
    except Exception as e:
        error(f"AI service test failed: {e}")
        return False

def test_integration_flow():
    """Test a complete flow"""
    print("\n" + "=" * 70)
    print("TEST 5: INTEGRATION FLOW (End-to-end)")
    print("=" * 70)
    
    try:
        # Simulate a complete flow
        user_message = "I need 300 steel brackets by Friday for assembly"
        
        info(f"User: {user_message}")
        
        # Step 1: Detect intent
        intent = IntentService.detect_intent(user_message)
        info(f"Intent: {intent.value}")
        
        # Step 2: Extract metadata
        metadata = IntentService.get_intent_metadata(user_message)
        info(f"Needs AI: {metadata['needs_ai']}")
        
        # Step 3: Extract data with regex
        qty = RegexUtils.extract_quantity(user_message)
        material = RegexUtils.extract_material(user_message)
        deadline = RegexUtils.extract_deadline(user_message)
        
        info(f"Quick extraction: Qty={qty}, Material={material}, Deadline={deadline}")
        
        # Step 4: Format response
        mock_order = {
            "id": 1,
            "part_name": "Steel Bracket",
            "quantity": qty or 300,
            "material": material or "Steel",
            "deadline": deadline or "Friday"
        }
        
        response = ResponseGenerator.order_created_response(mock_order)
        
        success("Full integration flow completed")
        info(f"Response type: {response['type']}")
        info(f"Message: {response['message']}")
        info(f"UI Hint: {response['ui_hint']}")
        
        return True
        
    except Exception as e:
        error(f"Integration flow failed: {e}")
        return False

# ===== MAIN TEST RUNNER =====

def main():
    print("\n")
    print(f"{Colors.BLUE}" + "=" * 70)
    print("PERSON B - SERVICE TEST SUITE".center(70))
    print("=" * 70 + f"{Colors.END}")
    
    results = {}
    
    # Run tests
    results["Intent Detection"] = test_intent_detection()
    results["Regex Utilities"] = test_regex_utilities()
    results["Response Generation"] = test_response_generation()
    results["AI Service"] = test_ai_service()
    results["Integration Flow"] = test_integration_flow()
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY".center(70))
    print("=" * 70)
    
    for test_name, result in results.items():
        if result is True:
            success(f"{test_name}: PASSED")
        elif result is False:
            error(f"{test_name}: FAILED")
        else:
            warning(f"{test_name}: SKIPPED")
    
    # Overall result
    passed = sum(1 for r in results.values() if r is True)
    total = len(results)
    
    print("\n" + "=" * 70)
    if passed == total:
        print(f"{Colors.GREEN}🎉 ALL TESTS PASSED! Ready for integration.{Colors.END}".center(70))
    else:
        print(f"{Colors.YELLOW}⚠️  Some tests failed or skipped.{Colors.END}".center(70))
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
