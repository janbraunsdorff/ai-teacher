from pydantic import BaseModel


class ConfigMongo(BaseModel):
    protocol: str =  "mongodb"
    user: str =  "application_user"
    password: str = "application_pass"
    servers: str = "mongodb_server_lynx:27017,mongodb_server_puma:27017,mongodb_server_wolf:27017"
    database: str = "teacher"


configMongo = ConfigMongo()
print(configMongo)