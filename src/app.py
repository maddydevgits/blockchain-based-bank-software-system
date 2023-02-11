from flask import Flask,render_template,redirect,request,session
from web3 import Web3, HTTPProvider
import json

app=Flask(__name__)
app.secret_key="sacetb1"

def connect_blockchain_bank(acc): # connect with blockchain - bank contract
    blockchain='http://127.0.0.1:7545'
    web3=Web3(HTTPProvider(blockchain))
    if acc==0:
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path='../build/contracts/bank.json'
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']
        contract_address=contract_json['networks']['5777']['address']
    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    return(contract,web3)

def connect_blockchain_kyc(acc): # connect with blockchain - kyc contract
    blockchain='http://127.0.0.1:7545'
    web3=Web3(HTTPProvider(blockchain))
    if acc==0:
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path='../build/contracts/kyc.json'
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']
        contract_address=contract_json['networks']['5777']['address']
    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    return(contract,web3)

def connect_blockchain_loan(acc): # connect with blockchain - loan contract
    blockchain='http://127.0.0.1:7545'
    web3=Web3(HTTPProvider(blockchain))
    if acc==0:
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path='../build/contracts/loan.json'
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']
        contract_address=contract_json['networks']['5777']['address']
    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    return(contract,web3)

def connect_blockchain_transactions(acc): # connect with blockchain - transactions contract
    blockchain='http://127.0.0.1:7545'
    web3=Web3(HTTPProvider(blockchain))
    if acc==0:
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path='../build/contracts/transactions.json'
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']
        contract_address=contract_json['networks']['5777']['address']
    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    return(contract,web3)

@app.route('/')
def homePage():
    return render_template('index.html')

@app.route('/addcustomer')
def addcustomerPage():
    return render_template('AddCustomer.html')

@app.route('/addamount')
def addamountPage():
    return render_template('AddAmount.html')

@app.route('/addamountform',methods=['post'])
def addamountform():
    try:
        customer=request.form['customer']
        amount=int(request.form['amount'])
        print(customer,amount)
        contract,web3=connect_blockchain_kyc(0)
        tx_hash=contract.functions.addAmount(customer,amount).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return render_template('AddAmount.html',res='Amount Added')
    except:
        return render_template('AddAmount.html',err="Adding Amount Failed")

@app.route('/viewcustomers')
def viewcustomersPage():
    contract,web3=connect_blockchain_kyc(0)
    _customers,_names,_caddresses,_aadhars,_pans,_mobiles,_emails,_accounts,_amounts,_passwords=contract.functions.viewCustomers().call()
    print(_customers,_names,_caddresses,_aadhars,_pans,_mobiles,_emails,_accounts,_amounts,_passwords)
    data=[]
    for i in range(len(_customers)):
        dummy=[]
        dummy.append(_customers[i])
        dummy.append(_names[i])
        dummy.append(_caddresses[i])
        dummy.append(_aadhars[i])
        dummy.append(_pans[i])
        dummy.append(_mobiles[i])
        dummy.append(_emails[i])
        dummy.append(_accounts[i])
        dummy.append(_amounts[i])
        dummy.append(_passwords[i])
        data.append(dummy)

    return render_template('ViewCustomers.html',dashboard_data=data,len=len(data))

@app.route('/logout')
def logoutPage():
    session['username']=None
    return redirect('/')

@app.route('/addcustomerform',methods=['post'])
def addcustomerform():
    customer=request.form['customer']
    name=request.form['name']
    caddress=request.form['caddress']
    aadhar=request.form['aadhar']
    pan=request.form['pan']
    mobile=request.form['mobile']
    email=request.form['email']
    account=request.form['account']
    password=request.form['password']
    print(customer,name,caddress,aadhar,pan,mobile,email,account,password)
    try:
        contract,web3=connect_blockchain_kyc(0)
        tx_hash=contract.functions.addCustomer(customer,name,caddress,aadhar,pan,mobile,email,account,int(password)).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return render_template('AddCustomer.html',res='Customer Added')
    except:
        return render_template('AddCustomer.html',err='Customer Adding Failed')

@app.route('/loginbank',methods=['post'])
def loginpage():
    username=request.form['username']
    password=request.form['password']
    print(username,password)
    contract,web3=connect_blockchain_bank(0)
    state=contract.functions.loginBank(username,int(password)).call()
    if state==True:
        session['username']=username
        return redirect('/addcustomer')
    else:
        return render_template('index.html',err='Invalid Credentials')

@app.route('/withdrawmoney')
def withdrawmoneyPage():
    return render_template('WithdrawAmount.html')

@app.route('/withdrawmoneyform',methods=['post'])
def withdrawmoneyform():
    try:
        customer=request.form['customer']
        amount=int(request.form['amount'])
        print(customer,amount)
        contract,web3=connect_blockchain_kyc(0)
        _customers,_names,_caddresses,_aadhars,_pans,_mobiles,_emails,_accounts,_amounts,_passwords=contract.functions.viewCustomers().call()

        customerIndex=_customers.index(customer)
        if(_amounts[customerIndex]>=amount):
            contract,web3=connect_blockchain_kyc(0)
            tx_hash=contract.functions.withdrawAmount(customer,amount).transact()
            web3.eth.waitForTransactionReceipt(tx_hash)
            return render_template('WithdrawAmount.html',res='Withdraw Completed')
        else:
            return render_template('WithdrawAmount.html',err='Insufficient Balance')
    except:
        return render_template('WithdrawAmount.html',err='Withdraw Failed')

@app.route('/viewloans')
def viewloans():
    contract,web3=connect_blockchain_loan(0)
    _customers,_loanAmounts,_loanids,_loanStatus=contract.functions.viewLoans().call()
    data=[]
    for i in range(0,len(_customers)):
        dummy=[]
        dummy.append(_customers[i])
        dummy.append(_loanAmounts[i])
        dummy.append(_loanids[i])
        dummy.append(_loanStatus[i])
        data.append(dummy)

    return render_template('ViewLoans.html',dashboard_data=data,len=len(data))

@app.route('/approveloan')
def approveLoanPage():
    return render_template('ApproveLoan.html')

@app.route('/approveloanform',methods=['post'])
def approveloanform():
    try:
        loanid=int(request.form['loanid'])
        print(loanid)
        contract,web3=connect_blockchain_loan(0)
        tx_hash=contract.functions.approveLoan(loanid).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return render_template('ApproveLoan.html',res='Approve Loan Success')
    except:
        return render_template('ApproveLoan.html',err='Approve Loan Failed')

@app.route('/rejectloan')
def rejectloanPage():
    return render_template('RejectLoan.html')

@app.route('/rejectloanform',methods=['post'])
def rejectloanform():
    try:
        loanid=int(request.form['loanid'])
        print(loanid)
        contract,web3=connect_blockchain_loan(0)
        tx_hash=contract.functions.rejectLoan(loanid).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return render_template('RejectLoan.html',res='Rejected Loan Successfully')
    except:
        return render_template('RejectLoan.html',err='Reject Loan Failed')

@app.route('/closeloan')
def closeloanPage():
    return render_template('CloseLoan.html')

@app.route('/closeloanform',methods=['post'])
def closeloanform():
    try:
        loanid=int(request.form['loanid'])
        contract,web3=connect_blockchain_loan(0)
        tx_hash=contract.functions.closeLoan(loanid).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return render_template('CloseLoan.html',res='Close Loan Success')
    except:
        return render_template('CloseLoan.html',err='Close Loan Failed')

@app.route('/clogin')
def cloginPage():
    return render_template('LoginAccount.html')

@app.route('/addtransaction')
def addtransactionPage():
    return render_template('AddTransaction.html')

@app.route('/addtransactionform',methods=['post'])
def addtransactionform():
    reciever=request.form['reciever']
    amount=int(request.form['amount'])
    sender=session['username']
    print(sender,reciever,amount)

    contract,web3=connect_blockchain_kyc(0)
    _customers,_names,_caddresses,_aadhars,_pans,_mobiles,_emails,_accounts,_amounts,_passwords=contract.functions.viewCustomers().call()

    customerIndex=_customers.index(sender)
    if(_amounts[customerIndex]>=amount):
        contract,web3=connect_blockchain_transactions(0)
        tx_hash=contract.functions.addTransaction(sender,reciever,amount).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        
        contract,web3=connect_blockchain_kyc(0)
        tx_hash=contract.functions.withdrawAmount(sender,amount).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)

        contract,web3=connect_blockchain_kyc(0)
        tx_hash=contract.functions.addAmount(reciever,amount).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)

        contract,web3=connect_blockchain_transactions(0)
        _senders,_recievers,_amounts,_status,_ids=contract.functions.viewTransactions().call()

        id=_ids[-1]
        tx_hash=contract.functions.closeTransaction(id).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return render_template('AddTransaction.html',res='Transaction Completed')
    else:
        return render_template('AddTransaction.html',err='Insufficient Balance')


@app.route('/logincustomer',methods=['post'])
def logincustomer():
    try:
        username=request.form['username']
        password=int(request.form['password'])
        print(username,password)
        contract,web3=connect_blockchain_kyc(0)
        state=contract.functions.loginAccount(username,password).call()
        if state==True:
            session['username']=username
            return redirect('/addtransaction')
        else:
            return render_template('LoginAccount.html',err='Login Invalid')
    except:
        return render_template('LoginAccount.html',err='Login Failed')

@app.route('/viewtransactions')
def viewtransactionsPage():
    contract,web3=connect_blockchain_transactions(0)
    _senders,_recievers,_amounts,_status,_ids=contract.functions.viewTransactions().call()
    
    data=[]
    for i in range(0,len(_senders)):
        if(_recievers[i]==session['username']):
            dummy=[]
            dummy.append(_senders[i])
            dummy.append(_recievers[i])
            dummy.append(_amounts[i])
            if(_status[i]==1):
                dummy.append("Transaction Done")
            else:
                dummy.append("Transaction Pending")
            dummy.append(_ids[i])
            data.append(dummy)

        if(_senders[i]==session['username']):
            dummy=[]
            dummy.append(_senders[i])
            dummy.append(_recievers[i])
            dummy.append(_amounts[i])
            if(_status[i]==1):
                dummy.append("Transaction Done")
            else:
                dummy.append("Transaction Pending")
            dummy.append(_ids[i])
            data.append(dummy)


    return render_template('ViewTransactions.html',dashboard_data=data,len=len(data))

@app.route('/checkbalance')
def checkbalance():
    contract,web3=connect_blockchain_kyc(0)
    _customers,_names,_caddresses,_aadhars,_pans,_mobiles,_emails,_accounts,_amounts,_passwords=contract.functions.viewCustomers().call()

    customerIndex=_customers.index(session['username'])
    amount=_amounts[customerIndex]
    return render_template('checkbalance.html',balance='Rs. '+str(amount)+'/-')

@app.route('/addloan')
def addloanPage():
    return render_template('AddLoan.html')

@app.route('/addloanform',methods=['post'])
def addloanform():
    customer=session['username']
    amount=request.form['amount']
    print(customer,amount)
    
    try:
        contract,web3=connect_blockchain_loan(0)
        tx_hash=contract.functions.addLoan(customer,int(amount)).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return render_template('AddLoan.html',res='Loan Requested Successfully')
    except:
        return render_template('AddLoan.html',res='Loan Requested Failure')

@app.route('/cviewloans')
def cviewloans():
    contract,web3=connect_blockchain_loan(0)
    _customers,_loanAmounts,_loanids,_loanStatus=contract.functions.viewLoans().call()
    
    data=[]
    for i in range(len(_customers)):
        if(_customers[i]==session['username']):
            dummy=[]
            dummy.append(_customers[i])
            dummy.append(_loanAmounts[i])
            dummy.append(_loanids[i])
            if(_loanStatus[i]==0):
                dummy.append('Loan Pending')
            elif(_loanStatus[i]==1):
                dummy.append('Loan Approved')
            elif(_loanStatus[i]==2):
                dummy.append('Loan Rejected')
            elif(_loanStatus[i]==3):
                dummy.append('Loan Closed')
            
            data.append(dummy)

    return render_template('cviewloans.html',dashboard_data=data,len=len(data))

if __name__=="__main__":
    app.run(debug=True,port=5001,host='0.0.0.0')

