from filters import add_one
from __init__ import create_app
import config

app = create_app(config.DevConfig)
app.jinja_env.filters['add_one'] = add_one

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, threaded=True)
