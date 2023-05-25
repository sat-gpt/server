# Create the invoice, pricing based on the query length
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the capital of France?", "user_uuid": "test78e4-a83b-4d8c-b8bd-a0343ca641b4"}' \
     http://localhost:5000/query

# Checking payment (if success, you'll get a chatgpt response)
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"query": "Hi, this is a longer query message.", "user_uuid": "test4444-a83b-4d8c-b8bd-a0343ca641b4"}' \
     http://localhost:5000/query

curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"query": "Hi, this is a longer query message.", "user_uuid": "test4444-a83b-4d8c-b8bd-a0343ca641b4", "r_hash": "b6681465097c337360eebec3cb5785e046a3f99b85c5e47310992181685691b7"}' \
     http://localhost:5000/query

curl -X POST \
     -H "Content-Type: application/json" \
     -d '{ "user_uuid": "test4444-a83b-4d8c-b8bd-a0343ca641b4"}' \
     http://localhost:5000/add-user

curl -X POST \
     -H "Content-Type: application/json" \
     -d '{ "user_uuid": "test4444-a83b-4d8c-b8bd-a0343ca641b4"}' \
     http://localhost:5000/get-credit

curl -X POST \
     -H "Content-Type: application/json" \
     -d '{ "user_uuid": "test4444-a83b-4d8c-b8bd-a0343ca641b4", "amount": 100 }' \
     http://localhost:5000/add-credit

curl -X POST \
     -H "Content-Type: application/json" \
     -d '{ "user_uuid": "test4444-a83b-4d8c-b8bd-a0343ca641b4", "amount": 100, "r_hash": "f659ec404fb520c5678ad45783985f5f605ece3e9eb0c21913a90f2f2abf2091"}' \
     http://localhost:5000/add-credit


# ERROR TEST:
# Create the invoice (without a user_uuid)
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the capital of France?"}' \
     http://localhost:5000/query
