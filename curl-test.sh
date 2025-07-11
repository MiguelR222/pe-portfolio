#!/bin/bash

echo "Creating new post..."
post_response=$(curl -X POST http://localhost:5000/api/timeline_post -d 'name=Miguel&email=miguel.ruiz0652@gmail.com&content=DB in Portfolio')
echo "POST Response:"
echo "$post_response"

timeline_post_id=$(echo "$post_response" | jq -r '.id')
if [ -z "$timeline_post_id" ]; then
    echo "Error: Could not extract ID from POST response"
    exit 1
fi
echo "Extracted ID: $timeline_post_id"

echo -e "Checking if post exists..."
get_response=$(curl http://localhost:5000/api/timeline_post)
echo "GET Response:"
echo "$get_response"

if echo "$get_response" | jq -e ".timeline_posts[] | select(.id == $timeline_post_id)" > /dev/null; then
    echo "Post with ID $timeline_post_id found in GET response"
else
    echo "Error: Post with ID $timeline_post_id not found in GET response"
    exit 1
fi

echo "Deleting post..."
curl -X DELETE "http://localhost:5000/api/timeline_post/$timeline_post_id"