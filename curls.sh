# Create the invoice, pricing based on the query length
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the capital of France?"}' \
     http://localhost:5000/query

# Checking payment (if success, you'll get a chatgpt response)
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{ "r_hash": "6f04b3e60f412965bf10b2f68636aa233f29afc89ed053e0ca7d00ac8795f793"}' \
     http://localhost:5000/query
