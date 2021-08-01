*** Settings ***
Resource    ../../resources/DLT.robot  
Resource    ../../resources/serial.robot
Resource    ../../resources/diagnoser.robot

*** Variables ***
${target}

*** Test Cases ***
ICP-15670 Diag Jobs for HUD Driver - START_TestVerbauHud 0xA31C
    [Tags]    JIRA_TEST:ICP-15670
    Run Diagnoser    ICP-15670    ICP-15670    ${target}
    Sleep    10s 
    Check Diagnoser 2        ICP-15670    0x71, 0x01, 0xA3, 0x1C
    Check Diagnoser 2        ICP-15670    0x71, 0x03, 0xA3, 0x1C

   
