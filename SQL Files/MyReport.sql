Select sum(The_Outstandingvalues.Value_paid) as PaidValue,
Agent.Person_Name as Agent,
UserName.Person_Name as UserName,
The_Outstandingvalues.Date_paid,
The_Outstandingvalues.Item_Add, 
The_Outstandingvalues.Outstandingvalues_No, 
The_Outstandingvalues.Type_Payment, 
(select sum(The_Outstandingvalues.Value_paid) from The_Outstandingvalues Where Type_Payment = 'ÇÏÝÚáí') As ReportTotal
from The_Outstandingvalues

Inner join The_Persons Agent on Agent.Person_No = The_Outstandingvalues.Person_No
Inner join The_Persons UserName on UserName.Person_No = The_Outstandingvalues.User_No

Where Type_Payment = 'ÇÏÝÚáí'

Group by Agent.Person_Name, 
UserName.Person_Name, 
The_Outstandingvalues.Date_paid,
The_Outstandingvalues.Item_Add, 
The_Outstandingvalues.Outstandingvalues_No, 
The_Outstandingvalues.Type_Payment