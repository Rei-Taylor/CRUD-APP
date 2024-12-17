from nicegui import ui 
import pandas as pd
from calculation import crin, export


def navbar():
    with ui.header():
        with ui.row(align_items="stretch").classes("w-full"):
            ui.label("This is navbar").classes("ml-64")
            
            with ui.dropdown_button(text="DropDown").classes("ml-64"):
                ui.item("A", on_click=lambda e : ui.notify(e  ))
                ui.item("B")
        

data = crin()

df = pd.DataFrame(data)

# Aggregate data
aggregated_data = df.groupby("Company")["Total_Mc"].sum().reset_index()

# Prepare data for the pie chart
chart_data = [
    {"value": row["Total_Mc"], "name": row["Company"]}
    for _, row in aggregated_data.iterrows()
]

# Pie chart configuration
chart_options = {
    "tooltip": {"trigger": "item"},
    "legend": {"top": "5%", "left": "center"},
    "series": [
        {
            "name": "Company Market Cap",
            "type": "pie",
            "radius": ["40%", "70%"],
            "avoidLabelOverlap": True,
            "itemStyle": {
                "borderRadius": 10,
                "borderColor": "#fff",
                "borderWidth": 2,
            },
            "label": {
                "show": True,
                "formatter": "{b}: {d}%",  # Show the company name and percentage
                "position": "outside",
                "fontSize": 12,
            },
            "emphasis": {
                "label": {
                    "show": True,
                    "fontSize": "16",
                    "fontWeight": "bold"
                }
            },
            "labelLine": {
                "show": True
            },
            "data": chart_data
        }
    ]
}




def analysis():
    with ui.grid(columns=5).classes("w-full"):
        ui.echart(options=chart_options)
        ui.echart(options=chart_options)


   