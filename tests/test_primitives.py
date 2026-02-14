from parma_health.primitives import (
    hash_sha256,
    mask_value,
    pseudonymize_value
)


def test_hash_sha256_deterministic():
    """Verify that same input and salt produce same output."""
    val1 = hash_sha256("test_user", salt="salty")
    val2 = hash_sha256("test_user", salt="salty")
    assert val1 == val2
    assert isinstance(val1, str)
    assert len(val1) == 64  # SHA256 hex digest length


def test_hash_alias_consistency():
    """Verify aliases point to the same logic."""
    val = "test_value"
    salt = "test_salt"
    h1 = hash_sha256(val, salt)
    h2 = mask_value(val, salt)
    h3 = pseudonymize_value(val, salt)
    assert h1 == h2 == h3


def test_hash_sha256_different_inputs():
    """Verify different inputs produce different outputs."""
    val1 = hash_sha256("user1", salt="salty")
    val2 = hash_sha256("user2", salt="salty")
    assert val1 != val2


def test_hash_sha256_different_salts():
    """Verify same input with different salts produce different outputs."""
    val1 = hash_sha256("user1", salt="salt_A")
    val2 = hash_sha256("user1", salt="salt_B")
    assert val1 != val2


def test_hash_sha256_none():
    """Verify None input returns None."""
    assert hash_sha256(None) is None


def test_hash_sha256_integers():
    """Verify non-string inputs are handled."""
    val = hash_sha256(12345, salt="salty")
    assert isinstance(val, str)
    assert len(val) == 64
