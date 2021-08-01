*** Settings ***
Resource    ../../resources/DLT.robot  
Resource    ../../resources/serial.robot
Resource    ../../resources/diagnoser.robot

*** Variables ***
${target}

*** Test Cases ***
ICP-5914 Check Dlt Traces for Display DiagJobs : STATUS_CID_DETAIL_INFORMATION_EXTENDED - STATUS_DISPLAY_DETAIL_INFORMATION_EXTENDED	
    [Tags]    JIRA_TEST:ICP-5914
    Res Rack        COM15 
    Check Display    ${target}
    Create Logs    ICP-5914    ${target}
    Sleep    15s
    Run Diagnoser    ICP-5914    ICP-5914    ${target}
    Sleep    25s
    Check Diagnoser 2        ICP-5914    0x62, 0x40, 0x11
    Kill Dlt 
    Check STATUS_DISPLAY_DETAIL_INFORMATION_EXTENDED    ICP-5914