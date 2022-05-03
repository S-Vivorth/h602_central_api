import json
import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
target_dir = os.path.sep.join(current_dir.split(os.path.sep)[0:-2])
sys.path.insert(0, target_dir)
from h602_central.models.h602_central_models import *
from h602_central.logics.settings_logic import settings_logic
import schedule
import time
from sqlalchemy import create_engine
from h602_central.config import Config
from fastapi_sqlalchemy import db
from sqlalchemy.orm import Session, sessionmaker
import requests

engine = create_engine(Config.DATABASE_URI)
engine.connect()
Session = sessionmaker(bind=engine)
session = Session()


def get_queue_status():
    b24_queue_detail_list = session.query(queue_detail_model).filter(queue_detail_model.is_active == 't',
                                                                     queue_detail_model.status == 1).all()

    for b24_queue_detail in b24_queue_detail_list:
        biller_code = b24_queue_detail.b24_biller_code
        company_b24 = session.query(company_b24_model).filter(company_b24_model.code == biller_code,
                                                              company_b24_model.is_active == 't').first()
        token = company_b24.token
        headers = {'Accept': "application/json", "token": token}
        print(headers)
        response = requests.get(url=f'https://supplierapi-demo.bill24.net/queue/detail/{b24_queue_detail.b24_queue_id}',
                                headers=headers
                                )
        if response.status_code == 200:
            if json.loads(response.text)['status'] == "ready":
                new_queue_detail = queue_detail_model()

                new_queue_detail.status = 2
                new_queue_detail.data = str(json.loads(response.text)['data'])
                copy(new_queue_detail, b24_queue_detail,
                     ignores=['id', 'queue_id', 'b24_queue_id', 'b24_biller_code', 'is_active', 'created_date',
                              'updated_date', 'updated_by', 'created_by'])
                queue = session.query(queue_model).filter(
                    queue_model.id == b24_queue_detail.queue_id,
                    queue_model.is_active == 't',
                ).first()
                if queue is not None:
                    new_queue = queue_model()
                    new_queue.status = 2
                    copy(new_queue, queue,
                         ignores=['id', 'company_id', 'date', 'type', 'total_record', 'data', 'is_active',
                                  'created_date', 'updated_date', 'updated_by', 'created_by'])

    session.commit()


def copy(from_obj, to_obj, ignores=[]):
    """copy all properties from one oject to another object in the same sqlalchemy class.
    :param from_obj: source object that will copy attribue to destination object.
    :param to_obj: destination object tha will copy from source object.
    :param ignores: list of columns that will not override value from source object to destination object.
    """
    for key in [k for k in from_obj.__table__.columns.keys() if k not in ignores]:
        setattr(to_obj, key, getattr(from_obj, key))

        # fix .ext for ExtMixin
    # because .ext is just declare in ExtMixin not in .columns schema
    # we need to for copy it if source object contain that
    if hasattr(from_obj, 'ext'):
        to_obj.ext = from_obj.ext

    return to_obj


schedule.every(3).minutes.do(get_queue_status)
while True:
    schedule.run_pending()
    time.sleep(1)
