*** Settings ***
Resource    ../../../resources/DLT.robot  
Resource    ../../../resources/serial.robot
Resource    ../../../resources/diagnoser.robot
Test Teardown    Close Connection

*** Variables ***
${target}

***Test Cases***
OSIS-17891 Check the wupCounter
    [Tags]  JIRA_TEST:OSIS-17891
    Res Rack        COM15
    Create Logs    OSIS-17891    ${target}
    Logging In SOC
    Send to Serial      /usr/bin/inc-demo_io_lifecycle_SomeIp -a
    Sleep    20s
    Success Check    Received wupCounter attribute changed: 0.
    Kill Dlt
    Read Dlt        OSIS-17891    IOLifecycle: received attribute wupCounter