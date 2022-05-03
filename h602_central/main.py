# to access h602_central dir otherwise it will not be found
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from h602_central.models import base_model

from fastapi import FastAPI
from routes import invoices
from routes import online_payments
from routes import operations
from fastapi_sqlalchemy import DBSessionMiddleware

import uvicorn

app = FastAPI(title='Central API', docs_url='/')
from config import Config

app.include_router(online_payments.online_payments)
app.include_router(invoices.invoices)
app.include_router(operations.operations)
app.add_middleware(DBSessionMiddleware, db_url=Config.DATABASE_URI, engine_args={'pool_pre_ping': True})
# at last, the bottom of the file/module

if __name__ == '__main__':
    uvicorn.run(app, debug=True, port=8000, host="0.0.0.0")
#
