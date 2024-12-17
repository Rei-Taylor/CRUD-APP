from sqlalchemy import create_engine, Column, Integer, String, Index, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os

from nicegui import ui

# Define base model
Base = declarative_base()

# Define a sample table model (for example, a 'User' table)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    age = Column(Integer)

class ColdStoreIn(Base):
    __tablename__ = 'csin'
    ID = Column(Integer, primary_key=True, index=True)
    Sr_No = Column(String(50), index=True)
    Fi_No = Column(String(50), index=True)
    Date = Column(Date, index=True)
    Form_Type = Column(String(50), index=True)
    Company = Column(String(100), index=True)
    Item = Column(String(100), index=True)
    Type = Column(String(50), index=True)
    Size = Column(String(50), index=True)
    Conversion = Column(String(50), index=True)
    Total_Mc = Column(Float)
    Total_Kg = Column(Float)
    Freezing_Types = Column(String(50), index=True)
    Remark = Column(String(500), index=True)
    Invoiced = Column(String(50), index=True)
    __table_args__ = (
        Index('idx_cold_store_in_company_date', 'Company', 'Date'),
    )

class ProcessingIn(Base):
    __tablename__ = 'processing_in'
    ID = Column(Integer, primary_key=True, index=True)
    Sr_No = Column(String(50), index=True)
    Fi_No = Column(String(50), index=True)
    Date = Column(Date, index=True)
    Company = Column(String(100), index=True)
    Item = Column(String(100), index=True)
    Type = Column(String(50), index=True)
    Size = Column(String(50), index=True)
    Conversion = Column(String(50), index=True)
    Total_Mc = Column(Float)
    Total_Kg = Column(Float)
    Freezing_Type = Column(String(50), index=True)
    __table_args__ = (
        Index('idx_processing_in_company_date', 'Company', 'Date'),
    )

class ExportIn(Base):
    __tablename__ = 'csout'
    ID = Column(Integer, primary_key=True, index=True)
    Sr_No = Column(String(50), index=True)
    Invoice_No = Column(String(50), index=True)
    Date = Column(Date, index=True)
    Form_Type = Column(String(100), index=True)
    Company = Column(String(100), index=True)
    Item = Column(String(1000), index=True)
    Type = Column(String(50), index=True)
    Size = Column(String(50), index=True)
    Conversion = Column(Float, index=True)
    Total_Mc = Column(Float)
    Total_Kg = Column(Float)
    Freezing_Types = Column(String(50), index=True)
    Remark = Column(String(500), index=True)

    __table_args__ = (
        Index('idx_export_in_ref_date', 'Sr_No'),
    ) 

class Repacking(Base):
    __tablename__ = 'repacking'
    ID = Column(Integer, primary_key=True, index=True)
    CSID = Column(Integer, ForeignKey('cold_store_in.ID'))
    Sr_No = Column(String(50), index=True)
    Fi_No = Column(String(50), index=True)
    Date = Column(Date, index=True)
    Ref_Date = Column(String(50), index=True)
    Company = Column(String(100), index=True)
    Item = Column(String(1000), index=True)
    Type = Column(String(50), index=True)
    Size = Column(String(50), index=True)
    Conversion = Column(Float, index=True)
    Total_Days = Column(Integer)
    Total_Mc = Column(Float)
    Total_Kg = Column(Float)
    Freezing_Type = Column(String(50), index=True)

    __table_args__ = (
        Index('idx_repacking_ref_date', 'Ref_Date'),
    )           
DB_USER = os.getenv("DB_USER", "default_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "default_password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "default_db")

# Update the connection string
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# Configure the engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=10,  
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True
)
Session = sessionmaker(bind=engine)

# Function to connect to the database
def connect_to_db():
    return Session()

# Add data goes here
def add_row(session, a, b, c,l, d, e, f, g, h, i, j, k,m):
    new_row = ColdStoreIn(Sr_No=a, Fi_No=b, Date=c, Form_Type = l,Company=d, Item=e, Type=f, Size=g, Conversion=h, Total_Mc=i, Total_Kg=j, Freezing_Types=k, Remark=m)
    session.add(new_row)
    session.commit()
    ui.notify("Success")
    return new_row

def add_row_exp(session, a, b, c,l, d, e, f, g, h, i, j, k,m):
    new_row = ExportIn(Sr_No=a, Invoice_No=b, Date=c, Form_Type = l,Company=d, Item=e, Type=f, Size=g, Conversion=h, Total_Mc=i, Total_Kg=j, Freezing_Types=k, Remark=m)
    session.add(new_row)
    session.commit()
    return new_row

def add_processing_row(session, a, b, c, d, e, f, g, h, i, j, k):
    new_row = ProcessingIn(Sr_No=a, Fi_No=b, Date=c, Company=d, Item=e, Type=f, Size=g, Conversion=h, Total_Mc=i, Total_Kg=j, Freezing_Type=k)
    session.add(new_row)
    session.commit()
    return new_row

# Function to add a new user
def add_user(session, name, age):
    new_user = User(name=name, age=age)
    session.add(new_user)
    session.commit()
    return new_user

def edit_row(session, df,a, b, c, d, e, f, g, h, i, j, k):
    row = session.query(df).filter_by(id=a).first()
    if row:
        if b:
            row.Sr_No = b
        if c:
            row.Fi_No = c
        if d:
            row.Date = d
        if e:
            row.Company = e
        if f:
            row.Item = f
        if g:
            row.Type = g
        if h:
            row.Size = h
        if i:
            row.Total_Mc = i
        if j:
            row.Total_Kg = j
        if k:
            row.Freezing_Type = k
        session.commit()
        return row
    return None                                       

# Function to edit an existing user
def edit_user(session, user_id, new_name=None, new_age=None):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        if new_name:
            user.name = new_name
        if new_age:
            user.age = new_age
        session.commit()
        return user
    return None

# Function to delete a user by ID
def delete_user(session, user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
        return True
    return False

# Show here
def show_crin(session):
    crins = session.query(ColdStoreIn).all()
    
    # Create a DataFrame for ColdStoreIn
    crin_data = [{
        'ID': crin.ID,
        'Sr_No': crin.Sr_No,
        'Fi_No': crin.Fi_No,
        'Date': crin.Date,
        'Form_Type': crin.Form_Type,
        'Company': crin.Company,
        'Item': crin.Item,
        'Type': crin.Type,
        'Size': crin.Size,
        'Conversion': crin.Conversion,
        'Total_Mc': crin.Total_Mc,
        'Total_Kg': crin.Total_Kg,
        'Freezing_Types': crin.Freezing_Types,
        'Remark': crin.Remark,
        'Invoiced': crin.Invoiced
    } for crin in crins]

    crin_df = pd.DataFrame(crin_data)
    return crin_df

def show_processing(session):
    crins = session.query(ProcessingIn).all()
    if crins:
        data = [{
            'ID': crin.ID,
            'Sr_No': crin.Sr_No,
            'Fi_No': crin.Fi_No,
            'Date': crin.Date,
            'Company': crin.Company,
            'Item': crin.Item,
            'Type': crin.Type,
            'Size': crin.Size,
            'Conversion': crin.Conversion,
            'Total_Mc': crin.Total_Mc,
            'Total_Kg': crin.Total_Kg,
            'Freezing_Type': crin.Freezing_Type
        } for crin in crins]
        return pd.DataFrame(data)
    else:
        pass

def show_repacking(session):
    crins = session.query(Repacking).all()
    if crins:
        data = [{
            'ID': crin.ID,
            'CSID': crin.CSID,
            'Sr_No': crin.Sr_No,
            'Fi_No': crin.Fi_No,
            'Date': crin.Date,
            'Ref_Date': crin.Ref_Date,
            'Company': crin.Company,
            'Item': crin.Item,
            'Type': crin.Type,
            'Size': crin.Size,
            'Conversion': crin.Conversion,
            'Total_Mc': crin.Total_Mc,
            'Total_Kg': crin.Total_Kg,
            'Freezing_Type': crin.Freezing_Type,
            'Total_Days': crin.Total_Days
        } for crin in crins]
        return pd.DataFrame(data)
    else:
        pass     

def show_exportin(session):
    crins = session.query(ExportIn).all()
    if crins:
        data = [{
            'ID': crin.ID,
            'Sr_No': crin.Sr_No,
            'Invoice_No': crin.Invoice_No,
            'Date': crin.Date,
            'Form_Type': crin.Form_Type,
            'Company': crin.Company,
            'Item': crin.Item,
            'Type': crin.Type,
            'Size': crin.Size,
            'Conversion': crin.Conversion,
            'Total_Mc': crin.Total_Mc,
            'Total_Kg': crin.Total_Kg,
            'Freezing_Types': crin.Freezing_Types,
            'Remark':crin.Remark
        } for crin in crins]
        return pd.DataFrame(data)
    else:
        pass    



def insert_multiple_rows_into_export_in(session, rows: list):
    """
    Insert multiple rows into the ExportIn table.
    """
    new_rows = [ExportIn(**row) for row in rows]
    session.bulk_save_objects(new_rows)
    session.commit()

def bulk_add_export_in(filtered_df, sr_no, fi_no, date):
    print("this is called")
    session = connect_to_db()
    new_rows = []
    for _, row in filtered_df.iterrows():
        new_row = {
            "CSID": row["ID"],
            "Sr_No": sr_no,
            "Fi_No": fi_no,
            "Date": date,
            "Ref_Date": row["Date"],
            "Company": row["Company"],
            "Item": row["Item"],
            "Type": row["Type"],
            "Size": row["Size"],
            "Conversion": row["Conversion"],
            "Total_Days": (date - row["Date"]).days,  # Example calculation for Total_Days
            "Total_Mc": row["Total_Mc"],
            "Total_Kg": row["Total_Kg"],
            "Freezing_Type": row["Freezing_Type"]
        }
        new_rows.append(new_row)

    print("new row added")
    insert_multiple_rows_into_export_in(session, new_rows)
    session.close()

def insert_multiple_rows_into_rp_in(session, rows: list):
    """
    Insert multiple rows into the ExportIn table.
    """
    new_rows = [Repacking(**row) for row in rows]
    session.bulk_save_objects(new_rows)
    session.commit()

def bulk_add_rp_in(filtered_df, sr_no, fi_no, date):
    print("this is called")
    session = connect_to_db()
    new_rows = []
    for _, row in filtered_df.iterrows():
        new_row = {
            "CSID": row["ID"],
            "Sr_No": sr_no,
            "Fi_No": fi_no,
            "Date": date,
            "Ref_Date": row["Date"],
            "Company": row["Company"],
            "Item": row["Item"],
            "Type": row["Type"],
            "Size": row["Size"],
            "Conversion": row["Conversion"],
            "Total_Days": (date - row["Date"]).days,  # Example calculation for Total_Days
            "Total_Mc": row["Total_Mc"],
            "Total_Kg": row["Total_Kg"],
            "Freezing_Type": row["Freezing_Type"]
        }
        new_rows.append(new_row)

    print("new row added")
    insert_multiple_rows_into_rp_in(session, new_rows)
    session.close()    

# ... existing code ...
def update_row(id, Sr_No, Fi_No, Date,Form_Type, Company, Item, Type, Size, Conversion, Total_Mc, Total_Kg, Freezing_Type,Remark, table):
    session = connect_to_db()
    try:
        if table == "crin":
            row = session.query(ColdStoreIn).filter_by(ID=id).first()
        elif table == "processing":
            row = session.query(ProcessingIn).filter_by(ID=id).first()
        elif table == "export":
            row = session.query(ExportIn).filter_by(ID=id).first()
        
        if row:
            row.Sr_No = Sr_No
            row.Fi_No = Fi_No
            row.Date = Date
            row.Form_Type = Form_Type
            row.Company = Company
            row.Item = Item
            row.Type = Type
            row.Size = Size
            row.Conversion = Conversion
            row.Total_Mc = Total_Mc
            row.Total_Kg = Total_Kg
            row.Freezing_Types = Freezing_Type
            row.Remark = Remark
            session.commit()
            ui.notify("success")
    except Exception as e:
        session.rollback()
        ui.notify(f"An error occurred while updating the row: {e}")
    finally:
        session.close()

def update_crin(session, a, c, d, e, f, g, h, i, j, k, l, m):
    crin = session.query(ColdStoreIn).filter_by(ID=a).first()
    if crin:
        crin.Sr_No = c
        crin.Fi_No = d
        crin.Date = e
        crin.Company = f
        crin.Item = g
        crin.Type = h
        crin.Size = i
        crin.Conversion = j
        crin.Total_Mc = k
        crin.Total_Kg = l
        crin.Freezing_Type = m
        session.commit()
        return crin
    return None

def show_data(session):
    users = session.query(User).all()
    if users:
        data = [{
            'ID': user.id,
            'Name': user.name,
            'Age': user.age
        } for user in users]
        return pd.DataFrame(data)
    else:
        return pd.DataFrame(columns=['ID', 'Name', 'Age'])

# Function to update user data
def update_user(session, user_id, new_name, new_age):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.name = new_name
        user.age = new_age
        session.commit()
        return user
    return None

def insert_coldstorein(session, *args):
    """
    Insert data into ColdStoreIn table.
    """
    new_row = ColdStoreIn(
        Sr_No=args[0],
        Fi_No=args[1],
        Date=args[2],
        Company=args[3],
        Item=args[4],
        Type=args[5],
        Size=args[6],
        Conversion=args[7],
        Total_Mc=args[8],
        Total_Kg=args[9],
        Freezing_Type=args[10]
    )
    session.add(new_row)
    session.commit()
    return new_row

if __name__ == "__main__":
    session = connect_to_db()

    # Add a new user
    added_user = add_user(session, 'John Doe', 30)
    print(f"Added user: {added_user.name}, {added_user.age}")

    # Edit the user
    updated_user = edit_user(session, added_user.id, new_name='Johnny Doe', new_age=31)
    if updated_user:
        print(f"Updated user: {updated_user.name}, {updated_user.age}")

    # Delete the user
    delete_success = delete_user(session, added_user.id)
    if delete_success:
        print("User deleted successfully.")

    # Insert a new ColdStoreIn record
    new_crin = insert_coldstorein(session, '001', 'FI001', '2023-10-01', 'Company A', 'Item A', 'Type A', 'Size A', 'Conv A', 100.0, 200.0, 'Freezing A')
    print(f"Inserted ColdStoreIn record: {new_crin.ID}, {new_crin.Sr_No}")