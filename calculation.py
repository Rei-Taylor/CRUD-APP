
import pandas as pd
import numpy as np

from database import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import time
from io import BytesIO

import requests
from sqlalchemy.orm import Session
from database import ExportIn







path = r"C:\Users\User\Downloads\MSLI_TEST_CRIN (3).xlsx"



Freezing_Types = ["Airblast-G","Airblast-BG","Airblast-W","Contact","Airblast-IQF","Double-Glazing"]


def sql():
    return connect_to_db()





#other logic here
def multiply(a, b):
    mu = pd.to_numeric(a) * pd.to_numeric(b)
    return mu



#show here 

def crin():
    connect = sql()
    try:
        df = show_crin(connect) 
        df['Total_Mc'] = df['Total_Mc'].round(2)
        df['Total_Kg'] = df['Total_Kg'].round(2)
        df['selected'] = False
    except Exception as e:
        ui.notify("An error occurred: {e}")
    finally:
        connect.close()
    return df





def export():
    connect = sql()
    try:
        df = show_exportin(connect)
        df['Total_Mc'] = df['Total_Mc'].round(2)
        df['Total_Kg'] = df['Total_Kg'].round(2)
        df['selected'] = False
    except Exception as e:
        ui.notify(f"An error occurred: {e}")
    finally:
        connect.close()
    return df


#unique values goes here


def delete_rows(session, ids_to_delete, data):
    """
    Delete rows from the ExportIn table based on a list of IDs.

    :param session: SQLAlchemy session object
    :param ids_to_delete: List of IDs to delete from the ExportIn table
    """
    try:
        if data == "repacking":
            session.query(Repacking).filter(Repacking.ID.in_(ids_to_delete)).delete(synchronize_session='fetch')
            session.commit()

        elif data == "crin":
            record = session.query(ColdStoreIn).filter_by(ID=ids_to_delete).one()
            session.delete(record)
            session.commit()
            time.sleep(2)

    except Exception as e:
        session.rollback()
        ui.notify(f"erorr{e} ")
        ui.notify(f"An error occurred while deleting rows: {e}")
    finally:
        session.close()

def delete_export_in_rows(session, ids_to_delete):
    """
    Delete rows from the ExportIn table based on a list of IDs.

    :param session: SQLAlchemy session object
    :param ids_to_delete: List of IDs to delete from the ExportIn table
    """
    try:
        # Delete rows with IDs in the provided list
        record = session.query(ExportIn).filter_by(ID=ids_to_delete).one()
        session.delete(record)
        session.commit()
        ui.notify("Selected rows deleted successfully.")
        
    except Exception as e:
        session.rollback()
        ui.notify(f"An error occurred while deleting rows: {e}")
    finally:
        session.close()





