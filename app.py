import dotenv

dotenv.load_dotenv()

from core.initializer import initialize
from route import routers
from model import db


app = initialize(__name__, routers)


@app.before_request
def connect_db():
    if db.is_closed():
        db.connect()


@app.after_request
def close_db(res):
    if not db.is_closed():
        db.close()

    return res


if __name__ == "__main__":
    app.run()
