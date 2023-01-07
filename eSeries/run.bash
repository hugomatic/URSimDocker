docker run -it --add-host=host.docker.internal:host-gateway -p 5900:5900 -p 29999:29999 -p 30001-30004:30001-30004 -p 8080:8080 -p 2222:22  -e ROBOT_TYPE=UR10 ursim/ur10
