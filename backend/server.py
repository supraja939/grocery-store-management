from flask import Flask, request, jsonify
from flask_cors import CORS
from sql_connection import get_sql_connection
import products_dao
import orders_dao
import users_dao


app = Flask(__name__)
CORS(app)   # 🔥 This enables OPTIONS + DELETE + POST automatically

connection = get_sql_connection()

@app.route("/getProducts", methods=["GET"])
def get_products():
    return jsonify(products_dao.get_all_products(connection))


@app.route("/insertProduct", methods=["POST"])
def insert_product():
    data = request.get_json()
    result = products_dao.insert_new_product(connection, data)

    if result == "exists":
        return jsonify({"message": "Product already exists"}), 400

    if result == "reactivated":
        return jsonify({"message": "Product reactivated"}), 200

    return jsonify({"message": "Product created"}), 201




@app.route("/deleteProduct/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    print("Deleting:", product_id)
    products_dao.delete_product(connection, product_id)
    return jsonify({"message": "Deleted"}), 200


@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = request.get_json()
    order_id = orders_dao.insert_order(connection, request_payload)

    response = jsonify({
        'order_id': order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



@app.route("/getOrders", methods=["GET"])
def get_orders():
    return jsonify(orders_dao.get_all_orders(connection))



@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = users_dao.validate_user(
        connection,
        data["username"],
        data["password"]
    )

    if user:
        return jsonify({"message": "success"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401



if __name__ == "__main__":
    app.run(debug=True)
