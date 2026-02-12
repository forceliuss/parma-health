from parma_health.primitives import mask_value


def test_mask_value_deterministic():
    """Verify that same input and salt produce same output."""
    val1 = mask_value("test_user", salt="salty")
    val2 = mask_value("test_user", salt="salty")
    assert val1 == val2
    assert isinstance(val1, str)
    assert len(val1) == 64  # SHA256 hex digest length


def test_mask_value_different_inputs():
    """Verify different inputs produce different outputs."""
    val1 = mask_value("user1", salt="salty")
    val2 = mask_value("user2", salt="salty")
    assert val1 != val2


def test_mask_value_different_salts():
    """Verify same input with different salts produce different outputs."""
    val1 = mask_value("user1", salt="salt_A")
    val2 = mask_value("user1", salt="salt_B")
    assert val1 != val2


def test_mask_value_none():
    """Verify None input returns None."""
    assert mask_value(None) is None


def test_mask_value_integers():
    """Verify non-string inputs are handled."""
    val = mask_value(12345, salt="salty")
    assert isinstance(val, str)
    assert len(val) == 64
