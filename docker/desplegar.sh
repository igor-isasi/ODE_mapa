#!/bin/bash

sudo docker-compose down
sudo docker rm opendataeuskadiapis-web-1
sudo docker rmi opendataeuskadiapis-web
sudo docker-compose build --no-cache
sudo docker-compose up