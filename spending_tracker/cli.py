import click
from spending_tracker import api, blueprint, app, db
from spending_tracker.models.usermodels import users
from spending_tracker.models.categorymodels import category
from spending_tracker.models.walletmodels import single_user


@click.command()
@click.option('--port', default=5000, help='Service port')
@click.option('--debug', default=False, is_flag=True, help='App debug mode')
def run(port, debug):
    api.add_namespace(users, path='/users')
    api.add_namespace(single_user, path='/user')
    api.add_namespace(category, path='/categories')
    app.register_blueprint(blueprint)
    app.app_context().push()
    db.create_all()
    app.run(debug=debug, port=port)
