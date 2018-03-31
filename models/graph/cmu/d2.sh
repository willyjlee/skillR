#!/bin/bash

echo "download model graph : cmu"

extract_download_url() {

        url=$( curl -q -o - $1 |  grep -o 'http*://download[^"]*' | tail -n 1 )
        echo "$url"

}

curl $( extract_download_url http://www.mediafire.com/file/1pyjsjl0p93x27c/graph_freeze.pb ) -o graph_freeze.pb
curl $( extract_download_url http://www.mediafire.com/file/qlzzr20mpocnpa3/graph_opt.pb ) -o graph_opt.pb
curl $( extract_download_url http://www.mediafire.com/file/i72ll9k5i7x6qfh/graph.pb ) -o graph.pb
