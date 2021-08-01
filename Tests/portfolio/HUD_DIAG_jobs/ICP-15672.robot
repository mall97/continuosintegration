*** Settings ***
Resource    ../../resources/DLT.robot  
Resource    ../../resources/serial.robot
Resource    ../../resources/diagnoser.robot

*** Variables ***
${target}

*** Test Cases ***
ICP-15672 Diag Jobs for HUD Driver -STATUS_SENSOREN_IDENT_LESEN_ERWEITERT 0xDA46
    [Tags]    JIRA_TEST:ICP-15672
    Run Diagnoser    ICP-15672    ICP-15672    ${target}
    Sleep    10s 
    Check Diagnoser 2        ICP-15672    0x62, 0xDA, 0x46