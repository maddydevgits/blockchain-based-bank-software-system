const loan=artifacts.require('loan')

module.exports=function(deployer){

    deployer.deploy(loan);
}