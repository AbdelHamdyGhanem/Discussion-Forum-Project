#!/bin/bash

# curl command for logout
curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:8037/logout
