#!/bin/bash

read -r -p "Answer Content: " answer_content
read -r -p "Topic ID: " topic_id

# curl command for posting answer
curl -i -H "Content-Type: application/json" \
   -X POST -d '{"answer_content": "'$answer_content'", "topic_id": '$topic_id'}' \
   -b cookie-jar -k https://cs3103.cs.unb.ca:8037/answer
