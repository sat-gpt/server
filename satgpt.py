import traceback
import openai
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from ln import add_invoice, lookup_invoice
from db.db import (
    add_user_uuid,
    check_invoice_used,
    create_invoices_table,
    create_users_table,
    lookup_user_by_r_hash,
    lookup_user_credit,
    set_invoice_used,
    add_r_hash_and_query,
    lookup_query,
    set_user_credit,
)
from util import price, base64_to_hex

# Load env vars
load_dotenv(verbose=True, dotenv_path=".env", override=True)
# Set up the OpenAI API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up the Flask app
app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

# TODO: rename from "query" to be more generic, since
# invoices can be generated for other reasons ("e.g. /add-credit")
def generate_invoice(query, amount=None):
    if not amount:
        amount = price(query)
    result = add_invoice(amount, f"{query[:20]}...")
    # result contains the payment request and the r_hash
    return result

def check_payment(r_hash):
    invoice = lookup_invoice(r_hash)
    paid = invoice["settled"]
    return (paid, invoice)

# TODO: how can we integrate check-payment into the query endpoint?
# how does /query know that check_payment has been paid?
# @app.route('/check-payment', methods=['POST'])
# def check_payment():
#     try:
#         data = request.get_json()

#         if "r_hash" not in data:
#             response = jsonify({"message": "No query provided"})
#             return response, 400

#         r_hash = data["r_hash"]
#         (paid, invoice) = check_payment(r_hash)
#         if paid:
#             if check_invoice_used(r_hash):
#                 response = jsonify({"message": "Payment already used"})
#                 # What's a good error code that's not an error but doesn't return a response?
#                 # A neutral code?
#                 return response, 200
#             else:
#                 set_invoice_used(r_hash)
#                 # deduct credit from user
#                 user_uuid = lookup_user_by_r_hash(r_hash)
#                 amount = lookup_invoice(r_hash)["value"]
#                 set_user_credit(user_uuid, amount, deduct=True)

#             response = jsonify({"message": "Payment successful"})
#             return response, 200
#         else:
#             response = jsonify(
#                 {
#                     "message": "Payment Required",
#                     "payment_request": invoice["payment_request"],
#                     "memo": invoice["memo"],
#                 }
#             )
#             return response, 402
#     except Exception as e:
#         # Return an error response if an exception occurs
#         error_message = f"An error occurred: {str(e)}"
#         traceback.print_exc()  # Optional: Print the traceback for debugging purposes
#         response = {"error": error_message}
#         return jsonify(response)    

@app.route("/query", methods=["POST"])
def query_chatbot():
    try:
        # Parse the request data
        data = request.get_json()

        # if query is not in data, return error
        if "query" and "user_uuid" not in data and "r_hash" not in data:
            response = jsonify({"message": "No query provided"})
            return response, 400

        # check if we're in the middle of a payment
        if "r_hash" in data:
            r_hash = data["r_hash"]
            (paid, invoice) = check_payment(r_hash)
            if paid:
                # Check that the invoice hasn't been used before
                if check_invoice_used(r_hash):
                    # Return the response to the client
                    # What's a good error code that's not an error but doesn't return a response?
                    # A neutral code?
                    response = jsonify({"message": "Payment already used"})
                    return response, 200
                else:
                    # mark invoice as used
                    set_invoice_used(r_hash)
                    # deduct credit from user
                    user_uuid = lookup_user_by_r_hash(r_hash)
                    amount = lookup_invoice(r_hash)["value"]
                    set_user_credit(user_uuid, amount, deduct=True)

                # lookup the query associated with the r_hash
                query = lookup_query(r_hash)

                # check if model is specified
                if "model_selected" in data:
                    gpt_model = data["model_selected"]
                else:
                    gpt_model = "gpt-3.5-turbo"

                # Call the OpenAI API to generate a response
                # completion = openai.ChatCompletion.create(
                #     model= gpt_model, messages=[{"role": "user", "content": query}]
                # )

                # Extract the response text from the API response
                # message = completion.choices[0].message.content.strip()
                message = "This is a test message"

                response = jsonify({"message": message})
                return response, 200
            else:
                response = jsonify(
                    {
                        "message": "Payment Required",
                        "payment_request": invoice["payment_request"],
                        "memo": invoice["memo"],
                    }
                )
                return response, 402
        else:
            # If r_hash isn't in request, generate an invoice
            query = data["query"]
            user_uuid = data["user_uuid"]
            # generate an invoice
            invoice = generate_invoice(query)
            # convert r_hash from base64 to hex because for some reason LND returns it in base64
            r_hash = base64_to_hex(invoice["r_hash"])
            # add r_hash and query to database
            add_r_hash_and_query(r_hash, query, user_uuid)
            response = jsonify({
                "message": "Payment Required",
                "invoice": invoice["payment_request"],
                "r_hash": r_hash,
            })
            return response, 200
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        traceback.print_exc() 
        response = jsonify({"error": error_message})
        return response, 500

@app.route("/add-user", methods=["POST"])
def add_user(user_uuid):
    try:
        data = request.get_json()

        if "user_uuid" not in data:
            response = jsonify({"message": "No user_id provided"})
            return response, 400

        user_uuid = data["user_uuid"]
        add_user_uuid(user_uuid)
        response = jsonify({"message": "User added"})
        return response, 200
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        traceback.print_exc()
        response = jsonify({"error": error_message})
        return response, 500
    
@app.route("/get-credit", methods=["POST"])
def get_credit(user_uuid):
    try:
        data = request.get_json()

        if "user_uuid" not in data:
            response = jsonify({"message": "No user_uuid provided"})
            return response, 400

        if "user_uuid" in data:
            user_uuid = data["user_uuid"]
            credit_satoshis = lookup_user_credit(user_uuid)
            response = jsonify({"credit_satoshis": credit_satoshis})
            return response, 200
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        traceback.print_exc()
        response = jsonify({"error": error_message})
        return response, 500

@app.route("/add-credit", methods=["POST"])
def add_credit(user_uuid):
    try:
        data = request.get_json()

        if "user_uuid" and "amount" not in data and "r_hash" not in data:
            response = jsonify({"message": "No user_uuid or r_hash provided"})
            return response, 400
        
        # check if we're in the middle of a payment
        if "r_hash" in data:
            r_hash = data["r_hash"]
            (paid, invoice) = check_payment(r_hash)
            if paid:
                # Check that the invoice hasn't been used before
                if check_invoice_used(r_hash):
                    # Return the response to the client
                    # What's a good error code that's not an error but doesn't return a response?
                    # A neutral code?
                    response = jsonify({"message": "Payment already used"})
                    return response, 200
                else:
                    # mark invoice as used
                    set_invoice_used(r_hash)
                    # deduct credit from user
                    user_uuid = lookup_user_by_r_hash(r_hash)
                    amount = lookup_invoice(r_hash)["value"]
                    set_user_credit(user_uuid, amount)

                # Return the response to the client
                response = jsonify({"message": f'Added {amount} satoshis to user {user_uuid}'})
                return response, 200 
            else:
                # Return the response to the client
                response = jsonify(
                    {
                        "message": "Payment Required",
                        "payment_request": invoice["payment_request"],
                        "memo": invoice["memo"],
                    }
                )
                return response, 402
        else:
            # If r_hash isn't in request, generate an invoice
            user_uuid = data["user_uuid"]
            invoice_description = f"Add credit to user {user_uuid}"
            invoice = generate_invoice(invoice_description)
            # convert r_hash from base64 to hex because for some reason LND returns it in base64
            r_hash = base64_to_hex(invoice["r_hash"])
            # add r_hash and description to database
            add_r_hash_and_query(r_hash, invoice_description, user_uuid)
            response = jsonify({
                "message": "Payment Required",
                "invoice": invoice["payment_request"],
                "r_hash": r_hash,
            })
            return response, 200
    except Exception as e:
        # Return an error response if an exception occurs
        error_message = f"An error occurred: {str(e)}"
        traceback.print_exc()
        response = jsonify({"error": error_message})
        return response, 500

# TODO: send file data in request
# translate audio files (TODO: list which audio types are supported)
# @app.route('/audio', methods=['GET'])
# def summarize_audio():
#     # Parse the request data
#     data = request.get_json()
#     query = data['query']

#     # Call the OpenAI API to generate a response
#     f = open("testfile.mp3", "rb")
#     transcript = openai.Audio.transcribe("whisper-1", f)
#     prompt = f"Summarize the following text: {transcript}"
#     summary = openai.Completion.create(
#         engine="text-davinci-002",
#         prompt=prompt,
#         max_tokens=60,
#         n=1,
#         stop=None,
#         temperature=0.7,
#     )


#     # Extract the response text from the API response
#     message = summary.choices[0].text.strip()

#     # Return the response to the client
#     return jsonify({'message': message})


# Start the Flask app on localhost:5000
if __name__ == "__main__":
    app.run(debug=True)
    create_invoices_table()
    create_users_table()
