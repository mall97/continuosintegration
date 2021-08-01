*** Settings ***
Resource    ../../resources/DLT.robot  
Resource    ../../resources/serial.robot
Resource    ../../resources/diagnoser.robot

*** Variables ***
${target}

*** Test Cases ***
ICP-5911 Check Dlt Traces for Display DiagJobs : STEUERN_CID_EIN - STEUERN_DISPLAY_ON
    [Tags]    JIRA_TEST:ICP-5911
    Res Rack        COM15 
    Check Display    ${target}
    Create Logs    ICP-5911    ${target}
    Sleep    15s
    Run Diagnoser    ICP-5911    ICP-5911    ${target}
    Sleep    25s 
    Check Diagnoser 2        ICP-5911    0x6E, 0xD5, 0xC2
    Kill Dlt 
    Check STEUERN_DISPLAY_ON    ICP-5911    
