import json

from fastapi_sqlalchemy import db
from h602_central.models.h602_central_models import *
import sqlalchemy as sa
class settings_logic:

    @staticmethod
    def get(name, default_value=''):
        obj = db.session.query(settings_model).filter(settings_model.name == name, settings_model.is_active == 't').first()
        if not obj:
            return default_value

        if obj.datatype == 'int':
            return int(obj.value)
        elif obj.datatype == 'bool':
            return eval(obj.value)
        elif obj.datatype == 'json':
            return json.loads(obj.value)
        else:
            return obj.value


    def get_queue_status(self):
        queue = db.session.query(queue_model).filter(queue_model.is_active == 't',
                                                     queue_model.status == 1).all()
        print(queue)

default = settings_logic
