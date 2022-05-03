export DOCKER_HOST=tcp://192.168.3.7:2375

docker-compose pull && docker stack deploy --with-registry-auth --compose-file ./docker-stack-demo.yml h602

exit
