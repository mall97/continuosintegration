*** Settings ***
Resource    ../../../resources/diagnoser.robot
Resource    ../../../resources/serial.robot

*** Variables ***
${target}

*** Test Cases ***
ICP-16236_Check CBS Diagnostic Jobs Implementation : CBS DiagJob 0x4007 
    [Tags]    JIRA_TEST:ICP-16236
    Run Diagnoser    ICP-16236   ICP-16236  ${target}
    Sleep   10s
    Run Keyword and Continue on Failure     Check Equal Or Bigger Number Of Bytes         ICP-16236    Received    146
