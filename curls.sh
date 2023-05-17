# Create the invoice, pricing based on the query length
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the largest city?"}' \
     http://localhost:5000/query

# Checking payment (if success, you'll get a chatgpt response)
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{ "r_hash": "3e2285b9c31c8c3668003c633de04ca338e38e0087060d49c738363c2854a26c"}' \
     http://localhost:5000/query

#23cb5236d9bc32e2b90e9926608af26173e02f947511d5574615ff22ff26b24e