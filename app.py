from models import Venue, setup_db

# from flask_moment import Moment
from flask_cors import CORS
from flask import Flask, Response, request, abort, jsonify

##### Settings #######

ITEMS_PER_PAGE = 10

def create_app():
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    def paginate(request,selection):
        page = request.args.get("page",1,type=int)
        start = (page-1)*ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE

        items = [item.format() for item in selection]

        return items[start:end]

    @app.route("/venues")
    def get_venues():

        venues = Venue.query.order_by(Venue.id).all()
        current_page = paginate(request, venues)

        return jsonify(
            {
                "success": True,
                "venues": current_page,
                "total_num_bikes": len(venues),
                "page": request.args.get("page", 1, type=int),
            }
        )

    return app

app = create_app()

    