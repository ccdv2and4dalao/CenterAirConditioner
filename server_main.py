from app.server_builder import ServerBuilder

if __name__ == '__main__':
    builder = ServerBuilder()
    builder.build()
    builder.boot_server()
    builder.expose_service()
