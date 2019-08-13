from flask_restplus import fields
from spending_tracker.cli import api


class SchemeBuilder(dict):
    def add_control(self, ctrl_name: str, href: str, **kwargs) -> None:
        """Add control to schema dict"""
        if ctrl_name not in self:
            self[ctrl_name] = {}
        self[ctrl_name] = kwargs
        self[ctrl_name] = fields.Url(example=href)


def schema_builder(model: object = None, ctrl_name=None, href=None) -> object:
    """Api schema generator.
    Builds properties based on db model schema
    args:
        model (object): db model object
        ctrl_name (str): name of control
        href (str): uri for control

    Returns:
        object: api model object
    """
    name = str(model)
    asd = SchemeBuilder()
    asd.add_control(ctrl_name, href)
    control_scheme = api.model(name + '_control', asd)
    if model:
        schema_func = getattr(model, 'get_schema')
        user_schema = api.model(name + '_schema', {
            'properties': fields.Nested(schema_func()),
            'links': fields.Nested(control_scheme)
        })
    else:
        user_schema = api.model('User links', {
            'links': fields.Nested(control_scheme)
        })
    return user_schema
