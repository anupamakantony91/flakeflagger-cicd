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
    {
        "test_name": "test_addition",
        "ExecutionTime": 0.001,
        "testLength": 3,
        "numAsserts": 1,
        "numCoveredLines": 2,
        "projectSourceLinesCovered": 10,
        "projectSourceClassesCovered": 1,
    },
    {
        "test_name": "test_string_operations",
        "ExecutionTime": 0.002,
        "testLength": 5,
        "numAsserts": 2,
        "numCoveredLines": 5,
        "projectSourceLinesCovered": 15,
        "projectSourceClassesCovered": 2,
    },
    {
        "test_name": "test_execution_time_long",
        "ExecutionTime": 2.500,
        "testLength": 45,
        "numAsserts": 1,
        "numCoveredLines": 85,
        "projectSourceLinesCovered": 420,
        "projectSourceClassesCovered": 18,
    },
    {
        "test_name": "test_covers_many_operations",
        "ExecutionTime": 1.800,
        "testLength": 38,
        "numAsserts": 3,
        "numCoveredLines": 72,
        "projectSourceLinesCovered": 380,
        "projectSourceClassesCovered": 15,
    },
    {
        "test_name": "test_execution_time_medium",
        "ExecutionTime": 0.850,
        "testLength": 20,
        "numAsserts": 2,
        "numCoveredLines": 40,
        "projectSourceLinesCovered": 180,
        "projectSourceClassesCovered": 8,
    },
    {
        "test_name": "test_boolean_logic",
        "ExecutionTime": 0.001,
        "testLength": 4,
        "numAsserts": 3,
        "numCoveredLines": 3,
        "projectSourceLinesCovered": 8,
        "projectSourceClassesCovered": 1,
    },
    {
        "test_name": "test_list_operations",
        "ExecutionTime": 0.003,
        "testLength": 6,
        "numAsserts": 2,
        "numCoveredLines": 6,
        "projectSourceLinesCovered": 20,
        "projectSourceClassesCovered": 2,
    },
    {
        "test_name": "test_dictionary_operations",
        "ExecutionTime": 0.002,
        "testLength": 5,
        "numAsserts": 2,
        "numCoveredLines": 4,
        "projectSourceLinesCovered": 12,
        "projectSourceClassesCovered": 1,
    },
    {
        "test_name": "test_execution_time_short",
        "ExecutionTime": 0.050,
        "testLength": 10,
        "numAsserts": 2,
        "numCoveredLines": 15,
        "projectSourceLinesCovered": 45,
        "projectSourceClassesCovered": 3,
    },
    {
        "test_name": "test_string_formatting",
        "ExecutionTime": 0.001,
        "testLength": 5,
        "numAsserts": 2,
        "numCoveredLines": 3,
        "projectSourceLinesCovered": 10,
        "projectSourceClassesCovered": 1,
    },
]

df = pd.DataFrame(tests)
test_names = df['test_name'].tolist()

# ── PREPARE FEATURES ──────────────────────────────
# Match the features the model was trained on
feature_cols = [
    'assertion-roulette', 'conditional-test-logic',
    'eager-test', 'fire-and-forget', 'indirect-testing',
    'mystery-guest', 'resource-optimism', 'test-run-war',
    'testLength', 'numAsserts', 'numCoveredLines',
    'ExecutionTime', 'projectSourceLinesCovered',
    'projectSourceClassesCovered',
    'hIndexModificationsPerCoveredLine_window5',
    'hIndexModificationsPerCoveredLine_window10',
    'hIndexModificationsPerCoveredLine_window25',
    'hIndexModificationsPerCoveredLine_window50',
    'hIndexModificationsPerCoveredLine_window75',
    'hIndexModificationsPerCoveredLine_window100',
    'hIndexModificationsPerCoveredLine_window500',
    'hIndexModificationsPerCoveredLine_window10000',
    'num_third_party_libs'
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