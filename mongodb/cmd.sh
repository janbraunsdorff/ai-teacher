docker run --network host     mongo:4.4 mongo --username admin_user --password admin_pass --host localhost:27017  --authenticationDatabase admin admin --eval "$(< replication-init.js)"
docker run --network host -it mongo:4.4 mongo --username admin_user --password admin_pass --host localhost:27017  --authenticationDatabase admin admin --eval "rs.status()"
docker run --network host -it mongo:4.4 mongo --username admin_user --password admin_pass --host localhost:27017  --authenticationDatabase admin admin --eval "$(< mongo-init.js)"


#mongodb://application_user:application_pass@mongodb_server_lynx:27017,mongodb_server_puma:27017,mongodb_server_wolf:27017/application_database?replicaSet=rs1
#mongodb://application_user:application_pass@localhost:27017,localhost:27117,localhost:27217/application_database?replicaSet=rs1
