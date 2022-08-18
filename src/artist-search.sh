#!/usr/bin/env bash

source /home/cspear/external/pitchfork-reviews/.env
source $PROJECT_PATH/src/utils.sh

function retrieve_data() {
    echo "id, name, popularity, followers" > $2
    while read artist; do
        printf "Retrieving information for $artist.\n"
        curl -G -i -s "https://api.spotify.com/v1/search?type=artist" \
            --data-urlencode "q=$artist" \
            --header "Authorization: Bearer $3" > response

        code=$( head -1 response | awk '{ print $2 }' )
        if [[ $code == 200 ]]; then 
            printf "\nArtist information successfully retrieved. Processing data now...\n"
        elif [[ $code == 429 ]]; then
            wait_time=$( grep -o 'retry-after' | awk '{ print $2 }' )
            printf "\nToo many retries. Will try again after $wait_time seconds.\n"
            sleep $( ( wait_time + 5 ) )
            c=0
            while [[ c < 2 ]]; do
                retrieve_data $1 $2 $3
                c=$c+1
            done
            printf "\nAttempted wait sequence unsuccessfully 3 times. Exiting program.\n"
            exit 1
        else
            printf "\nUnrecognized response code\n"
        fi

        tr -d '\r' < response | awk -v RS="" '{ if ( NR==2 ) print }' \
            | jq -r '.artists.items[0] 
            | "\(.id), \(.name), \(.popularity), \(.followers.total)"' >> $2

        rm response
        printf "Artist $artist complete.\n"
    done < $1
}

ACCESS_TOKEN=$( curl -s -X POST --url "https://accounts.spotify.com/api/token" \
    -d "client_id=$CLIENT_ID" \
    -d "client_secret=$CLIENT_SECRET" \
    -d "grant_type=client_credentials" \
    | jq -r '.access_token' )

# TODO: get latest artist list
artist_list="$PROJECT_PATH/data/processed/2022-08-18-artists-unique.txt"

dt=$( date --rfc-3339='date' )
artist_data="$PROJECT_PATH/data/processed/$dt-sp_data.csv"
#timeout 30 retrieve_data $artist_list $artist_data $ACCESS_TOKEN
retrieve_data $artist_list $artist_data $ACCESS_TOKEN

x=( $( wc -l $artist_data ) )
printf "$(( ${x[0]}-1 )) artists processed. Data saved to ${x[@]:1}.\n"

