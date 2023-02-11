// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract transactions {
  
  address[] _senders;
  address[] _recievers;
  uint[] _amounts;
  uint[] _status;
  uint[] _ids;

  uint txid=0;

  function addTransaction(address sender,address reciever,uint amount) public{

    txid+=1;
    _senders.push(sender);
    _recievers.push(reciever);
    _amounts.push(amount);
    _status.push(0);
    _ids.push(txid);
  }

  function viewTransactions() public view returns(address[] memory,address[] memory,uint[] memory,uint[] memory,uint[] memory){

    return (_senders,_recievers,_amounts,_status,_ids);
  }

  function closeTransaction(uint id) public{

    uint i=0;
    for(i=0;i<_ids.length;i++){
      if(_ids[i]==id){
        _status[i]=1;
      }
    }
  }
}
