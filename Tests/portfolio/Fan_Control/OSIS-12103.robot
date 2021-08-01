*** Settings ***
Resource    ../../../resources/DLT.robot  
Resource    ../../../resources/serial.robot
Resource    ../../../resources/diagnoser.robot
Test Teardown    Close Connection

*** Variables ***
${target}

***Test Cases***
OSIS-12103 Flag0 at NOR Mode/ distance ≤ 10°C to HIGH thresold : Sensor 1 - REF
    [Tags]  JIRA_TEST:OSIS-12103
    Logging In SOC
    Send to Serial      /usr/bin/inc-demo_io_environment_SomeIp -g 1:4:70000
    Sleep   2s
    Send to Serial      /usr/bin/inc-demo_healthdata_client
    Run Keyword and Continue on Failure    Success Check    fanRpm: 2000
    Send to Serial      /usr/bin/inc-demo_io_environment_SomeIp -g 1:4:64000
    Sleep   2s
    Send to Serial      /usr/bin/inc-demo_healthdata_client
    Run Keyword and Continue on Failure     Success Check    fanRpm: 0