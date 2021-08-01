*** Settings ***
Resource    ../../resources/DLT.robot  
Resource    ../../resources/serial.robot
Resource    ../../resources/diagnoser.robot

*** Variables ***
${target}

*** Test Cases ***
ICP-5913 Check Dlt Traces for Display DiagJobs : TEST_VERBAU - STEUERN_TEST_VERBAU_DISPLAY
    [Tags]    JIRA_TEST:ICP-5913
    Res Rack        COM15 
    Check Display    ${target}
    Create Logs    ICP-5913    ${target}
    Sleep    15s
    Run Diagnoser    ICP-5913    ICP-5913    ${target}
    Sleep    25s
    Check Diagnoser 2        ICP-5913    0x71, 0x01, 0xAC, 0x00
    Check Diagnoser 2        ICP-5913    0x71, 0x03, 0xAC, 0x00
    Kill Dlt 
    Check STEUERN_TEST_VERBAU_DISPLAY    ICP-5913