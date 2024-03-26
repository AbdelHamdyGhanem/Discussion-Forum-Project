#!/bin/bash

# reading
read -r -p "Topic Title: " topic_title
read -r -p "Content: " content

# curl command for posting topic
curl -i -H "Content-Type: application/json" \
   -X POST -d '{"topic_title": "'$topic_title'", "content": "'$content'"}' \
   -b cookie-jar -k https://cs3103.cs.unb.ca:8037/topics