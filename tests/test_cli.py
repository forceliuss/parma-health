import pytest
from click.testing import CliRunner
from parma_health.cli import main
import pandas as pd
import os


@pytest.fixture
def runner():
    return CliRunner()


def test_hello_command(runner):
    """Verify hello command works."""
    result = runner.invoke(main, ['hello'])
    assert result.exit_code == 0
    assert "Hello from Parma Health Toolkit!" in result.output


def test_run_command_csv(runner, tmp_path):
    """Verify run command processes CSV files correctly."""
    # Setup inputs
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    df = pd.DataFrame({'id': [1, 2, 3], 'name': ['alice', 'bob', 'charlie']})
    df.to_csv(input_file, index=False)

    # Run command
    result = runner.invoke(main, [
        'run',
        '--source', str(input_file),
        '--destination', str(output_file)
    ])

    # Verify success
    assert result.exit_code == 0
    assert "Processing" in result.output
    assert "Done!" in result.output

    # Verify output file content
    assert os.path.exists(output_file)
    result_df = pd.read_csv(output_file)
    pd.testing.assert_frame_equal(df, result_df)


def test_run_command_invalid_extension(runner, tmp_path):
    """Verify error for unsupported file extensions."""
    input_file = tmp_path / "input.txt"
    input_file.write_text("dummy content")

    result = runner.invoke(main, ['run', '--source', str(input_file)])

    assert "Error: Unsupported file type .txt" in result.output


def test_run_command_missing_file(runner):
    """
    Verify click handles missing files (via type=click.Path(exists=True)).
    """
    result = runner.invoke(main, ['run', '--source', 'nonexistent.csv'])

    assert result.exit_code != 0
    assert "Error" in result.output
