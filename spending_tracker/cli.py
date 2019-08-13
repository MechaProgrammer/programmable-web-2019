import click
from spending_tracker import api, blueprint, create_app, db


def app_maker():
    app = create_app()
    with app.app_context():
        from spending_tracker.resources.usermodels import users
        from spending_tracker.resources.categorymodels import category
        from spending_tracker.resources.walletmodels import single_user
        from spending_tracker.resources.entrypoint import entry_point
        api.add_namespace(entry_point, path='/api')
        api.add_namespace(users, path='/api/users')
        api.add_namespace(single_user, path='/api/user')
        api.add_namespace(category, path='/api/categories')
        app.register_blueprint(blueprint)
        db.create_all()
    return app


@click.command()
@click.option('--port', default=5000, help='Service port')
@click.option('--debug', default=False, is_flag=True, help='App debug mode')
def run_client(port, debug):
    """Start flask client"""
    app = app_maker()
    click.echo(
        """
            Spending tracker API is running.
            Swagger documentation can be found on /api/doc
        """
    )
    app.run(debug=debug, port=port)

