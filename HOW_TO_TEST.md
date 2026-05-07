# 🧪 HOW TO TEST PERSON B'S WORK

## Quick Test (3 Steps)

### Step 1: Install Dependencies

```bash
cd c:\Users\Home\OneDrive\Desktop\nova-nexus\backend

# Install required packages
cd ..
```

Expected output:
```
Successfully installed groq python-dotenv fastapi uvicorn
```

---

### Step 2: Verify .env File

```bash
# Check if .env has your API key
cat .env
```

Should show:
```
GROQ_API_KEY=gsk_your_key_here
```

✅ If you see this, good! If empty, add your key.

---

### Step 3: Run Test Suite

```bash
# Run the complete test
python test_person_b.py
```

---

## Expected Output

```
======================================================================
PERSON B - SERVICE TEST SUITE
======================================================================

TEST 1: INTENT DETECTION (Regex-based routing)
======================================================================
✅ "Need 200 titanium flanges by Friday" → CREATE_ORDER
✅ "Create order for 100 steel brackets" → CREATE_ORDER
✅ "Mark order 1 as accepted" → UPDATE_STATUS
✅ "Update status of order 5 to rejected" → UPDATE_STATUS
✅ "Order 3 passed thermal inspection" → QUALITY_REPORT
✅ "Log quality check for order 2" → QUALITY_REPORT
✅ "Show all accepted orders" → SHOW_ACCEPTED
✅ "List all orders" → SHOW_ACCEPTED
ℹ️  Passed: 8/8

TEST 2: REGEX UTILITIES (Pattern matching)
======================================================================
✅ "Order 5 needs 200 steel brackets"
    → ID: 5, Qty: 200, Material: Steel
✅ "Order #10 with 500 titanium flanges"
    → ID: 10, Qty: 500, Material: Titanium
✅ "Need 100 aluminum rods by Friday July 20"
    → ID: None, Qty: 100, Material: Aluminum
✅ "Mark order 3 as accepted"
    → ID: 3, Qty: None, Material: None
ℹ️  Passed: 4/4

TEST 3: RESPONSE GENERATION (Cinematic formatting)
======================================================================
✅ ORDER_CREATED response valid
  Message: ✅ Manufacturing order #1 successfully registered...
  UI Hint: success-glow
✅ STATUS_UPDATED response valid
  Message: Order #1 status: PENDING → ACCEPTED
  UI Hint: pulse-success
✅ QUALITY_LOGGED response valid
  Message: ✓ THERMAL quality check logged for order #1
  UI Hint: pulse-info
✅ ORDERS_LIST response valid
  Message: Found 1 all orders
  UI Hint: fade-in
✅ ERROR response valid
  Message: Test error
  UI Hint: error-pulse

TEST 4: AI SERVICE (Optional - requires Groq API key)
======================================================================
ℹ️  Testing extraction: 'Need 500 aluminum rods delivered by next Wednesday'
✅ AI extraction successful
  → Part: Aluminum Rod
  → Material: Aluminum
  → Quantity: 500
  → Deadline: Wednesday

TEST 5: INTEGRATION FLOW (End-to-end)
======================================================================
ℹ️  User: I need 300 steel brackets by Friday for assembly
ℹ️  Intent: CREATE_ORDER
ℹ️  Needs AI: True
ℹ️  Quick extraction: Qty=300, Material=Steel, Deadline=Friday
✅ Full integration flow completed
ℹ️  Response type: ORDER_CREATED
ℹ️  Message: ✅ Manufacturing order #1 successfully registered.
ℹ️  UI Hint: success-glow

======================================================================
TEST SUMMARY
======================================================================
✅ Intent Detection: PASSED
✅ Regex Utilities: PASSED
✅ Response Generation: PASSED
✅ AI Service: PASSED
✅ Integration Flow: PASSED

======================================================================
🎉 ALL TESTS PASSED! Ready for integration.
======================================================================
```

---

## What Each Test Verifies

### ✅ TEST 1: Intent Detection
**Checks:** Can it correctly identify what user wants?

| Input | Expected | Your Result |
|-------|----------|------------|
| "Need 200 titanium flanges by Friday" | CREATE_ORDER | ✅ |
| "Mark order 1 as accepted" | UPDATE_STATUS | ✅ |
| "Order 3 passed thermal inspection" | QUALITY_REPORT | ✅ |
| "Show all accepted orders" | SHOW_ACCEPTED | ✅ |

**Success if:** All 8 messages detected correctly

---

### ✅ TEST 2: Regex Utilities
**Checks:** Can it extract quantities, materials, order IDs?

| Input | Extract | Your Result |
|-------|---------|------------|
| "Order 5 needs 200 steel brackets" | qty=200, mat=Steel, id=5 | ✅ |
| "Need 100 aluminum rods" | qty=100, mat=Aluminum | ✅ |

**Success if:** All extractions match expected values

---

### ✅ TEST 3: Response Generation
**Checks:** Do responses include ui_hint for animations?

```python
response = {
    "type": "ORDER_CREATED",
    "message": "✅ Order #1 registered",
    "data": {...},
    "ui_hint": "success-glow",  ← ✅ Must be present!
    "status": "success",
    "timestamp": "2024-01-15..."
}
```

**Success if:** All responses have these 6 fields

---

### ✅ TEST 4: AI Service
**Checks:** Can it call Groq API and extract data?

```
Input: "Need 500 aluminum rods delivered by next Wednesday"

Output: {
    "part_name": "Aluminum Rod",
    "material": "Aluminum",
    "quantity": 500,
    "deadline": "Wednesday",
    "success": True
}
```

**Success if:** Extraction is accurate

**Note:** May show warning if API key invalid, but code still works

---

### ✅ TEST 5: Integration Flow
**Checks:** Do all 4 services work together?

```
Step 1: Intent Detection → CREATE_ORDER ✅
Step 2: Get Metadata → needs_ai: True ✅
Step 3: Regex Extraction → qty=300, material=Steel ✅
Step 4: AI Extraction → part_name extracted ✅
Step 5: Response Generator → Returns with ui_hint ✅
```

**Success if:** All 5 steps complete without errors

---

## If Tests Fail - Troubleshooting

### ❌ Error: `ModuleNotFoundError: No module named 'groq'`

```bash
# Fix: Install missing package
pip install groq python-dotenv
```

---

### ❌ Error: `GROQ_API_KEY not found in .env file`

```bash
# Check if .env exists
cat .env

# If empty or missing, add your key:
echo GROQ_API_KEY=gsk_your_key_here > .env
```

---

### ❌ Error: `NameError: name 'IntentService' is not defined`

```bash
# Make sure you're in backend directory
cd c:\Users\Home\OneDrive\Desktop\nova-nexus\backend

# Not from root:
cd c:\Users\Home\OneDrive\Desktop\nova-nexus
python backend/test_person_b.py  # ❌ Won't work

# Correct:
cd backend
python test_person_b.py  # ✅ Works
```

---

### ❌ Test shows "SKIPPED" for AI Service

```
⚠️  API key not found or invalid
```

**This is OK!** Your code is working, just API key issue.

**Fix:** Add valid Groq API key to `.env`

Get one free at: https://console.groq.com

---

## Manual Testing (If You Want to Test Individual Services)

### Test Intent Detection

```bash
python -c "
from services.intent_service import IntentService

msg = 'Need 200 titanium flanges by Friday'
intent = IntentService.detect_intent(msg)
print(f'Message: {msg}')
print(f'Intent: {intent.value}')
"
```

Expected output:
```
Message: Need 200 titanium flanges by Friday
Intent: CREATE_ORDER
```

---

### Test Regex Extraction

```bash
python -c "
from utils.regex_utils import RegexUtils

msg = 'Order 5 with 200 steel brackets'
print(f'Order ID: {RegexUtils.extract_order_id(msg)}')
print(f'Quantity: {RegexUtils.extract_quantity(msg)}')
print(f'Material: {RegexUtils.extract_material(msg)}')
"
```

Expected output:
```
Order ID: 5
Quantity: 200
Material: Steel
```

---

### Test Response Generation

```bash
python -c "
from services.response_service import ResponseGenerator

mock_order = {'id': 1, 'part_name': 'Steel Bracket'}
response = ResponseGenerator.order_created_response(mock_order)

print(f'Type: {response[\"type\"]}')
print(f'Message: {response[\"message\"]}')
print(f'UI Hint: {response[\"ui_hint\"]}')
"
```

Expected output:
```
Type: ORDER_CREATED
Message: ✅ Manufacturing order #1 successfully registered.
UI Hint: success-glow
```

---

### Test AI Service

```bash
python -c "
from services.ai_service import AIService

ai = AIService()
result = ai.extract_order_data('Need 300 aluminum rods by Friday')
print(f'Part: {result.get(\"part_name\")}')
print(f'Material: {result.get(\"material\")}')
print(f'Quantity: {result.get(\"quantity\")}')
"
```

Expected output:
```
Part: Aluminum Rod
Material: Aluminum
Quantity: 300
```

---

## Success Checklist

After running `python test_person_b.py`:

- [ ] TEST 1: Intent Detection PASSED (8/8)
- [ ] TEST 2: Regex Utilities PASSED (4/4)
- [ ] TEST 3: Response Generation PASSED (5/5)
- [ ] TEST 4: AI Service PASSED (or SKIPPED if key issue)
- [ ] TEST 5: Integration Flow PASSED
- [ ] Final message: "🎉 ALL TESTS PASSED! Ready for integration."

---

## If All Tests Pass ✅

Commit and push:

```bash
cd c:\Users\Home\OneDrive\Desktop\nova-nexus

git add backend/

git commit -m "test: All Person B services verified and working"

git push origin backend-ai
```

**Now you're ready for Person A to build their part!** 🚀

---

## Need Help?

Check these in order:

1. **Is .env file valid?** 
   - `cat .env` should show your API key

2. **Are dependencies installed?**
   - `pip list` should show groq, python-dotenv

3. **Are you in correct directory?**
   - `pwd` should show `/backend`

4. **Does test file exist?**
   - `ls test_person_b.py` should find it

If still stuck, share the error message and we'll debug together!
