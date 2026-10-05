from flask import Flask, render_template, request, redirect, url_for
from database import (
    init_database,
    add_land,
    get_all_land_records,
    delete_land,
    update_land
)
from blockchain.blockchain import Blockchain
from datetime import date, datetime


app = Flask(__name__)

blockchain = Blockchain()

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

        timestamp = int(datetime.now().timestamp())

        land_id = (
            "LC-"
            + date.today().strftime("%Y")
            + "-"
            + survey_number.replace("/", "")
            + "-"
            + str(timestamp)
        )

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

        blockchain.add_block({
            "type": "Land Registration",
            "land_id": land_id,
            "owner_name": owner_name,
            "guardian_name": guardian_name,
            "survey_number": survey_number,
            "area": area,
            "land_type": land_type,
            "state": state,
            "district": district,
            "taluk": taluk,
            "village": village,
            "address": address,
            "registration_date": registration_date
        })

        return redirect(url_for("land_records"))

    return render_template("register_land.html")


@app.route("/land-records")
def land_records():

    records = get_all_land_records()

    return render_template(
        "land_records.html",
        records=records
    )


@app.route("/delete-land/<land_id>", methods=["POST"])
def delete_land_record(land_id):

    delete_land(land_id)

    return redirect(url_for("land_records"))


@app.route("/edit-land/<land_id>", methods=["GET", "POST"])
def edit_land(land_id):

    records = get_all_land_records()

    record = None

    for item in records:
        if item["land_id"] == land_id:
            record = item
            break

    if record is None:
        return "Land record not found", 404

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

        update_land(
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

        blockchain.add_block({
            "type": "Land Record Updated",
            "land_id": land_id,
            "owner_name": owner_name,
            "survey_number": survey_number,
            "updated_at": str(datetime.now())
        })

        return redirect(url_for("land_records"))

    return render_template(
        "edit_land.html",
        record=record
    )


@app.route("/blockchain")
def blockchain_explorer():

    chain = blockchain.get_chain()

    return render_template(
        "blockchain.html",
        chain=chain,
        valid=blockchain.is_chain_valid()
    )


if __name__ == "__main__":
    app.run(debug=True)