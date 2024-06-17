#!/bin/bash

# curl command for deleting topic
curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:8037/topics/1
