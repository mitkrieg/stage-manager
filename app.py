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
                "total_num_venues": len(venues),
                "page": request.args.get("page", 1, type=int),
            }
        )

    @app.route("/venues", methods=["POST"])
    def create_venue():
        print('working')
        body = request.get_json()

        try:
            name = body.get("name",None)
            capacity = body.get('capacity',None)
            style = body.get('style',None)

            print(name,capacity,style)

            

            venue = Venue(
                name=name,
                capacity=capacity,
                style=style
            )

            print(venue)

            venue.insert()

            print('returning')

            return jsonify({
                "success":True,
                "created_venue_id":venue.id
            })
        except Exception as e:
            print(e)
            abort(400)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
                "success":False,
                "error":400
            })
        


        

    return app

app = create_app()

    