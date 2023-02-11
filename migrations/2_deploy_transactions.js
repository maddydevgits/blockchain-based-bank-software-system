const transactions=artifacts.require('transactions')

module.exports=function(deployer){

    deployer.deploy(transactions);
}