*** Settings ***
Resource    ../../resources/DLT.robot  
Resource    ../../resources/serial.robot
Resource    ../../resources/diagnoser.robot

*** Variables ***
${target}

*** Test Cases ***
ICP-5916 Check Dlt Traces for Display DiagJobs : STATUS_CID_SW_VERSION - STATUS_DISPLAY_SW_VERSION		
    [Tags]    JIRA_TEST:ICP-5916
    Res Rack        COM15 
    Check Display    ${target}
    Create Logs    ICP-5916    ${target}
    Sleep    15s
    Run Diagnoser    ICP-5916    ICP-5916    ${target}
    Sleep    25s
    Check Diagnoser 2        ICP-5916    0x62, 0x40, 0x0E
    Kill Dlt 
    Check STATUS_DISPLAY_SW_VERSION    ICP-5916