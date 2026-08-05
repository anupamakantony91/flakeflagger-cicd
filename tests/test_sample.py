# Sample test suite for FlakeFlagger CI/CD pipeline demo
# These represent typical tests in a real project

import time
import random

# ── STABLE TESTS (should not be flagged as flaky) ──

def test_addition():
    """Simple arithmetic - always passes"""
    assert 1 + 1 == 2

def test_string_operations():
    """String operations - always stable"""
    text = "flaky test detection"
    assert text.upper() == "FLAKY TEST DETECTION"
    assert len(text) == 20

def test_list_operations():
    """List operations - always stable"""
    items = [3, 1, 4, 1, 5, 9, 2, 6]
    assert sorted(items) == [1, 1, 2, 3, 4, 5, 6, 9]
    assert len(items) == 8

def test_dictionary_operations():
    """Dictionary operations - always stable"""
    data = {"project": "flakeflagger", "type": "research"}
    assert data["project"] == "flakeflagger"
    assert "type" in data

def test_boolean_logic():
    """Boolean logic - always stable"""
    assert True and True
    assert not False
    assert True or False

# ── POTENTIALLY FLAKY TESTS (timing dependent) ──

def test_execution_time_short():
    """Short execution - less likely flaky"""
    start = time.time()
    result = sum(range(100))
    end = time.time()
    assert result == 4950
    assert (end - start) < 1.0

def test_execution_time_medium():
    """Medium execution - moderate flaky risk"""
    start = time.time()
    result = sum(range(10000))
    end = time.time()
    assert result == 49995000
    assert (end - start) < 2.0

def test_execution_time_long():
    """Long execution - higher flaky risk"""
    start = time.time()
    time.sleep(0.1)
    end = time.time()
    assert (end - start) >= 0.1

def test_covers_many_operations():
    """Covers many operations - higher flaky risk"""
    results = []
    for i in range(1000):
        results.append(i * 2)
    assert len(results) == 1000
    assert results[0] == 0
    assert results[-1] == 1998

def test_string_formatting():
    """String formatting - stable"""
    name = "DevOps"
    result = f"Hello {name}, welcome to CI/CD!"
    assert "DevOps" in result
    assert result.startswith("Hello")