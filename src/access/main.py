import logging
import sys
import typer
from access.io import load_database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def main(
    filename: str = typer.Option(
        "data.geojson",
        "--input",
        "-i",
        help="GeoJSON filename inside the data/ folder.",
    ),
):
    """
    Who Can Reach What — Urban accessibility analysis for spatial justice.

    Loads a GeoJSON layer and computes network-based accessibility metrics
    to reveal structural inequalities in urban access.
    """
    logger.info("Social Access. Starting Execution")
    gdf = load_database(filename)
    logger.info(f"Loaded: {gdf.shape[0]} features")


if __name__ == "__main__":
    app()