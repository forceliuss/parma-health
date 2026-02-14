import pytest
import pandas as pd
from parma_health.anonymizer import (
    Anonymizer,
    AnonymizerConfig,
    AnonymizationRule
)
from parma_health.primitives import (
    mask_value,
    pseudonymize_value
)


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'name': ['Alice', 'Bob'],
        'age': [30, 25],
        'email': ['alice@example.com', 'bob@example.com']
    })


def test_suppress_rule(sample_df):
    """Verify 'suppress' action drops the column."""
    config = AnonymizerConfig(rules=[
        AnonymizationRule(field='email', action='suppress')
    ])
    engine = Anonymizer(config)

    result = engine.process_chunk(sample_df)

    assert 'email' not in result.columns
    assert 'name' in result.columns
    assert len(result) == 2


def test_mask_rule(sample_df):
    """Verify 'mask' action replaces values."""
    config = AnonymizerConfig(rules=[
        AnonymizationRule(field='name', action='mask')
    ])
    engine = Anonymizer(config)

    result = engine.process_chunk(sample_df)

    # Calculate expected hash for 'Alice' using default salt
    expected_hash = mask_value("Alice", salt="default_salt")
    assert result['name'][0] == expected_hash
    assert result['age'].equals(sample_df['age'])


def test_multiple_rules(sample_df):
    """Verify applying multiple rules sequentially."""
    config = AnonymizerConfig(rules=[
        AnonymizationRule(field='name', action='mask'),
        AnonymizationRule(field='email', action='suppress')
    ])
    engine = Anonymizer(config)

    result = engine.process_chunk(sample_df)

    expected_hash = mask_value("Alice", salt="default_salt")
    assert result['name'][0] == expected_hash
    assert 'email' not in result.columns
    assert 'age' in result.columns


def test_unknown_field_ignored(sample_df):
    """Verify rules for fields not in DF are ignored."""
    config = AnonymizerConfig(rules=[
        AnonymizationRule(field='nonexistent', action='mask')
    ])
    engine = Anonymizer(config)

    result = engine.process_chunk(sample_df)

    pd.testing.assert_frame_equal(result, sample_df)


def test_mask_rule_custom_salt(sample_df):
    """Verify 'mask' action uses custom salt from rule params."""
    config = AnonymizerConfig(rules=[
        AnonymizationRule(
            field='name',
            action='mask',
            params={'salt': 'custom_salt'}
        )
    ])
    engine = Anonymizer(config)

    result = engine.process_chunk(sample_df)

    # Calculate expected hash using custom salt
    expected_hash = mask_value("Alice", salt="custom_salt")
    assert result['name'][0] == expected_hash
    # Ensure it's different from default salt
    assert result['name'][0] != mask_value("Alice", salt="default_salt")


def test_pseudonymize_rule(sample_df):
    """Verify 'pseudonymize' action uses hashing logic."""
    config = AnonymizerConfig(rules=[
        AnonymizationRule(field='name', action='pseudonymize')
    ])
    engine = Anonymizer(config)

    result = engine.process_chunk(sample_df)

    expected_hash = pseudonymize_value("Alice", salt="default_salt")
    assert result['name'][0] == expected_hash
    assert result['age'].equals(sample_df['age'])
