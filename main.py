from PIL import Image
from pathlib import Path
from flask import Flask, request, send_file

app = Flask(__name__)

# Static directory where your map tiles are stored
TILE_DIRECTORY = './tiles/'
TRANSPARENT_TILE = Path(TILE_DIRECTORY, "transparent.png")

@app.route('/wmts', methods=['GET'])
def wmts_service():
    """
    Main entry point for WMTS service, handles GetTile.
    """
    service_request = request.args.get('request')
    if service_request == 'GetTile':
        return get_tile()
    else:
        return "Invalid WMTS request", 400


@app.route('/legend', methods=['GET'])
def legend_service():
    """
    Main entry point for legend service.
    Example URL: /legend?layer=bathy
    """
    layer = request.args.get('layer')

    if layer not in ["bathy", "predictions"]:
        return "Invalid legend request", 400

    legend_file = Path(TILE_DIRECTORY, layer, "gradient.png")

    if not legend_file.exists() or not legend_file.is_file():
        return "Tile not found", 404

    return send_file(legend_file, mimetype='image/png')

@app.errorhandler(404)
def page_not_found(e):
    # your processing here
    print(e, request)
    return "Request not found or not handled", 404


def get_tile():
    """
    Serves the requested tile (based on Layer, TileMatrix, TileRow, TileCol).
    Example URL: /wmts?request=GetTile&layer=ortho&tilematrix={z}&tilerow={x}&tilecol={y}
    Example URL: /wmts?request=GetTile&layer=ortho&year=2023&tilematrix={z}&tilerow={x}&tilecol={y}
    Example URL: /wmts?request=GetTile&layer=bathy&tilematrix={z}&tilerow={x}&tilecol={y}
    Example URL: /wmts?request=GetTile&layer=predictions&tilematrix={z}&tilerow={x}&tilecol={y}
    """

    layer = request.args.get('layer')
    year = request.args.get('year', 'all') # If year is not in arguments, return all tif merged.
    tile_matrix = request.args.get('tilematrix')
    tile_row = request.args.get('tilerow')
    tile_col = request.args.get('tilecol')

    tile_col = str(2**(int(tile_matrix)) - int(tile_col) -1) # TMS tiles are flip compared with XYZ tiles

    if not (tile_matrix and tile_row and tile_col):
        return "Missing parameters", 400

    tile_path = Path(TILE_DIRECTORY, layer, year, tile_matrix, tile_row, f"{tile_col}.png")
    if tile_path.exists():
        return send_file(tile_path, mimetype='image/png')
    else:
        if not TRANSPARENT_TILE.exists():
            generate_transparent_tile()
        return send_file(TRANSPARENT_TILE, mimetype='image/png')


def generate_transparent_tile():
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    img.save(TRANSPARENT_TILE, format="PNG")


if __name__ == '__main__':
    # Run the Flask server
    app.run(port=5004, debug=True)