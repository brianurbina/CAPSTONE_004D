import redis

# Conexión a Redis
client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

# Verificar la conexión
try:
    client.ping()
    print("Conexión exitosa a Redis!")
except redis.ConnectionError:
    print("No se pudo conectar a Redis.")
