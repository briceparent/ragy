import os

IS_DEV_SERVER = os.path.exists('./is_dev_server')
SERVER_URL = "0.0.0.0"
SERVER_PORT = 80

if IS_DEV_SERVER:
    SERVER_PORT = 8080
    SERVER_URL = "127.0.0.1"
