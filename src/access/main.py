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
    ),
    network_type: str = typer.Option(
        "drive",  # using drive here on purpuse
        "--network_type",
        "-n",
        help="from OSMnx: all, all_public, bike, drive, drive_service, walk",
    ),
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

    # Build Network
    bbox = get_bbox_wgs84(gdf)
    logger.info("Downloading desired network from bbox")
    graph = download_network(bbox=bbox, network_type=network_type)
    network = build_pandana_network(graph)

    print(network.node_ids)
    logger.info("---- Network built and working ----")


if __name__ == "__main__":
    app()
