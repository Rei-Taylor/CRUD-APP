from nicegui import ui
import pandas as pd
from calculation import crin




balance_df = pd.DataFrame()


def get_error_rows(tb1, tb2):
        # Group by "Sr_No" and sum the "Quantity" for each group
        
        tb1_sum = tb1.groupby("Sr_No")["Total_Mc"].sum().reset_index()
        tb2_sum = tb2.groupby("Sr_No")["Total_Mc"].sum().reset_index()

        # Merge the two dataframes on "Sr_No" to compare quantities
        merged_df = pd.merge(tb1_sum, tb2_sum, on="Sr_No", suffixes=('_tb1', '_tb2'), how='outer')

        # Find rows where the quantities do not match
        unmatched_rows = merged_df[merged_df["Total_Mc_tb1"] != merged_df["Total_Mc_tb2"]]

        return unmatched_rows



def cool(df1, df2):
    df = pd.DataFrame(df1).sort_values(by=["Date"])
    df2 = pd.DataFrame(df2).sort_values(by=["Date"])
    fifo_table = pd.DataFrame(columns=["Sr_No","Date", "Ref_Date", "Company", "Item", "Type", "Size", "Conversion", "Total_Mc", "Total_Kg"])

    discrepancies = []
        
        # Implement FIFO logic
    for index, out_row in df2.iterrows():
            sr_no = out_row['Sr_No']
            company = out_row['Company']
            item = out_row['Item']
            item_type = out_row['Type']
            size = out_row['Size']
            Conversion = out_row['Conversion']

            quantity_needed = out_row['Total_Mc']
            
            date = out_row['Date']
            
            # Use loc with boolean indexing
            input_records = df.loc[
                (df['Item'] == item) & 
                (df['Type'] == item_type) & 
                (df['Company'] == company) & 
                (df['Size'] == size) & 
                (df['Conversion'] == Conversion)
            ]
            
            total_available_quantity = input_records['Total_Mc'].sum()
            
            
            if quantity_needed > total_available_quantity:
                    discrepancies.append({
                    "Date": date,
                    "Company": company,
                    "Item": item,
                    "Type": item_type,
                    "Size": size,
                    "Conversion": Conversion,
                    "Quantity_Requested": quantity_needed,
                    "Quantity_Available": total_available_quantity
                })
            
            for in_index, in_row in input_records.iterrows():
                if pd.to_numeric(quantity_needed) <= 0:
                    
                    break
                
                available_quantity = in_row['Total_Mc']
                
                ref_date = in_row['Date']
                
                # Ensure correct date comparison
                if pd.to_numeric(quantity_needed) == 0:
                    
                    if pd.to_datetime(date) < pd.to_datetime(ref_date):
                        discrepancies.append({
                            "Sr_No": sr_no,
                            "Date": date,
                            "Company": company,
                            "Ref_Date": ref_date,
                            "Item": item,
                            "Type": item_type,
                            "Size": size,
                            "Conversion": Conversion,
                            "Total_Mc": quantity_needed,
                            "Issue": "Out Date is before In Date"
                        })
                        continue
                
                if available_quantity > 0:
                    quantity_to_use = min(available_quantity, quantity_needed)
                    
                    quantity_needed -= quantity_to_use
                    
                    # Record the transaction in the FIFO table
                    fifo_table = fifo_table._append({
                        "Date": date,
                        "Sr_No": sr_no,
                        "Ref_Date": ref_date,
                        "Company": company,
                        "Item": item,
                        "Type": item_type,
                        "Size": size,
                        "Conversion": Conversion,
                        "Total_Mc": quantity_to_use,
                        "Total_Kg": pd.to_numeric(Conversion) * pd.to_numeric(quantity_to_use)
                    }, ignore_index=True)
                    
                    # Update the input record's quantity
                    df.at[in_index, 'Total_Mc'] -= quantity_to_use

               
    with ui.row().classes("w-full"):
        ui.label("Export")
        metric_card(fifo_table)
    ui.aggrid.from_pandas(fifo_table).classes("w-full h-full")
    if discrepancies:
        ui.label("Discrepancies found:")
        ui.aggrid.from_pandas(pd.DataFrame(discrepancies)).classes("w-full h-full")
            
            # Suggestion for discrepancies
    suggestions = []
    for discrepancy in discrepancies:
                
                # Check for different size and type but same item
                similar_items = df.loc[
                    (df['Item'] == discrepancy['Item']) & 
                    ((df['Size'] != discrepancy['Size']) | (df['Type'] != discrepancy['Type']) | (df['Date'] < discrepancy['Date']))
                    & ((df["Company"] == discrepancy["Company"]))

                ]
                if not similar_items.empty:
                    suggestions.append({
                        "Suggestion": "Consider reviewing items with different 'Size' or 'Type' but same 'Item'.",
                        "Item": discrepancy["Item"],
                        "Company": discrepancy["Company"]
                    })
            
    if suggestions:
                ui.label("Suggestions:")
                s_df = pd.DataFrame(similar_items)
                suggestions_df = s_df[s_df["Total_Mc"] != 0]
                
                ui.aggrid.from_pandas(pd.DataFrame(suggestions_df)).classes("w-full h-full")
    else:
                ui.label("No discrepancies found.") 

   
    wrong = get_error_rows(df2, fifo_table)
    ui.aggrid.from_pandas(wrong).classes("w-full h-full")  


    balance_table = df.groupby(['Sr_No', 'Date', 'Company', 'Item', 'Type', 'Size', 'Conversion', 'Total_Kg'], as_index=False)['Total_Mc'].sum()
    balance_df.add(balance_table)
    with ui.row().classes("w-full"):
        ui.label("Balance Table")
        metric_card(balance_table)
    ui.aggrid.from_pandas(balance_table).classes("w-full h-full")
        

def analysis_result(filtered_df, unique_columns, container):
    filtered_df['Total_Mc'] = pd.to_numeric(filtered_df['Total_Mc'], errors='coerce')
    filtered_df['Total_Kg'] = pd.to_numeric(filtered_df['Total_Kg'], errors='coerce')
    grouped_df = filtered_df.groupby(unique_columns)[['Total_Mc', 'Total_Kg']].sum().reset_index()
    with container:
        container.clear()
        ui.label("Analysis Results:")   
        ui.aggrid.from_pandas(grouped_df)

def analysis_calc(filtered_df, analyze):
    df = pd.DataFrame(filtered_df)
    with ui.expansion("Data Analysis"):
            ui.label("Data Analysis")

            # Select columns for unique values
            unique_columns = ui.select(label="Select Columns for Unique Values", options=df.columns.to_list())

            # Analyze Data Button
            ui.button("Analyze Data", on_click=lambda : analysis_result(filtered_df, unique_columns.value, analyze))

                
                    # Convert sum columns to numeric
                    

                    # Convert the analysis result to Excel
                    


def metric_card(df):
        sum_columns = ["Total_Mc", "Total_Kg"]
        # Calculate the sum for each column in self.sum_columns
        
        t_MC = pd.to_numeric(df["Total_Mc"], errors='coerce').sum()
        t_Kg = pd.to_numeric(df["Total_Kg"], errors="coerce").sum()
        with ui.row().style("margin-right: 100px"):
               ui.label(f"Total Mc : {t_MC}")
               ui.label(f"Total_Kg : {t_Kg}").style("align-self:flex-end; display:flex; justify-content:end; align-items:end; flex-wrap:wrap;")



      
          




