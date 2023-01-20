SELECT Sum(The_Outstandingvalues.Value_paid) AS SumValue_paid, 
The_Persons.Person_Name, 
The_Persons_1.Person_Name AS User_Name, 
The_Outstandingvalues.Date_paid, 
The_Outstandingvalues.Item_Add, 
The_Outstandingvalues.Outstandingvalues_No, 
The_Outstandingvalues.Type_Payment 
FROM The_Persons AS The_Persons_1 
INNER JOIN (The_Outstandingvalues INNER JOIN The_Persons 
ON The_Outstandingvalues.Person_No = The_Persons.Person_No) 
ON The_Persons_1.Person_No = The_Outstandingvalues.User_No 
GROUP BY The_Persons.Person_Name, 
The_Persons_1.Person_Name, 
The_Outstandingvalues.Date_paid, 
The_Outstandingvalues.Item_Add, 
The_Outstandingvalues.Account_No, 
The_Outstandingvalues.Outstandingvalues_No, 
The_Outstandingvalues.Type_Payment 
HAVING The_Persons_1.[Person_Name]='مدير النظام' 
and (The_Outstandingvalues.[Type_Payment]='خصم مسموح' 
Or The_Outstandingvalues.[Type_Payment]='خصم مكتسب') 
and The_Outstandingvalues.Date_paid='01/12/2023' and The_Outstandingvalues.[Account_No]=23