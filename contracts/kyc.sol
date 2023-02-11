// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract kyc {

  address[] _customers;
  string[] _names;
  string[] _caddresses;
  string[] _aadhars;
  string[] _pans;
  string[] _mobiles;
  string[] _emails;
  string[] _accounts;
  uint[] _amounts;
  uint[] _passwords;

  mapping(address=>bool) users;

  function addCustomer(address customer,string memory name,string memory caddress,string memory aadhar,string memory pan,string memory mobile,string memory email,string memory account,uint password) public{

    require(!users[customer]);

    users[customer]=true;
    _customers.push(customer);
    _names.push(name);
    _caddresses.push(caddress);
    _aadhars.push(aadhar);
    _pans.push(pan);
    _mobiles.push(mobile);
    _emails.push(email);
    _accounts.push(account);
    _amounts.push(0);
    _passwords.push(password);
  }

  function viewCustomers() public view returns(address[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,uint[] memory,uint[] memory){

    return (_customers,_names,_caddresses,_aadhars,_pans,_mobiles,_emails,_accounts,_amounts,_passwords);
  }

  function addAmount(address customer,uint amount) public {

    require(users[customer]);

    uint i=0;
    for(i=0;i<_customers.length;i++){
      if(_customers[i]==customer){
        _amounts[i]+=amount;
      }
    }
  }

  function withdrawAmount(address customer,uint amount) public{

    require(users[customer]);

    uint i=0;
    for(i=0;i<_customers.length;i++){
      if(_customers[i]==customer){
        _amounts[i]-=amount;
      }
    }
  }

  function loginAccount(address username,uint password) public view returns(bool){

    uint i=0;
    for(i=0;i<_customers.length;i++){
      if(_customers[i]==username && _passwords[i]==password){
        return true;
      }
    }
    return false;
  }
}
