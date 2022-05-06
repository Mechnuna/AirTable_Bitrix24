curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"FIELDS_AFTER":{
              "id":"taskId"}}' \
  http://127.0.0.1:5000/api