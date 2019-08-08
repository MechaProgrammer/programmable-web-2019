import click
from spending_tracker import api, blueprint, app, db
from spending_tracker.models.usermodels import users


@click.command()
@click.option('--port', default=5000, help='Service port')
@click.option('--debug', default=False, is_flag=True, help='App debug mode')
def run(port, debug):
    api.add_namespace(users, path='/users')
    app.register_blueprint(blueprint)
    app.app_context().push()
    db.create_all()
    app.run(debug=debug, port=port)
