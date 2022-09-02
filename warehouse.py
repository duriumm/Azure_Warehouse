import json
import requests
import xmltodict
from azure.data.tables import TableServiceClient
from azure.data.tables import TableClient
from azure.data.tables import UpdateMode
import os


MY_TABLE_NAME = "WarehouseTable"
MY_PARTITION_KEY = "Warehouse"
MY_ROW_KEY = ""
MY_ENDPOINT = "https://lassesstorageaccount.table.core.windows.net/?sv=2021-06-08&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2022-12-01T00:44:48Z&st=2022-09-02T15:44:48Z&spr=https&sig=vgvmtB5Ey%2BCSEAmCCFx8zLH17eRFrqlfUUBGFFPBn5E%3D"
clear = lambda: os.system('cls')

def initialize_warehouse_balance_to_zero(table_client):
  entity_to_add = {"PartitionKey": MY_PARTITION_KEY, "RowKey": MY_ROW_KEY, "Item_Balance": 0}
  table_client.update_entity(mode=UpdateMode.REPLACE, entity=entity_to_add)  

def get_item_balance_from_warehouse(table_client):
  got_entity = table_client.get_entity(partition_key=MY_PARTITION_KEY, row_key=MY_ROW_KEY)
  return got_entity["Item_Balance"]

def add_items_to_warehouse_stock(table_client, amount_to_add):
  entity_to_add = {"PartitionKey": MY_PARTITION_KEY, "RowKey": MY_ROW_KEY, "Item_Balance": get_item_balance_from_warehouse(table_client) + amount_to_add}
  table_client.update_entity(mode=UpdateMode.REPLACE, entity=entity_to_add)  
  
def remove_items_from_warehouse_stock(table_client, amount_to_remove):
  current_warehouse_balance = get_item_balance_from_warehouse(table_client) 
  if current_warehouse_balance - amount_to_remove < 0:
    print(f"You tried to remove {amount_to_remove} items but the warehouse stock only had {current_warehouse_balance} available, therefor {amount_to_remove - current_warehouse_balance * 1} item/s did not get removed")
    entity_to_add = {"PartitionKey": MY_PARTITION_KEY, "RowKey": MY_ROW_KEY, "Item_Balance": 0}
  else:
    entity_to_add = {"PartitionKey": MY_PARTITION_KEY, "RowKey": MY_ROW_KEY, "Item_Balance": current_warehouse_balance - amount_to_remove}
  
  table_client.update_entity(mode=UpdateMode.REPLACE, entity=entity_to_add)  



def main():
  service = TableServiceClient(endpoint=MY_ENDPOINT)
  table_client = service.get_table_client(table_name=MY_TABLE_NAME)
  initialize_warehouse_balance_to_zero(table_client)

  while True:
    

    print("Welcome to the W.I.S. - Warehouse Inventory System")
    print("These are the available commands you can use: \n")
    print("1. Adding items   ---------------------- -- Example usage: 'Add 5' to add five items to stock")
    print("2. Removing items ---------------------- -- Example usage: 'Remove 5' to remove five items from stock")
    print("3. Show current amount of items in stock -- Example usage: 'Balance' to show stock amount")
    print("4. Exit Warehouse Inventory System ----- -- Example usage: 'Exit' to Exit the system")

    print("Enter your choice below")

    user_input = input().lower()

    print("----------------------------------------------------------------------------------\n")
    print(f"User input was: {user_input}")
    splitted_user_input = user_input.split()
    print(f"Splitted User input was: {splitted_user_input}")
    if len(splitted_user_input) > 2:
      print("Invalid input, list len > 2 - try again")
    elif len(splitted_user_input) == 1:
      if splitted_user_input[0] == "balance":
        print("Trying to show warehouse balance")
        print(f"Warehouse item balance: {get_item_balance_from_warehouse(table_client)}")
      elif splitted_user_input[0] == "exit":
        return
    elif len(splitted_user_input) == 2:
      try: 
        splitted_user_input[1] = int(splitted_user_input[1])
      except:
        print(f"Could not convert input {splitted_user_input[1]} to integer")
      if not isinstance(splitted_user_input[1], int) or splitted_user_input[1] < 0:
        print("Invalid input, try again")

      if splitted_user_input[0] == "add":
        print("Trying to add items to warehouse")
        add_items_to_warehouse_stock(table_client, splitted_user_input[1])

      elif splitted_user_input[0] == "remove":
        print("Trying to remove items from warehouse")
        remove_items_from_warehouse_stock(table_client, splitted_user_input[1])

    print("Press any key to continue or type 'exit' to close application")
    user_input = input().lower()
    if user_input.lower() == "exit":
      return

    clear()

  #get_item_balance_from_warehouse(table_client)

  #print(f"Item balance in warehouse afterwards is: {get_item_balance_from_warehouse(table_client)}")
  # add_items_to_warehouse_stock(table_client, -555)
  # print(f"Item balance in warehouse after addition is: {get_item_balance_from_warehouse(table_client)}")

  # remove_items_from_warehouse_stock(table_client, 144)
  # print(f"Item balance in warehouse after subtraction is: {get_item_balance_from_warehouse(table_client)}")




if __name__ == '__main__':
  main()



  
