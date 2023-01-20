SELECT Sum(The_Outstandingvalues.Value_paid) AS SumValue_paid, 
The_Persons.Person_Name, 
The_Persons_1.Person_Name AS UserName, 
The_Outstandingvalues.Date_paid, 
The_Outstandingvalues.Item_Add, 
The_Outstandingvalues.Outstandingvalues_No, 
The_Outstandingvalues.Type_Payment 
FROM The_Persons AS The_Persons_1
INNER JOIN (The_Outstandingvalues INNER JOIN The_Persons 
ON The_Outstandingvalues.Person_No = The_Persons.Person_No) 
ON The_Persons_1.Person_No = The_Outstandingvalues.User_No
Where Type_Payment <> 'نقداً' 
GROUP BY The_Persons.Person_Name, 
The_Persons_1.Person_Name, 
The_Outstandingvalues.Date_paid, 
The_Outstandingvalues.Item_Add, 
The_Outstandingvalues.Account_No, 
The_Outstandingvalues.Outstandingvalues_No, 
The_Outstandingvalues.Type_Payment
