from tables import *
from flask import render_template, Flask, request, jsonify
import os
import csv


app = Flask(__name__)

# Tell Flask what SQLAlchemy databas to use.
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# Link the Flask app with the database (no Flask app is actually being run yet).
db.init_app(app)

@app.route("/")
def submit():
    flights = Flight.query.all()
    return render_template("book_a_flight.html",flights=flights)

@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("id"))
    except ValueError:
        return render_template("error.html", message="Invalid flight number.")
    passenger = Passenger(name=name, flight_id=flight_id)
    db.session.add(passenger)
    db.session.commit()
    return render_template("submited.html", name = name)


@app.route("/detials")
def detials():
    flights = Flight.query.all()
    return render_template("detials.html", flights=flights)


@app.route('/flight_detials/<int:flight_id>')
def flight_detials(flight_id):
    flight = Flight.query.get(flight_id)
    passengers = Passenger.query.filter_by(flight_id=flight_id).all()
    return render_template("flight_detlials.html",flight =flight,passengers=passengers )




@app.route("/api/flight_detials/<int:flight_id>")
def flight_api(flight_id):
    """Return details about a single flight."""

    # Make sure flight exists.
    flight = Flight.query.get(flight_id)
    if flight is None:
        return jsonify({"error": "Invalid flight_id"}), 422
    passengers = db.relationship("Passenger", backref="flight", lazy=True)
    # Get all passengers.
    passengers = Passenger.query.filter_by(flight_id=flight_id).all()  #relationships means to add a modal to an object that instiated from another one by doting
    names = []
    for passenger in passengers:
        names.append(passenger.name)
    return jsonify({
        "origin": flight.origin,
        "destination": flight.destination,
        "duration": flight.duration,
        "passengers": names
    })
