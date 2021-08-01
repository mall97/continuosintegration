*** Settings ***
Resource    ../../../resources/diagnoser.robot
Resource    ../../../resources/serial.robot

*** Variables ***
${target}

*** Test Cases ***
ICP-9674_Check CBS Diagnostic Jobs Implementation : CBS DiagJob 0x1006 
    [Tags]    JIRA_TEST:ICP-9674
    Run Diagnoser    ICP-9674   ICP-9674   ${target}
    Sleep   10s
    Run Keyword and Continue on Failure     Check Equal Or Bigger Number Of Bytes         ICP-9674    Received    36
