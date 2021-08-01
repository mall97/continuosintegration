*** Settings ***
Resource    ../../resources/DLT.robot  
Resource    ../../resources/serial.robot
Resource    ../../resources/diagnoser.robot

*** Variables ***
${target}

*** Test Cases ***
ICP-5915 Check Dlt Traces for Display DiagJobs : STEUERN _TESTBILD_ERWEITERT - STEUERN_DISPLAY_TESTBILD_ERWEITERT		
    [Tags]    JIRA_TEST:ICP-5915
    Res Rack        COM15 
    Check Display    ${target}
    Create Logs    ICP-5915    ${target}
    Sleep    15s
    Run Diagnoser    ICP-5915    ICP-5915    ${target}
    Sleep    25s
    Check Diagnoser 2        ICP-5915    0x6E, 0xD5, 0xC1
    Kill Dlt 
    Check STEUERN_DISPLAY_TESTBILD_ERWEITERT    ICP-5915