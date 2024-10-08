from pathlib import Path
from flask import Flask, request, send_file

app = Flask(__name__)

# Static directory where your map tiles are stored
TILE_DIRECTORY = './tiles'

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

@app.errorhandler(404)
def page_not_found(e):
    # your processing here
    print(e, request)
    return "Request not found or not handled", 404

def get_tile():
    """
    Serves the requested tile (based on TileMatrix, TileRow, TileCol).
    Example URL: /wmts?request=GetTile&tilematrix=2&tilerow=1&tilecol=1
    Example URL: /wmts?request=GetTile&tilematrix={z}&tilerow={x}&tilecol={y}
    """
    tile_matrix = request.args.get('tilematrix')
    tile_row = request.args.get('tilerow')
    tile_col = request.args.get('tilecol')

    tile_col = str(2**(int(tile_matrix)) - int(tile_col) -1) # TMS tiles are flip compared with XYZ tiles

    if not (tile_matrix and tile_row and tile_col):
        return "Missing parameters", 400

    tile_path = Path(TILE_DIRECTORY, tile_matrix, tile_row, f"{tile_col}.png")

    if tile_path.exists():
        return send_file(tile_path, mimetype='image/png')
    else:
        return "Tile not found", 404

if __name__ == '__main__':
    # Run the Flask server
    app.run(port=5004, debug=True)