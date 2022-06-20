from . import bp as api
from flask import jsonify

@api.route('/', methods=["GET"])
def test():
    return jsonify({'success': True})