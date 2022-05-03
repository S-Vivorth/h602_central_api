import os


class Config:
    DATABASE_URI = (
        os.getenv('DATABASE_URI')
        or 'postgresql+psycopg2://postgres:underadmin@192.168.3.7:5432/qe_central'
    )
