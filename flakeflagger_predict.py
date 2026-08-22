# ============================================
# FlakeFlagger CI/CD Detection Script
# Runs automatically inside GitHub Actions
# ============================================

import pandas as pd
import numpy as np
import joblib
import time
import json

print("=" * 55)
print("FlakeFlagger - CI/CD Flaky Test Detection")
print("=" * 55)

# ── LOAD MODEL ────────────────────────────────────
print("\n[1] Loading trained model...")
model = joblib.load('flakeflagger_model.pkl')
print("    Model loaded successfully")

# ── SIMULATE TEST FEATURES ────────────────────────
# In a real pipeline these features would be extracted
# from actual test execution results.
# Here we simulate realistic feature values for our
# sample test suite to demonstrate the pipeline.

print("\n[2] Reading test features...")

tests = [
    # Group 1 — Stable tests (low risk)
    {"test_name": "test_addition", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 1,
     "projectSourceLinesCovered": 5, "projectSourceClassesCovered": 1},
    {"test_name": "test_subtraction", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 1,
     "projectSourceLinesCovered": 5, "projectSourceClassesCovered": 1},
    {"test_name": "test_multiplication", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 1,
     "projectSourceLinesCovered": 5, "projectSourceClassesCovered": 1},
    {"test_name": "test_division", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 1,
     "projectSourceLinesCovered": 5, "projectSourceClassesCovered": 1},
    {"test_name": "test_modulo", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 1,
     "projectSourceLinesCovered": 5, "projectSourceClassesCovered": 1},
    {"test_name": "test_string_upper", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 2,
     "projectSourceLinesCovered": 8, "projectSourceClassesCovered": 1},
    {"test_name": "test_string_lower", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 2,
     "projectSourceLinesCovered": 8, "projectSourceClassesCovered": 1},
    {"test_name": "test_string_length", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 2,
     "projectSourceLinesCovered": 8, "projectSourceClassesCovered": 1},
    {"test_name": "test_string_contains", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 2,
     "projectSourceLinesCovered": 8, "projectSourceClassesCovered": 1},
    {"test_name": "test_string_split", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 2,
     "projectSourceLinesCovered": 8, "projectSourceClassesCovered": 1},
    {"test_name": "test_list_append", "ExecutionTime": 0.001,
     "testLength": 3, "numAsserts": 1, "numCoveredLines": 3,
     "projectSourceLinesCovered": 10, "projectSourceClassesCovered": 1},
    {"test_name": "test_list_remove", "ExecutionTime": 0.001,
     "testLength": 3, "numAsserts": 1, "numCoveredLines": 3,
     "projectSourceLinesCovered": 10, "projectSourceClassesCovered": 1},
    {"test_name": "test_list_sort", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 3,
     "projectSourceLinesCovered": 10, "projectSourceClassesCovered": 1},
    {"test_name": "test_list_length", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 2,
     "projectSourceLinesCovered": 8, "projectSourceClassesCovered": 1},
    {"test_name": "test_dict_access", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 2,
     "projectSourceLinesCovered": 8, "projectSourceClassesCovered": 1},
    {"test_name": "test_dict_keys", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 2,
     "projectSourceLinesCovered": 8, "projectSourceClassesCovered": 1},
    {"test_name": "test_boolean_and", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 1,
     "projectSourceLinesCovered": 5, "projectSourceClassesCovered": 1},
    {"test_name": "test_boolean_or", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 1,
     "projectSourceLinesCovered": 5, "projectSourceClassesCovered": 1},
    {"test_name": "test_boolean_not", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 1,
     "projectSourceLinesCovered": 5, "projectSourceClassesCovered": 1},
    {"test_name": "test_integer_type", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 1,
     "projectSourceLinesCovered": 5, "projectSourceClassesCovered": 1},
    {"test_name": "test_float_type", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 1,
     "projectSourceLinesCovered": 5, "projectSourceClassesCovered": 1},
    {"test_name": "test_string_type", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 1,
     "projectSourceLinesCovered": 5, "projectSourceClassesCovered": 1},
    {"test_name": "test_list_type", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 1,
     "projectSourceLinesCovered": 5, "projectSourceClassesCovered": 1},
    {"test_name": "test_dict_type", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 1,
     "projectSourceLinesCovered": 5, "projectSourceClassesCovered": 1},
    {"test_name": "test_math_sqrt", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 3,
     "projectSourceLinesCovered": 12, "projectSourceClassesCovered": 1},
    {"test_name": "test_math_pow", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 3,
     "projectSourceLinesCovered": 12, "projectSourceClassesCovered": 1},
    {"test_name": "test_math_floor", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 3,
     "projectSourceLinesCovered": 12, "projectSourceClassesCovered": 1},
    {"test_name": "test_math_ceil", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 3,
     "projectSourceLinesCovered": 12, "projectSourceClassesCovered": 1},
    {"test_name": "test_math_abs", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 2,
     "projectSourceLinesCovered": 8, "projectSourceClassesCovered": 1},
    {"test_name": "test_range_length", "ExecutionTime": 0.001,
     "testLength": 2, "numAsserts": 1, "numCoveredLines": 2,
     "projectSourceLinesCovered": 8, "projectSourceClassesCovered": 1},
    # Group 2 — Medium risk tests
    {"test_name": "test_list_comprehension", "ExecutionTime": 0.05,
     "testLength": 5, "numAsserts": 3, "numCoveredLines": 15,
     "projectSourceLinesCovered": 45, "projectSourceClassesCovered": 3},
    {"test_name": "test_nested_loops", "ExecutionTime": 0.08,
     "testLength": 6, "numAsserts": 1, "numCoveredLines": 20,
     "projectSourceLinesCovered": 60, "projectSourceClassesCovered": 3},
    {"test_name": "test_string_operations_medium", "ExecutionTime": 0.02,
     "testLength": 5, "numAsserts": 2, "numCoveredLines": 12,
     "projectSourceLinesCovered": 35, "projectSourceClassesCovered": 2},
    {"test_name": "test_dictionary_operations", "ExecutionTime": 0.05,
     "testLength": 6, "numAsserts": 2, "numCoveredLines": 18,
     "projectSourceLinesCovered": 50, "projectSourceClassesCovered": 3},
    {"test_name": "test_list_filter", "ExecutionTime": 0.03,
     "testLength": 4, "numAsserts": 1, "numCoveredLines": 10,
     "projectSourceLinesCovered": 30, "projectSourceClassesCovered": 2},
    {"test_name": "test_string_join", "ExecutionTime": 0.04,
     "testLength": 5, "numAsserts": 2, "numCoveredLines": 12,
     "projectSourceLinesCovered": 35, "projectSourceClassesCovered": 2},
    {"test_name": "test_math_operations", "ExecutionTime": 0.05,
     "testLength": 5, "numAsserts": 2, "numCoveredLines": 15,
     "projectSourceLinesCovered": 40, "projectSourceClassesCovered": 3},
    {"test_name": "test_set_operations", "ExecutionTime": 0.04,
     "testLength": 5, "numAsserts": 1, "numCoveredLines": 12,
     "projectSourceLinesCovered": 35, "projectSourceClassesCovered": 2},
    {"test_name": "test_tuple_operations", "ExecutionTime": 0.02,
     "testLength": 4, "numAsserts": 3, "numCoveredLines": 10,
     "projectSourceLinesCovered": 30, "projectSourceClassesCovered": 2},
    {"test_name": "test_sorted_large_list", "ExecutionTime": 0.10,
     "testLength": 6, "numAsserts": 2, "numCoveredLines": 20,
     "projectSourceLinesCovered": 55, "projectSourceClassesCovered": 3},
    # Group 3 — Higher risk tests (timing dependent)
    {"test_name": "test_execution_time_medium", "ExecutionTime": 0.85,
     "testLength": 7, "numAsserts": 2, "numCoveredLines": 40,
     "projectSourceLinesCovered": 180, "projectSourceClassesCovered": 8},
    {"test_name": "test_large_list_processing", "ExecutionTime": 1.20,
     "testLength": 6, "numAsserts": 1, "numCoveredLines": 55,
     "projectSourceLinesCovered": 220, "projectSourceClassesCovered": 9},
    {"test_name": "test_string_manipulation_large", "ExecutionTime": 0.95,
     "testLength": 6, "numAsserts": 1, "numCoveredLines": 45,
     "projectSourceLinesCovered": 190, "projectSourceClassesCovered": 8},
    {"test_name": "test_nested_dict_operations", "ExecutionTime": 1.50,
     "testLength": 8, "numAsserts": 2, "numCoveredLines": 65,
     "projectSourceLinesCovered": 280, "projectSourceClassesCovered": 12},
    {"test_name": "test_recursive_computation", "ExecutionTime": 2.10,
     "testLength": 7, "numAsserts": 1, "numCoveredLines": 70,
     "projectSourceLinesCovered": 310, "projectSourceClassesCovered": 14},
    {"test_name": "test_multiple_iterations", "ExecutionTime": 1.80,
     "testLength": 6, "numAsserts": 1, "numCoveredLines": 60,
     "projectSourceLinesCovered": 260, "projectSourceClassesCovered": 11},
    {"test_name": "test_string_search_large", "ExecutionTime": 1.30,
     "testLength": 6, "numAsserts": 2, "numCoveredLines": 55,
     "projectSourceLinesCovered": 230, "projectSourceClassesCovered": 10},
    {"test_name": "test_list_operations_large", "ExecutionTime": 1.60,
     "testLength": 7, "numAsserts": 4, "numCoveredLines": 65,
     "projectSourceLinesCovered": 270, "projectSourceClassesCovered": 12},
    {"test_name": "test_execution_time_with_sleep", "ExecutionTime": 2.50,
     "testLength": 6, "numAsserts": 2, "numCoveredLines": 85,
     "projectSourceLinesCovered": 420, "projectSourceClassesCovered": 18},
        {"test_name": "test_covers_many_modules", "ExecutionTime": 1.80,
     "testLength": 9, "numAsserts": 5, "numCoveredLines": 90,
     "projectSourceLinesCovered": 450, "projectSourceClassesCovered": 20},
         # Flaky test simulation — exact feature values that produce
    # 100% flaky prediction from the trained model
    # Based on real flaky test from logback project (Bell et al. 2021)
    {"test_name": "test_flaky_simulation",
     "ExecutionTime": 0.146,
     "testLength": 19.0,
     "numAsserts": 3.0,
     "numCoveredLines": 22.0,
     "projectSourceLinesCovered": 90.0,
     "projectSourceClassesCovered": 33.0,
     "assertion-roulette": 1.0,
     "conditional-test-logic": 0.0,
     "eager-test": 0.0,
     "fire-and-forget": 0.0,
     "indirect-testing": 1.0,
     "mystery-guest": 0.0,
     "resource-optimism": 0.0,
     "test-run-war": 0.0,
     "hIndexModificationsPerCoveredLine_window5": 0.0,
     "hIndexModificationsPerCoveredLine_window10": 0.0,
     "hIndexModificationsPerCoveredLine_window25": 0.0,
     "hIndexModificationsPerCoveredLine_window50": 0.0,
     "hIndexModificationsPerCoveredLine_window75": 0.0,
     "hIndexModificationsPerCoveredLine_window100": 0.0,
     "hIndexModificationsPerCoveredLine_window500": 2.0,
     "hIndexModificationsPerCoveredLine_window10000": 4.0,
     "num_third_party_libs": 3.0},
]

# Fill missing features with 0
for col in feature_cols:
    if col not in df.columns:
        df[col] = 0

X = df[feature_cols]

# ── PREDICT ───────────────────────────────────────
print(f"\n[3] Running FlakeFlagger on {len(X)} tests...")
start = time.time()
predictions = model.predict(X)
probabilities = model.predict_proba(X)
elapsed = time.time() - start

print(f"    Prediction completed in {elapsed*1000:.2f}ms")
print(f"    Time per test: {(elapsed/len(X))*1000:.4f}ms")

# ── REPORT ────────────────────────────────────────
print("\n[4] FlakeFlagger Detection Report:")
print("-" * 55)
print(f"{'Test Name':<35} {'Risk':>6} {'Status':>12}")
print("-" * 55)

flaky_count = 0
results = []

for i, (name, pred, prob) in enumerate(
        zip(test_names, predictions, probabilities)):
    flaky_prob = prob[1] * 100
    status = "⚠ LIKELY FLAKY" if pred == 1 else "✓ STABLE"
    if pred == 1:
        flaky_count += 1
    print(f"{name:<35} {flaky_prob:>5.1f}% {status:>14}")
    results.append({
        "test": name,
        "flaky_probability": round(flaky_prob, 2),
        "prediction": "FLAKY" if pred == 1 else "STABLE"
    })

print("-" * 55)
print(f"\nSummary:")
print(f"  Total tests analysed: {len(X)}")
print(f"  Likely flaky:         {flaky_count}")
print(f"  Stable:               {len(X) - flaky_count}")
print(f"  Detection time:       {elapsed*1000:.2f}ms")

# Save results to JSON for pipeline artifacts
with open('flakeflagger_report.json', 'w') as f:
    json.dump({
        "summary": {
            "total_tests": len(X),
            "flaky_detected": flaky_count,
            "stable": len(X) - flaky_count,
            "detection_time_ms": round(elapsed * 1000, 2)
        },
        "results": results
    }, f, indent=2)

print("\n    Report saved as: flakeflagger_report.json")
print("\n" + "=" * 55)
if flaky_count > 0:
    print(f"⚠  WARNING: {flaky_count} likely flaky test(s) detected!")
    print("   Investigate these before merging.")
else:
    print("✓  All tests appear stable. Safe to merge.")
print("=" * 55)