*** Settings ***
Resource    ../../resources/DLT.robot  
Resource    ../../resources/serial.robot
Resource    ../../resources/diagnoser.robot

*** Variables ***
${target}

*** Test Cases ***
ICP-5912 Check Dlt Traces for Display DiagJobs : STEUERN_CID_ENDE - STEUERN_DISPLAY_OFF
    [Tags]    JIRA_TEST:ICP-5912
    Res Rack        COM15 
    Check Display    ${target}
    Create Logs    ICP-5912    ${target}
    Sleep    15s
    Run Diagnoser    ICP-5912    ICP-5912    ${target}
    Sleep    25s
    Check Diagnoser 2        ICP-5912    0x6E, 0xD5, 0xC9
    Kill Dlt 
    Check STEUERN_DISPLAY_OFF    ICP-5912            