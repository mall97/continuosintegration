*** Settings ***
Resource    ../../resources/DLT.robot  
Resource    ../../resources/serial.robot
Resource    ../../resources/diagnoser.robot

*** Variables ***
${target}

*** Test Cases ***
ICP-15669 Diag Jobs for HUD Driver -STATUS_SENSOREN_IDENT_LESEN_HUD 0x4604
    [Tags]    JIRA_TEST:ICP-15669
    Run Diagnoser    ICP-15669    ICP-15669    ${target}
    Sleep    10s 
    Check Diagnoser 2        ICP-15669    0x62, 0x46, 0x04

