*** Settings ***
Resource    ../../resources/DLT.robot  
Resource    ../../resources/serial.robot
Library   ../../Libraries/vcar/on_off_vcar.py
Test Teardown    Close Connection

*** Variables ***
${HardwareVariant}
${HardwareSample}
${target}

*** Test Cases ***
OSIS-6050_Voltage and Temperature signals on environment data
    [Tags]    JIRA_TEST:OSIS-6050
    Logging In SOC        #Logging into SOC successful
    Send To Serial        /usr/bin/inc-demo_io_environment_SomeIp -t 2  
    Sleep    3s
    Check Environment Data Valid
    Send To Serial        /usr/bin/inc-demo_io_environment_SomeIp -t 2  
    Sleep    3s
    Check Environment Data Invalid

OSIS-8871_SHUTDOWN_APPLICATION_RESET
    [Tags]    JIRA_TEST:OSIS-8871
    Create Logs        ${LOG3}    ${target}
    Logging In SOC        #Logging into SOC successful
    Send To Serial        /usr/bin/nsm_control --requestRestart=7  
    Sleep    30s
    Kill Dlt
    Check NSM Reason        ${LOG3} 

OSIS-8858_Check HardwareVariant and HardwareSample 
    [Tags]    JIRA_TEST:OSIS-8858
    Logging In SOC        #Logging into SOC successful
    Send To Serial        /usr/bin/inc-demo_io_testing -t 1
    Sleep    5s
    Check Hw Versions    ${HardwareVariant}    ${HardwareSample}



    