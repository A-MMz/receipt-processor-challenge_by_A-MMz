from flask import Flask, request, jsonify
import uuid
import math

app = Flask(__name__)

# In-memory database for storing receipts and points
receipts_db = {}

def calculate_points(receipt):
    points = 0

    # Rule 1: One point for every alphanumeric character in the retailer name
    alphanumeric_count = 0
    for char in receipt["retailer"]:
        if char.isalnum():
            alphanumeric_count += 1
    points += alphanumeric_count

    # Rule 2: 50 points if the total is a round dollar amount with no cents
    if float(receipt["total"]) == int(float(receipt["total"])):
        points += 50

    # Rule 3: 25 points if the total is a multiple of 0.25
    if float(receipt["total"]) % 0.25 == 0:
        points += 25

    # Rule 4: 5 points for every two items on the receipt
    points += (len(receipt["items"]) // 2) * 5

    # Rule 5: Points for items' description and price
    for item in receipt["items"]:
        if len(item["shortDescription"].strip()) % 3 == 0:
            item_points = math.ceil(float(item["price"]) * 0.2)
            points += item_points

    # Rule 6: 6 points if the day in the purchase date is odd
    day = int(receipt["purchaseDate"].split("-")[2])
    if day % 2 != 0:
        points += 6

    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm
    time = receipt["purchaseTime"].split(":")
    hour = int(time[0])
    if 14 <= hour < 16:
        points += 10

    return points

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    receipt = request.json
    receipt_id = str(uuid.uuid4())
    points = calculate_points(receipt)
    receipts_db[receipt_id] = {
        "receipt": receipt,
        "points": points
    }
    return jsonify({"id": receipt_id}), 200

@app.route('/receipts/<id>/points', methods=['GET'])
def get_points(id):
    return jsonify({"points": receipts_db[id]["points"]}), 200

if __name__ == "__main__":
    app.run(debug=True)
