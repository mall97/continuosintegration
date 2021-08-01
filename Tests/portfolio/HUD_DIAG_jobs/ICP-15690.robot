*** Settings ***
Resource    ../../resources/DLT.robot  
Resource    ../../resources/serial.robot
Resource    ../../resources/diagnoser.robot

*** Variables ***
${target}

*** Test Cases ***
ICP-15690 Diag Jobs for HUD Driver - Did_HudSwVersionLesen 0xDA44
    [Tags]    JIRA_TEST:ICP-15690
    Run Diagnoser    ICP-15690    ICP-15690    ${target}
    Sleep    10s 
    Check Diagnoser 2        ICP-15690    0x62, 0xDA, 0x44

