
from nicegui import ui 
from calculation import crin, export, connect_to_db, delete_rows, delete_export_in_rows
from database import *
from show import cool, metric_card
import datetime
from analysis import analysis




   

@ui.refreshable_method
def cs():
    df1 = crin()
    df1[col_list]
    cols = {
        'columnDefs': [{'headerName': col, 'field': col} for col in df1.columns],
        'rowData': df1.to_dict(orient='records'),
        'rowSelection': 'multiple',
    }
    return df1


col_list = ["Sr_No", "Fi_No", "Date", "Company", "Item", "Type", "Size", "Conversion", "Total_Mc", "Total_Kg", "Freezing_Types"]
@ui.refreshable_method
def cols(df):
    cols = {
        'columnDefs': [{'headerName': col, 'field': col} for col in df.columns],
        'rowData': df.to_dict(orient='records'),
        'rowSelection': 'multiple',
    }
    return cols

@ui.refreshable_method
def exp():
    df2 = export()
    return df2

df1 = crin()
df2 = export()



def get_unique(df, col):
    if df == "Cold_Store_In":
        data = cs()
        df2 = data[col].unique().tolist()
    else:
        data = exp()
        df2 = data[col].unique().tolist()    
    return df2

def input(label, options):
    ui.select(label=label, options=options)

def date_input(value):
    with ui.input('Date', value=value) as date:
        with ui.menu().props('no-parent-event') as menu:
            with ui.date().bind_value(date):
                with ui.row().classes('justify-end'):
                    ui.button('Close', on_click=menu.close).props('flat')
        with date.add_slot('append'):
            ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')

    return date       


def left_drawer(df):
       filters = {}
       with ui.column(align_items="stretch").classes("w-full"):
            sr_no_filter = ui.select(label="Sr_No", options=get_unique(df, "Sr_No"), 
                                    on_change=lambda e: filters.update({"Sr_No": e.value}), clearable=True, multiple=True)
            comp_filter = ui.select(label="Company", options=get_unique(df, "Company"), 
                                    on_change=lambda e: filters.update({"Company": e.value}), clearable=True, multiple=True)
            item_filter = ui.select(label="Item", options=get_unique(df, "Item"), 
                                    on_change=lambda e: filters.update({"Item": e.value}), clearable=True, multiple=True)
            type_filter = ui.select(label="Type", options=get_unique(df, "Type"),  clearable=True, multiple=True ,
                                    on_change=lambda e: filters.update({"Type": e.value}))
            size_filter = ui.select(label="Size", options=get_unique(df, "Size"), clearable=True, multiple=True, 
                                    on_change=lambda e: filters.update({"Size": e.value}))
            conversion_filter = ui.select(label="Conversion", options=get_unique(df, "Conversion"), clearable=True, multiple=True, 
                                    on_change=lambda e: filters.update({"Conversion": e.value}))
            form_filter = ui.select(label="Form_Type", options=get_unique(df, "Form_Type"), clearable=True, multiple=True, 
                                    on_change=lambda e: filters.update({"Form_Type": e.value}))
            freez_filter = ui.select(label="Freezing_Type", options=get_unique(df, "Freezing_Types"), clearable=True, multiple=True, 
                                    on_change=lambda e: filters.update({"Freezing_Types": e.value}))
            



def filter_dataframe(df, filters):
    filtered_df = df.copy()  # Use a copy to avoid modifying the original DataFrame
    text_columns = ["Company", "Item", "Type", "Size", "Fi_No"]
    numeric_columns = ["Sr_No", "Conversion"]

    for col, filter_values in filters.items():
        # Skip filtering if filter_values is empty or None
        if not filter_values:
            continue

        if col in text_columns:
            # Ensure filter_values is a list for text columns
            if isinstance(filter_values, str):
                filter_values = [filter_values]
            filtered_df = filtered_df.loc[filtered_df[col].str.contains('|'.join(filter_values), case=False, na=False)]
        elif col in numeric_columns:
            # Ensure filter_values is a list for numeric columns
            if not isinstance(filter_values, list):
                filter_values = [filter_values]
            filtered_df = filtered_df.loc[filtered_df[col].isin(filter_values)]
        elif col == "Date":
            # Handle date range filtering
            start_date, end_date = filter_values
            filtered_df = filtered_df.loc[(filtered_df["Date"] >= start_date) & (filtered_df["Date"] <= end_date)]

    return filtered_df




def on_filter(container, filters):
    cs.refresh
    tables.refresh
    a = filter_dataframe(cs(), filters)
    
    #container = ui.card().classes("w-full")
    with container:
        container.clear()
        #container.clear
        tables.refresh
        tables(a)

def on_filter2(container, filters):
    cs.refresh
    tables.refresh
    
    b = filter_dataframe(exp(), filters)
    #container = ui.card().classes("w-full")
    with container:
        container.clear()
        #container.clear
        tables.refresh
        tables(b)


def show_cool(container, filters):
    filters_for_data = {key: value for key, value in filters.items() if key != "Sr_No"}
    data = filter_dataframe(cs(), filters_for_data)
    data2 = filter_dataframe(exp(), filters)
    with container:
        container.clear()
    
        cool(data, data2)

        

def edit_modal(df, id, table):
    data1 = edit_form(df=df, id=id, table=table)
    data = data1.iloc[0]
    
    with ui.dialog(value=True).classes("w-full") as edit_dialog, ui.card().classes("w-full"):
            h = ui.input("Sr_No", value=data["Sr_No"]).classes("w-full")

            i = date_input(value=data["Date"])

            a = ui.input(label="Company", value=data["Company"]).classes("w-full")
            b = ui.input(label="Item",  value=data["Item"]).classes("w-full")
            c = ui.input(label="Type").classes("w-full")
            d = ui.input(label="Size", value=data["Size"]).classes("w-full")
            e = ui.input(label="Conversion", value=data["Conversion"]).classes("w-full")
            f = ui.input(label="Form_Type", value=data["Form_Type"]).classes("w-full")
            g = ui.input(label="Freezing_Types", value=data["Freezing_Types"]).classes("w-full")
            k = ui.input("Total_Mc", value=data["Total_Mc"]).classes("w-full")
            j = ui.input("Total_Kg", value=data["Total_Kg"]).classes("w-full")
            
            
            

            ui.button("submit", on_click=lambda : update_row(id=id, Sr_No=h.value, Fi_No=0, Date=i.value, Form_Type=f.value, Company=a.value, Item=b.value, Type=c.value, Size=d.value,Conversion=e.value, Total_Mc=k.value, Total_Kg=j.value, Freezing_Type=g.value, Remark=0, table=table ))
            ui.button("close", on_click=edit_dialog.close)


def edit_modal_exp(df, id, table):
    data1 = edit_form(df=df, id=id, table=table)
    data = data1.iloc[0]
    
    with ui.dialog(value=True).classes("w-full") as edit_dialog, ui.card().classes("w-full"):
            h = ui.input("Sr_No", value=data["Sr_No"]).classes("w-full")
            

            i = date_input(value=data["Date"])

            a = ui.input(label="Company", value=data["Company"]).classes("w-full")
            b = ui.input(label="Item",  value=data["Item"]).classes("w-full")
            c = ui.input(label="Type").classes("w-full")
            d = ui.input(label="Size", value=data["Size"]).classes("w-full")
            e = ui.input(label="Conversion", value=data["Conversion"]).classes("w-full")
            f = ui.input(label="Form_Type", value=data["Form_Type"]).classes("w-full")
            g = ui.input(label="Freezing_Types", value=data["Freezing_Types"]).classes("w-full")
            k = ui.input("Total_Mc", value=data["Total_Mc"]).classes("w-full")
            j = ui.input("Total_Kg", value=data["Total_Kg"]).classes("w-full")
            
            
            

            ui.button("submit", on_click=lambda : update_row(id=id, Sr_No=h.value, Fi_No=0, Date=i.value, Form_Type=f.value, Company=a.value, Item=b.value, Type=c.value, Size=d.value,Conversion=e.value, Total_Mc=k.value, Total_Kg=j.value, Freezing_Type=g.value, Remark=0, table=table ))
            ui.button("close", on_click=edit_dialog.close)            

                        
def navbar(container, container2, container3):
    with ui.header():
        navigation = ui.row()
        ui.link("Home", main)
        ui.link("Analysis", analysis_page)
        
     
        ui.button("Show Filters", on_click=lambda :right_drawer.toggle())
    with ui.left_drawer(fixed=True, bottom_corner=True, value=False).classes("w-full") as right_drawer:
        with ui.column().classes("w-full"):
            with ui.card().classes("w-full"):
                filteringUI(cs(),container, "Cold_Store_In")
            with ui.card().classes("w-full"):
                filteringUI(exp(),container2, "Cold_Store_Out")
            with ui.card().classes("w-full"):    
                filteringUI(exp(), container3, "Auto_Calculate")





def filteringUI(df, container, table):
    cols = df.columns.to_list()
    text_columns = ["Company", "Item", "Type", "Size", "Fi_No"]
    Numeric = ["Sr_No", "Conversion"]
    sum_columns = ["Total_Mc", "Total_Kg"]
    filters = {}

    with ui.expansion(f"Filter for {table}").classes("w-full"):
        with ui.column(align_items="stretch").classes("w-full"):
            sr_no_filter = ui.select(label="Sr_No", options=get_unique(table, "Sr_No"), 
                                    on_change=lambda e: filters.update({"Sr_No": e.value}), clearable=True, multiple=True)
            comp_filter = ui.select(label="Company", options=get_unique(table, "Company"), 
                                    on_change=lambda e: filters.update({"Company": e.value}), clearable=True, multiple=True)
            item_filter = ui.select(label="Item", options=get_unique(table, "Item"), 
                                    on_change=lambda e: filters.update({"Item": e.value}), clearable=True, multiple=True)
            type_filter = ui.select(label="Type", options=get_unique(table, "Type"),  clearable=True, multiple=True ,
                                    on_change=lambda e: filters.update({"Type": e.value}))
            size_filter = ui.select(label="Size", options=get_unique(table, "Size"), clearable=True, multiple=True, 
                                    on_change=lambda e: filters.update({"Size": e.value}))
            conversion_filter = ui.select(label="Conversion", options=get_unique(table, "Conversion"), clearable=True, multiple=True, 
                                    on_change=lambda e: filters.update({"Conversion": e.value}))
            form_filter = ui.select(label="Form_Type", options=get_unique(table, "Form_Type"), clearable=True, multiple=True, 
                                    on_change=lambda e: filters.update({"Form_Type": e.value}))
            freez_filter = ui.select(label="Freezing_Type", options=get_unique(table, "Freezing_Types"), clearable=True, multiple=True, 
                                    on_change=lambda e: filters.update({"Freezing_Types": e.value}))

    
    with ui.row().classes("w-full h-full"):    
        if table == "Cold_Store_In":                    
            ui.button("filter", on_click=lambda: on_filter(container, filters))
        elif table == "Cold_Store_Out":
            ui.button("filter", on_click=lambda :on_filter2(container, filters))  
        elif table == "Auto_Calculate":
            ui.button("filter", on_click=lambda : show_cool(container, filters) )      
        
        
     
    
    
def edit_form(df, id, table):
    
        Id = id
        data = df[df["ID"] == Id]
        
        return data
        
def multiply(a, b):
    mu = pd.to_numeric(a) * pd.to_numeric(b)
    return mu       



def dialog():
    @ui.refreshable       
    def total_mc(lists):
        
        tmc.clear()
        for i in lists:
        
            with tmc:
                ui.input(label=f"Total_MC for {i}", on_change=lambda e, s=i: update_total_mc(s, e.value)).classes("w-full")
              

    total_mc_values = {}
    def update_total_mc(size, value):
        total_mc_values[size] = float(value) if value else 0              
    with ui.dialog().classes("w-full") as dialog, ui.card().classes("w-full"):
        ui.label("Cold_Store_Form")
        h = ui.input("Sr_No").classes("w-full")
        i = date_input(value=datetime.datetime.now())

        a = ui.select(label="Company", options=get_unique("Cold_Store_In", "Company"), clearable=True).classes("w-full")
        b = ui.select(label="Item", options=get_unique("Cold_Store_In", "Item"), clearable=True).classes("w-full")
        c = ui.select(label="Type", options=get_unique("Cold_Store_In", "Type"), clearable=True).classes("w-full")
        d = ui.select(label="Size", options=get_unique("Cold_Store_In", "Size"), on_change=lambda : total_mc(d.value), multiple=True, clearable=True).classes("w-full")
        
        tmc = ui.column()
        
           
        e = ui.select(label="Conversion", options=get_unique("Cold_Store_In", "Conversion"), clearable=True).classes("w-full")
        f = ui.select(label="Form_Type", options=get_unique("Cold_Store_In", "Form_Type"), clearable=True).classes("w-full")
        g = ui.select(label="Freezing_Types", options=get_unique("Cold_Store_In", "Freezing_Types"), clearable=True, new_value_mode="add").classes("w-full")
        

        def update():
             for size, total_mc in total_mc_values.items():
                kg = multiply(e.value, total_mc)  # Replace '1' with actual input value
                add_row(session=connect_to_db(), a=h.value, b=0, c=i.value, l=f.value, d=a.value, e=b.value, f=c.value, g=size, h=e.value, i=total_mc, j=kg, k=g.value, m=0)
                tables.refresh()
                

        
        
        

        ui.button("submit", on_click=lambda : update())
        ui.button("close", on_click=dialog.close)
    ui.button("Add", on_click=dialog.open)

    

@ui.refreshable_method
def tables(df1):
    
    

    with ui.column().classes("w-full h-full").style("height: 700px"):
        with ui.card().style("align-self:flex-end;").classes("w-full h-full"):
            with ui.row():
                ui.label("Cold_Store")
                dialog()
                
                metric_card(df1)
            tb = ui.aggrid(cols(df1), auto_size_columns=False).classes("w-full h-full")
            async def show(option):
                rows = await tb.get_selected_rows()
                if rows:
                    for row in rows:
                        ui.notify(f"{row['ID']}")
                        if option == "delete":
                            delete_rows(connect_to_db(), ids_to_delete=row["ID"], data="crin")
                            tables.refresh
                        if option == "edit":
                            edit_modal(cs(), id=int(row["ID"]), table="crin")   
                            
                       
                        
                                
            with ui.row():
                ui.button("delete", on_click=lambda: show("delete"))
                ui.button("edit", on_click=lambda : show("edit"))


def table2(df2):            
        @ui.refreshable       
        def total_mc_exp(lists):
            
            tmc.clear()
            for i in lists:
            
                with tmc:
                    ui.input(label=f"Total_MC for {i}", on_change=lambda e, s=i: update_total_mc_exp(s, e.value)).classes("w-full")
                    

        total_mc_values_exp = {}
        def update_total_mc_exp(size, value):
            total_mc_values_exp[size] = float(value) if value else 0              
        with ui.dialog().classes("w-full") as exp_dialog, ui.card().classes("w-full"):
            ui.label("Export_From")
            h = ui.input("Sr_No").classes("w-full")
            i = date_input(value=datetime.datetime.now())

            a = ui.select(label="Company", options=get_unique("exp", "Company")).classes("w-full")
            b = ui.select(label="Item", options=get_unique("exp", "Item")).classes("w-full")
            c = ui.select(label="Type", options=get_unique("exp", "Type")).classes("w-full")
            d = ui.select(label="Size", options=get_unique("exp", "Size"), on_change=lambda : total_mc_exp(d.value), multiple=True).classes("w-full")
            
            tmc = ui.column()
            
                
            e = ui.select(label="Conversion", options=get_unique("exp", "Conversion")).classes("w-full")
            f = ui.select(label="Form_Type", options=get_unique("exp", "Form_Type")).classes("w-full")
            g = ui.select(label="Freezing_Types", options=get_unique("exp", "Freezing_Types")).classes("w-full")
            k = ui.input("Total_Mc").classes("w-full")
            j = ui.input("Total_Kg").classes("w-full")

            def update():
                    for size, total_mc in total_mc_values_exp.items():
                        kg = multiply(e.value, total_mc)  # Replace '1' with actual input value
                        add_row_exp(session=connect_to_db(), a=h.value, b=0, c=i.value, l=f.value, d=a.value, e=b.value, f=c.value, g=size, h=e.value, i=total_mc, j=kg, k=g.value, m=0)
                    

            
            
            
            
            ui.button("submit", on_click=lambda : update())
            ui.button("close", on_click=exp_dialog.close)    
            
        with ui.card().classes("w-full h-full").style("height : 700px"):
            with ui.row():
                ui.link_target("#Export")
                ui.label("Export")
                ui.button("add", on_click=exp_dialog.open).style("margin-left : 1000px")
                
                metric_card(df2)
            tb2 = ui.aggrid(cols(df2), auto_size_columns=True).classes("w-full h-full")
            async def show_exp(option):
                rows = await tb2.get_selected_rows()
                if rows:
                    for row in rows:
                        ui.notify(f"{row['ID']}")
                        if option == "delete":
                            delete_export_in_rows(connect_to_db(), ids_to_delete=row["ID"])
                            tables.refresh
                        if option == "edit":
                            edit_modal(exp(), id=int(row["ID"]), table="export")   
                            
                       
                        
                                
            with ui.row():
                ui.button("delete", on_click=lambda: show_exp("delete"))
                ui.button("edit", on_click=lambda : show_exp("edit"))

        
    
@ui.page("/analysis")
def analysis_page():
    navbar()
    analysis()

@ui.page("/", dark=True)
def main():
    
    ui.colors(
    primary="#78c2ad",
    secondary="#dee2e6",
)
       
        
        
    
    container = ui.card().classes("w-full h-full") 
    container2 = ui.card().classes ("w-full h-full")
    container3 = ui.card().classes("w-full h-full").style("height : 2000px")
    navbar(container, container2, container3)
     
    with container:
        tables(cs())
    with container2:    
        table2(exp())
    with container3:
        cool(cs(), exp())     
    #filteringUI(cs())   
    
            









ui.run(native=True, on_air="FnygfC0A7CHm8u1s")








