from app.server_builder import ServerBuilder
from lib.console_builder import build_and_run_console

if __name__ == '__main__':
    builder = ServerBuilder(use_test_database=True)
    builder.build()
    builder.boot_server()

    build_and_run_console(builder.injector)

    builder.expose_service()
