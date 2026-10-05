from flask import Flask, render_template, request, redirect, url_for
from database import init_database, add_land, get_all_land_records
from datetime import date


app = Flask(__name__)


# Initialize database
init_database()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register-land", methods=["GET", "POST"])
def register_land():

    if request.method == "POST":

        owner_name = request.form["owner_name"]
        guardian_name = request.form["guardian_name"]
        survey_number = request.form["survey_number"]
        area = request.form["area"]
        land_type = request.form["land_type"]
        state = request.form["state"]
        district = request.form["district"]
        taluk = request.form["taluk"]
        village = request.form["village"]
        address = request.form["address"]
        registration_date = request.form["registration_date"]

        # Generate Land ID
        land_id = "LC-" + date.today().strftime("%Y") + "-" + survey_number.replace("/", "")

        add_land(
            land_id,
            owner_name,
            guardian_name,
            survey_number,
            area,
            land_type,
            state,
            district,
            taluk,
            village,
            address,
            registration_date
        )

        return redirect(url_for("land_records"))

    return render_template("register_land.html")


@app.route("/land-records")
def land_records():

    records = get_all_land_records()

    return render_template(
        "land_records.html",
        records=records
    )


if __name__ == "__main__":
    app.run(debug=True)