import click
import os
from parma_health.connectors import CSVConnector


@click.group()
@click.version_option()
def main():
    """Parma Health Toolkit CLI"""
    pass


@main.command()
def hello():
    """Test command"""
    click.echo("Hello from Parma Health Toolkit!")


@main.command()
@click.option(
    '--source',
    required=True,
    type=click.Path(exists=True),
    help='Path to input file'
)
@click.option(
    '--destination',
    default='output.csv',
    help='Path to output file'
)
def run(source, destination):
    """
    Run the anonymization pipeline.
    Currently supports: CSV passthrough (read -> write).
    """
    click.echo(f"Processing {source} -> {destination}")

    # Determine file type (simple extension check for now)
    _, ext = os.path.splitext(source)
    if ext.lower() != '.csv':
        click.echo(
            f"Error: Unsupported file type {ext}. Only .csv is supported.",
            err=True
        )
        return

    try:
        # Initialize connectors
        source_connector = CSVConnector(source)
        dest_connector = CSVConnector(destination)

        # Execute pipeline (Stream: Read -> Write)
        click.echo("Reading and writing data...")
        data_stream = source_connector.read()
        dest_connector.write(data_stream)

        click.echo("Done!")

    except Exception as e:
        click.echo(f"Error processing file: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()
