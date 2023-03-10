from flask import Flask, request
from waitress import serve
import DatabaseRepository as repo

app = Flask(__name__)

@app.route('/')
def Index():
    return 'Almohaseb3 V1 API By Mohammed Radwan, The Server Is Currently Up & Running'

@app.route('/GetAllUsers', methods=['GET'])
def GetAllUsers():
    return repo.GetAllUsers()

@app.route('/GetCashBalance', methods=['GET'])
def GetCahsBalance():
    Date1 = request.args.get('d1')
    Date2 = request.args.get('d2')
    return repo.GetCashBalance(Date1, Date2)

@app.route('/GetCashStatement', methods=['GET'])
def GetCashStatement():
    Date1 = request.args.get('d1')
    Date2 = request.args.get('d2')
    return repo.GetCashStatement(Date1, Date2)    

@app.route('/GetCreditBalance', methods=['GET'])
def GetCreditBalance():
    return repo.GetCreditBalance()

@app.route('/GetDebitBalance', methods=['GET'])
def GetDebitBalance():
    return repo.GetDebitBalance()

@app.route('/GetAgentStatement', methods=['GET'])
def GetAgentStatement():
    Date1 = request.args.get('d1')
    Date2 = request.args.get('d2')
    Agent = request.args.get('name')
    return repo.GetAgentStatement(Date1, Date2, Agent)

@app.route('/GetItemInventory', methods=['GET'])
def GetItemInventory():
    return repo.GetItemInventory()

@app.route('/GetSalesProfit', methods=['GET'])
def GetSalesProfit():
    Date1 = request.args.get('d1')
    Date2 = request.args.get('d2')
    return repo.GetSalesProfit(Date1, Date2)       

@app.route('/AddMovementRestriction', methods=['POST'])
def AddMovementRestriction():
    response = request.json
    
    person_no = response['person_no']
    Purchase_invoice = response['purchase_invoice']
    Movementrestrictions_Date = response['movementrestrictions_date']
    User_No = response['user_no']

    repo.AddMovementRestriction(person_no, Purchase_invoice, Movementrestrictions_Date, User_No)
    return response

@app.route('/AddDetails', methods=['POST'])
def AddDetails():
    response = request.json
    
    packaging = response['packaging']
    moverestno = response['moverestno']
    item_no = response['item_no']
    charge_value = response['charge_value']
    item_quantity = response['item_quantity']
    exp_date = response['exp_date']
    computer_name = response['computer_name']
    comment = response['comment']

    repo.AddDetails(packaging, moverestno, item_no, charge_value, item_quantity, exp_date, computer_name, comment)
    return response

@app.route('/AddAgent', methods=['POST'])
def AddAgent():
    response = request.json
    
    person_name = response['person_name']
    person_add = response['person_add']
    person_tel = response['person_tel']
    person_kind = response['person_kind']

    repo.AddAgent(person_name, person_add, person_tel, person_kind)
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
    #serve(app, host='0.0.0.0', port=8081)