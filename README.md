# Azure Warehouse inventory 

## Description
Inventory system too keep track of hur much stock we have left in our warehouse.
Used through the command line interface.
The data is located in an Azure table storage which we can update as we please

Every start on the application will reset the balance of invetory to 0

### How to run
1. Open warehouse.py and run it
2. Enter any of the example commands shown below
- Example usage: 'Add 5' to add five items to stock"
- Example usage: 'Remove 5' to remove five items from stock"
- Example usage: 'Balance' to show stock amount"
- Example usage: 'Exit' to Exit the system"

## Dependencies
To continue development on this tool or to run it you need these installs below
```python
pip install azure-data-tables
pip install requests
```

### Connected resources
Azure table storage with one table named WarehouseTable
![image](https://user-images.githubusercontent.com/55485130/188272211-4b0ea104-b98c-4bf5-bd7f-3a7625bfa363.png)


### Ideas on how to improve for furute developers
For the future development i would recommend:
- Putting urls, sas keys etc in their own config folder. Or use microsofts keyvault for connection string storage
- Creating a virtual environment for the released product 
- Creating a GUI using QT Lib in python for more appealing visuals


### Additional comments
The reasoning behind using azure table storage instead of a lets say a SQL database is that the table storage is very cheap and fast to access. 
Since the requirement to keep track of one piece of data (the amount of items) i chose the table storage.

<br>
