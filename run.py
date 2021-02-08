from zaneapi import create_app
from config import Config

app = create_app(Config)

if __name__ == "__main__":
    app.run("0.0.0.0", port=80)
