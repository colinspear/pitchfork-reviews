#!/usr/bin/env bash

source /home/cspear/external/pitchfork-reviews/.env

mjl=4tK6Z8fK7Sc9133byjPGIT
so=3uQ5cxFHxXddqPL58egs1z
cj=1WVGbBnzZ5WLZ2PfesIHik #=rO6MAFXjQxmP8O1ISoCdxw

ACCESS_TOKEN=$( curl -s -X POST --url "https://accounts.spotify.com/api/token" \
    -d "client_id=$CLIENT_ID" \
    -d "client_secret=$CLIENT_SECRET" \
    -d "grant_type=client_credentials" \
    | jq -r '.access_token' )


curl -G -i -s "https://api.spotify.com/v1/artists" \
    --data-urlencode "ids=$cj" \
    --header "Authorization: Bearer $ACCESS_TOKEN" \
    | grep genres

