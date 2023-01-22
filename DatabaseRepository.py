import pyodbc
import pandas
import socket

conn = pyodbc.connect("Driver={SQL Server};Server=GH93ST\SQLExpress; Database=AlmohasebSQL; User Id=ah; password=123456")
cursor = conn.cursor()

def GetAllUsers():
    df = pandas.read_sql("select * from the_persons where person_kind=1", conn)
    dfjson = df.to_json(orient="records", date_format="iso", force_ascii=False)
    return dfjson

def GetAllAgents():
    df = pandas.read_sql("""select * from the_persons where person_kind=2
                        or person_kind=3""", conn)
    dfjson = df.to_json(orient="records", date_format="iso", force_ascii=False)
    return dfjson

def GetAgentByName(name):
    df = pandas.read_sql(f"""select * from the_persons where (person_kind=2
                        or person_kind=3) and person_name like '%{name}%'""", conn)
    dfjson = df.to_json(orient="records", date_format="iso", force_ascii=False)
    return dfjson

def GetCashBalance(d1, d2):
    df = pandas.read_sql(f"""
    select type_payment, sum(Value_paid) as TotalValue from The_Outstandingvalues
    where Date_paid >= '{d1}' and Date_paid <= '{d2}'
    group by Type_Payment
    """, conn)
    dfjson = df.to_json(orient='records', date_format='iso', force_ascii=False)
    return dfjson

def GetCashStatement(d1, d2):
    df = pandas.read_sql(f"""
        select date_paid, Movementrestrictions_No as EntryNumber, Value_paid
		type_payment, Users.Person_Name, Debit.Person_Name as Agent, Credit.Account_Name as Account
        from The_Outstandingvalues
        inner join The_Persons Users on Users.Person_No = The_Outstandingvalues.User_No
        inner join The_Persons Debit on Debit.Person_No = The_Outstandingvalues.Person_No
        inner join The_Account Credit on Credit.Account_No = The_Outstandingvalues.Account_No
        where Date_paid >= '{d1}' and Date_paid <= '{d2}'
        """, conn)
    dfjson = df.to_json(orient='records', date_format='iso', force_ascii=False)
    return dfjson

def GetCreditBalance():
    df = pandas.read_sql(f"""select 
                        Person_Name as Agent,
                        Sum((Item_Quntity / Old_Unit) * Charge_Value) as Debit,
                        sum(The_Outstandingvalues.Value_paid) as Credit,
                        sum((Item_Quntity / Old_Unit) * Charge_Value) + sum(The_Outstandingvalues.Value_paid) as Balance
                        from The_Movementrestrictions
                        inner join The_Details on The_Details.Movementrestrictions_No = The_Movementrestrictions.Movementrestrictions_No
                        inner join The_Items on The_Items.Item_No = The_Details.Item_No
                        inner join The_Persons on The_Persons.Person_No = The_Movementrestrictions.Person_No
                        left join The_Outstandingvalues on The_Outstandingvalues.Movementrestrictions_No = The_Movementrestrictions.Movementrestrictions_No
                        where Person_Kind = 3
                        group by Person_Name
                        order by Balance desc""", conn)
    dfjson = df.to_json(orient="records", date_format="iso", force_ascii=False)
    return dfjson

def GetDebitBalance():
    df = pandas.read_sql(f"""select 
                        Person_Name as Agent,
                        Sum((Item_Quntity / Old_Unit) * Charge_Value) as Debit,
                        sum(The_Outstandingvalues.Value_paid) as Credit,
                        sum((Item_Quntity / Old_Unit) * Charge_Value) - sum(The_Outstandingvalues.Value_paid) as Balance
                        from The_Movementrestrictions
                        inner join The_Details on The_Details.Movementrestrictions_No = The_Movementrestrictions.Movementrestrictions_No
                        inner join The_Items on The_Items.Item_No = The_Details.Item_No
                        inner join The_Persons on The_Persons.Person_No = The_Movementrestrictions.Person_No
                        left join The_Outstandingvalues on The_Outstandingvalues.Movementrestrictions_No = The_Movementrestrictions.Movementrestrictions_No
                        where Person_Kind = 2
                        group by Person_Name
                        order by Balance desc""", conn)
    dfjson = df.to_json(orient="records", date_format="iso", force_ascii=False)
    return dfjson

def GetAgentStatement(date1, date2, agent):
    df = pandas.read_sql(f"""select The_Details.Movementrestrictions_No, The_Movementrestrictions.Movementrestrictions_Date, Users.Person_Name as [User],
                            Barcode, Scientific_Name, Charge_Value,
                            (The_Details.Item_Quntity / The_Items.Old_Unit) as Quantity, Agents.Person_Name, sum(The_Outstandingvalues.Value_paid) as Credit
                            from The_Details
                            inner join The_Movementrestrictions on The_Movementrestrictions.Movementrestrictions_No = The_Details.Movementrestrictions_No
                            inner join The_Persons Agents on Agents.Person_No = The_Movementrestrictions.Person_No
                            inner join The_Persons Users on Users.Person_No = The_Movementrestrictions.User_No
                            inner join The_Items on The_Items.Item_No = The_Details.Item_No
                            left outer join The_Outstandingvalues on The_Outstandingvalues.Movementrestrictions_No = The_Details.Movementrestrictions_No
                            where Agents.Person_Name like '{agent}'
                            and (The_Movementrestrictions.Movementrestrictions_Date >= '{date1}' and The_Movementrestrictions.Movementrestrictions_Date <= '{date2}')
                            group by The_Details.Movementrestrictions_No, The_Details.Item_No, The_Details.Barcode,
                            The_Items.Scientific_Name, The_Details.Charge_Value, The_Details.Item_Quntity, The_Items.Old_Unit,
                            Agents.Person_Name, The_Movementrestrictions.Movementrestrictions_Date, Users.Person_Name""", conn)
    dfjason = df.to_json(orient='records', date_format='iso', force_ascii=False)
    return dfjason

def GetItemInventory():
    df = pandas.read_sql(f"""select The_Barcode.Barcode, The_Items.Scientific_Name, The_Group.Group_Name, The_ItemDetails.Exp_date, item_cost,
                        (CONVERT(int,The_ItemDetails.Item_Quantity) / CONVERT(int,The_Items.Old_Unit)) as BoxQuantity,
                        (CONVERT(decimal,The_ItemDetails.Item_Quantity) % CONVERT(decimal,The_Items.Old_Unit)) as SingleQuantity,
                        (CONVERT(int,The_ItemDetails.Item_Quantity) / CONVERT(int,The_Items.Old_Unit)) * The_ItemDetails.Item_Cost  +
                        (CONVERT(decimal,The_ItemDetails.Item_Quantity) % CONVERT(decimal,The_Items.Old_Unit)) * (The_ItemDetails.Item_Cost / The_Items.Old_Unit) as TotalCost,
                        the_Charge.Charge_Value as BoxSellPrice, the_Charge.Charge_Value / The_Items.Old_Unit as SingleSellPrice,
                        The_ItemDetails.Last_Movement
                        from The_ItemDetails
                        inner join The_Items on The_Items.Item_No = The_ItemDetails.Item_No
                        inner join the_Charge on the_Charge.ItemDetails_No = The_ItemDetails.ItemDetails_No
                        inner join The_Barcode on The_Barcode.Item_No = The_ItemDetails.Item_No
                        inner join The_Group on The_Group.Group_No = The_Items.Group_No
                        where The_ItemDetails.Item_Quantity > 0""", conn)
    dfjason = df.to_json(orient='records', date_format='iso', force_ascii=False)
    return dfjason

def GetSalesProfit(date1, date2):
    df = pandas.read_sql(f"""
                            select entries.Movementrestrictions_Date, users.Person_Name,
                            sum((The_Details.Charge_Value / The_Items.Old_Unit) * The_Details.Item_Quntity) as SoldItems,
                            sum((The_Details.Item_Cost / The_Items.Old_Unit) * The_Details.Item_Quntity) as SoldItemsCost,
                            (sum((The_Details.Charge_Value / The_Items.Old_Unit) * The_Details.Item_Quntity) - sum((The_Details.Item_Cost / The_Items.Old_Unit) * The_Details.Item_Quntity)) as Profit
                            from the_details
                            inner join the_movementrestrictions entries on entries.MovementRestrictions_no = the_details.MovementRestrictions_No
                            inner join The_Items on The_Items.Item_No = The_Details.Item_No
                            inner join The_Persons users on users.Person_No = entries.User_No
                            where (entries.Account_No = 1)
                            and entries.Movementrestrictions_Date >= '{date1}' and entries.Movementrestrictions_Date <= '{date2}'
                            group by entries.Movementrestrictions_Date, users.Person_Name""", conn)
    dfjason = df.to_json(orient='records', date_format='iso', force_ascii=False)
    return dfjason

def AddMovementRestriction(person_no, Purchase_invoice, Movementrestrictions_Date, User_No):
    com_name = socket.gethostname()
    cursor.execute(f"exec dbo.AddMoveRstr {person_no}, '{Purchase_invoice}', '{Movementrestrictions_Date}', {User_No}, '{com_name}'")
    cursor.commit()

def AddDetails(packaging, moverestno,item_no, charge_value, item_quantity, exp_date, computer_name, comment):
    cursor.execute(f"exec dbo.AddDetails {packaging}, {moverestno}, {item_no}, {charge_value}, {item_quantity}, '{exp_date}', '{computer_name}', '{comment}'")
    cursor.commit()

def AddAgent(person_name, person_add, person_tel, person_kind):
    cursor.execute(f"""Insert Into The_Persons(person_name, person_add, person_tel, person_kind)
                    Values('{person_name}', '{person_add}', '{person_tel}', {person_kind})""")
    cursor.commit()
