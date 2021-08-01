*** Settings ***
Resource    ../../../resources/diagnoser.robot
Resource    ../../../resources/serial.robot

*** Variables ***
${target}

*** Test Cases ***
ICP-9607_Check CBS Diagnostic Jobs Implementation : CBS DiagJob 0x4201 
    [Tags]    JIRA_TEST:ICP-9607
    Create Logs    ICP-9607    ${target}
    Run Diagnoser    ICP-9607    ICP-9607   ${target}
    Sleep   10s
    Run Keyword and Continue on Failure     Check Equal Or Bigger Number Of Bytes         ICP-9607    Received    150
    Kill Dlt
    Check CBS_0x4201    ICP-9607