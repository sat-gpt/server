# Create the invoice, pricing based on the query length
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the capital of France?", "user_uuid": "cd2b78e4-a83b-4d8c-b8bd-a0343ca641b4"}' \
     http://localhost:5000/query

# Checking payment (if success, you'll get a chatgpt response)
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{ "r_hash": "1870fc8372fbfcf42a60838bf070c67bce195d1f928fca4340d8d72f0abb87bc"}' \
     http://localhost:5000/query

curl -X POST \
     -H "Content-Type: application/json" \
     -d '{ "user_uuid": "cd2b78e4-a83b-4d8c-b8bd-a0343ca641b4"}' \
     http://localhost:5000/add-user

curl -X POST \
     -H "Content-Type: application/json" \
     -d '{ "user_uuid": "cd2b78e4-a83b-4d8c-b8bd-a0343ca641b4"}' \
     http://localhost:5000/get-credit

curl -X POST \
     -H "Content-Type: application/json" \
     -d '{ "user_uuid": "cd2b78e4-a83b-4d8c-b8bd-a0343ca641b4", "amount": 10 }' \
     http://localhost:5000/add-credit

curl -X POST \
     -H "Content-Type: application/json" \
     -d '{ "r_hash": "419a8af46102beaf7c6d7000723ed4bc6e85bb32817da1cdb6b70ee1b1fb254d" }' \
     http://localhost:5000/add-credit

# ERROR TEST:
# Create the invoice (without a user_uuid)
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the capital of France?"}' \
     http://localhost:5000/query
