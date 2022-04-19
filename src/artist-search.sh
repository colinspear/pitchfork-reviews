#!/usr/bin/env bash

source .env

CLIENT_ID=$CLIENT_ID
CLIENT_SECRET=$CLIENT_SECRET

ACCESS_TOKEN=$( curl -X POST --url "https://accounts.spotify.com/api/token" \
    -d "client_id=$CLIENT_ID" \
    -d "client_secret=$CLIENT_SECRET" \
    -d "grant_type=client_credentials" \
    | jq -r '.access_token' )

#    curl --request GET --url "https://api.spotify.com/v1/search?q=Lambchop&type=artist" \
#      --header "Authorization: Bearer $ACCESS_TOKEN"

#artist='Florence + the Machine'

# TODO: get latest artist file
artists=$( sort -u '../data/processed/artists.txt' )

dt=$( date --rfc-339='date' )
echo "id, name, popularity, followers" > "../data/processed/${dt}-sp_data.csv"

for artist in artists; do
    curl -G "https://api.spotify.com/v1/search?type=artist" \
        --data-urlencode "q=$artist" \
        --header "Authorization: Bearer $ACCESS_TOKEN" |
        jq -r '.artists.items[0] | 
            "\(.id), \(.name), \(.popularity), \(.followers.total)"' >> "../data/processed/${dt}-sp_data.csv"
done


