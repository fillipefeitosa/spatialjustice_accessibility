import logging
import pandana
import pandas as pd
import geopandas as gpd
import osmnx as ox

logger = logging.getLogger(__name__)

# TODO: function to download network by name


def get_bbox_wgs84(gdf: gpd.GeoDataFrame) -> tuple:
    """
    Converts the GeoDataFrame extent to WGS84 and returns
    the bounding box as (west, south, east, north).

    osmnx requires lat/lon coordinates — we convert here
    once and reuse the result for all OSM downloads.
    The GeoDataFrame itself stays in EPSG:25832.

    Args:
        gdf: GeoDataFrame in any projected CRS

    Returns:
        (west, south, east, north) in decimal degrees
    """
    gdf_wgs84 = gdf.to_crs(epsg=4326)
    west, south, east, north = gdf_wgs84.total_bounds
    logger.info(f"Bounding box — W:{west:.4f} S:{south:.4f} E:{east:.4f} N:{north:.4f}")
    return west, south, east, north


def download_network(bbox: tuple, network_type: str = "walk"):
    """
    Downloads the OSM street network for the bounding box.

    Args:
        bbox:         (north, south, east, west) in WGS84
        network_type: 'walk', 'drive', or 'bike'

    Returns:
        osmnx MultiDiGraph
    """
    print(f"Downloading OSM {network_type} network...")
    graph = ox.graph_from_bbox(bbox, network_type=network_type)
    logger.info(
        "Network ready — %s nodes, %s edges", len(graph.nodes), len(graph.edges)
    )
    return graph


def build_pandana_network(graph) -> pandana.Network:
    """
    Converts an osmnx graph to a pandana Network.
    Edge weights are lengths in meters as computed by osmnx.

    Args:
        graph: osmnx MultiDiGraph

    Returns:
        pandana.Network ready for accessibility queries
    """
    nodes, edges = ox.graph_to_gdfs(graph, nodes=True, edges=True)

    edge_from = pd.Series(edges.index.get_level_values("u").values)
    edge_to = pd.Series(edges.index.get_level_values("v").values)
    edge_weights = pd.DataFrame({"distance": edges["length"].values})

    network = pandana.Network(
        node_x=nodes["x"],
        node_y=nodes["y"],
        edge_from=edge_from,
        edge_to=edge_to,
        edge_weights=edge_weights,
        twoway=False,
    )
    logging.info("Pandana network ready — %s nodes", len(nodes))
    return network
