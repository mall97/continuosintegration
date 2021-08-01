*** Settings ***
Resource    ../../resources/DLT.robot  
Resource    ../../resources/serial.robot
Resource    ../../resources/diagnoser.robot

*** Variables ***
${target}

*** Test Cases ***
ICP-14111 Time Read Diagnostic job -22 40 19 read real time clock status
    [Tags]    JIRA_TEST:ICP-14111
    Run Diagnoser    ICP-14111    ICP-14111    ${target}
    Sleep    10s 
    Check Diagnoser 2        ICP-14111   0x62, 0x40, 0x19 