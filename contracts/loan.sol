// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract loan {
  
  address[] _customers;
  uint[] _loanAmounts;
  uint[] _loanids;
  uint[] _loanStatus;

  uint lid=0;

  function addLoan(address customer,uint amount) public{

    lid+=1;
    _customers.push(customer);
    _loanAmounts.push(amount);
    _loanids.push(lid);
    _loanStatus.push(0);
  }

  function viewLoans() public view returns(address[] memory,uint[] memory,uint[] memory,uint[] memory){

    return (_customers,_loanAmounts,_loanids,_loanStatus);
  }

  function approveLoan(uint loanid) public{

    uint i=0;
    for(i=0;i<_loanids.length;i++){
      if(_loanids[i]==loanid){
        _loanStatus[i]=1;
      }
    }
  } 

  function rejectLoan(uint loanid) public{

    uint i=0;
    for(i=0;i<_loanids.length;i++){
      if(_loanids[i]==loanid){
        _loanStatus[i]=2;
      }
    }
  } 

  function closeLoan(uint loanid) public{

    uint i=0;
    for(i=0;i<_loanids.length;i++){
      if(_loanids[i]==loanid){
        _loanStatus[i]=3;
      }
    }
  } 
}
