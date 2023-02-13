docker build -t darkbuddy .
docker rm -f darkbuddy
docker run -ti -d --name darkbuddy -p 9000:9000 darkbuddy
docker image rm -f darkbuddy