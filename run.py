import zaneapi
import config


if __name__ == "__main__":
    app = zaneapi.create_app(config.Config)
    app.run(port=5000)
