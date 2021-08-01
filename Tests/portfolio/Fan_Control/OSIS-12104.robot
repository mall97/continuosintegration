*** Settings ***
Resource    ../../../resources/DLT.robot  
Resource    ../../../resources/serial.robot
Resource    ../../../resources/diagnoser.robot
Test Teardown    Close Connection

*** Variables ***
${target}

***Test Cases***
OSIS-12104 Flag0 at NOR Mode/ distance ≥ 10°C to HIGH thresold : Sensor 2 - SoC
    [Tags]  JIRA_TEST:OSIS-12104
    Logging In SOC
    Send to Serial      /bin/systemctl stop temperature-monitor
    Send to Serial      /usr/bin/inc-demo_soc_monitor -s 84000
    Sleep   2s
    Send to Serial      /usr/bin/inc-demo_healthdata_client
    Run Keyword and Continue on Failure    Success Check    fanRpm: 0
    Send To Serial  /usr/bin/inc-demo_soc_monitor -s 86000
    Sleep   2s     
    Send to Serial      /usr/bin/inc-demo_healthdata_client
    Run Keyword and Continue on Failure     Success Check    fanRpm: 2000
    Send to Serial      /bin/systemctl start temperature-monitor