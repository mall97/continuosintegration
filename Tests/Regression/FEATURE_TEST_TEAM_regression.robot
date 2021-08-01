*** Settings ***
Resource    ../../resources/DLT.robot  
Resource    ../../resources/serial.robot
Resource    ../../resources/diagnoser.robot
Test Teardown    Close Connection

*** Variables ***
${target}

***Test Cases***

#end
