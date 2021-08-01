*** Settings ***
Resource    ../../resources/DLT.robot  
Resource    ../../resources/serial.robot
Resource    ../../resources/diagnoser.robot

*** Variables ***
${target}

*** Test Cases ***
ICP-16470 Check Diag jobs for Climate Timer Implementation
    [Tags]    JIRA_TEST:ICP-16470
    Run Diagnoser   ICP-16470   ICP-16470   ${target}
    Sleep   10s
    Check Equal Number of Bytes         ICP-16470   Received    59

