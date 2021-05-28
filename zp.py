import os
import logging
from app import create_app, db
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
@app.shell_context_processor
def make_shell_context():
    return dict(db=db)

@app.cli.command()
def test():

    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':

    app.run(debug=True)
    logging.getLogger().setLevel("DEBUG")
    app.jinja_env.filters['zip'] = zip
