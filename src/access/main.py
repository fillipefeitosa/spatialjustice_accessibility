import logging
import sys
import typer
from access.io import load_database

from access.network import get_bbox_wgs84, build_pandana_network, download_network

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
    )
):
    """
    Who can reach what? \n
    Urban accessibility analysis
    for spatial justice.

    Loads a GeoJSON layer and computes network-based accessibility metrics
    to reveal structural inequalities in urban access.
    """
    logger.info("Social Access. Starting Execution")
    gdf = load_database(filename)
    logger.info("Loaded: %s features", gdf.shape[0])


if __name__ == "__main__":
    app()
