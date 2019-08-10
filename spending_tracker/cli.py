import click
from spending_tracker import api, blueprint, create_app, db


@click.command()
@click.option('--port', default=5000, help='Service port')
@click.option('--debug', default=False, is_flag=True, help='App debug mode')
def run(port, debug):
    app = create_app()
    with app.app_context():
        from spending_tracker.resources.usermodels import users
        from spending_tracker.resources.categorymodels import category
        from spending_tracker.resources.walletmodels import single_user
        api.add_namespace(users, path='/users')
        api.add_namespace(single_user, path='/user')
        api.add_namespace(category, path='/categories')
        app.register_blueprint(blueprint)
        # app.app_context().push()
        db.create_all()
    app.run(debug=debug, port=port)
