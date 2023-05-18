# Create the invoice, pricing based on the query length
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the capital of France?", "user_uuid": "cd2b78e4-a83b-4d8c-b8bd-a0343ca641b4"}' \
     http://localhost:5000/query

# Checking payment (if success, you'll get a chatgpt response)
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"query": "Hi", "user_uuid": "test78e4-a83b-4d8c-b8bd-a0343ca641b4"}' \
     http://localhost:5000/query

curl -X POST \
     -H "Content-Type: application/json" \
     -d '{ "user_uuid": "test78e4-a83b-4d8c-b8bd-a0343ca641b4"}' \
     http://localhost:5000/add-user

curl -X POST \
     -H "Content-Type: application/json" \
     -d '{ "user_uuid": "test78e4-a83b-4d8c-b8bd-a0343ca641b4"}' \
     http://localhost:5000/get-credit

curl -X POST \
     -H "Content-Type: application/json" \
     -d '{ "user_uuid": "test78e4-a83b-4d8c-b8bd-a0343ca641b4", "amount": 10 }' \
     http://localhost:5000/add-credit

curl -X POST \
     -H "Content-Type: application/json" \
     -d '{ "r_hash": "16d18f8ebd36b67c16e8e2d86a5199d1b82dbcca0a5c9c2d097f96d7ac3a65a5" }' \
     http://localhost:5000/add-credit

# ERROR TEST:
# Create the invoice (without a user_uuid)
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the capital of France?"}' \
     http://localhost:5000/query
