// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract bank {

    address _username;
    uint _password;

    constructor() {
        _username=msg.sender;
        _password=1234;
    }

    function loginBank(address username,uint password) public view returns(bool) {
        if(_username==username && _password==password) {
            return true;
        } else {
            return false;
        }
    }
}