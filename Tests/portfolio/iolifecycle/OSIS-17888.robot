Resource    ../../../resources/DLT.robot  
Resource    ../../../resources/serial.robot
Resource    ../../../resources/diagnoser.robot
Test Teardown    Close Connection

*** Variables ***
${target}

***Test Cases***
OSIS-17888 Check Wake-up reason over-temperature
    [Tags]  JIRA_TEST:OSIS-17888
    Res Rack        COM15
    Create Logs    OSIS-17888    ${target}
    Logging In SOC
    Send to Serial      /usr/bin/inc-demo_io_lifecycle_SomeIp -b 8
    Sleep    20s
    Kill Dlt
    Read Dlt        OSIS-17888    SHUTDOWN_OVERTEMPERATURE