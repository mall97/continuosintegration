*** Settings ***
Resource    ../../../resources/diagnoser.robot
Resource    ../../../resources/serial.robot

*** Variables ***
${target}

*** Test Cases ***
ICP-9606_Check CBS Diagnostic Jobs Implementation : CBS DiagJob 0x1004 
    [Tags]    JIRA_TEST:ICP-9606
    Create Logs    ICP-9606    ${target}
    Run Diagnoser    ICP-9606    ICP-9606   ${target}
    Sleep   10s
    Run Keyword and Continue on Failure     Check Equal Number Of Bytes         ICP-9606    Received    1143
    Kill Dlt
    Check CBS_0x1004    ICP-9606