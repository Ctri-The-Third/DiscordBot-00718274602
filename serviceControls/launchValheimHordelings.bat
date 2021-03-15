docker pull lloesche/valheim-server
docker run -d --name valheim-server-hordelings --cap-add=sys_nice -p 2456-2458:2456-2458/udp -p 2459:80 -v C:\ValheimServers\Hordelings\ValheimConfig:/config -v C:\ValheimServers\Hordelings\ValheimServer:/opt/valheim -e SERVER_NAME="Hordelings" -e WORLD_NAME="Dedicated_hordes" -e SERVER_PASS="Gwent" -e STATUS_HTTP=true lloesche/valheim-server
