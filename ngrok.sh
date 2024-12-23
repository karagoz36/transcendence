./ngrok http https://localhost:8000 1>/dev/null &
pid=$!
curl http://localhost:4040/api/tunnels
exit_code=$?

while [ $exit_code -ne 0 ]; do
    curl http://localhost:4040/api/tunnels
    exit_code=$?
    sleep 1
done

export NGROK_URL=$(curl http://localhost:4040/api/tunnels 2>/dev/null | python3 -c "import sys,json;
res=json.load(sys.stdin);
tunnel=res['tunnels'][0];
print(tunnel['public_url']);")

echo $NGROK _URL

docker compose -f srcs/docker-compose.yml up
kill $pid
echo "DONE"