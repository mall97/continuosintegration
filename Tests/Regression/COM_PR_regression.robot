*** Settings ***
Resource    ../../resources/DLT.robot  
Resource    ../../resources/serial.robot
Test Teardown    Close Connection

*** Variables ***
${target}

*** Keywords ***
INC Check
    FOR    ${i}    IN RANGE    0    10
        Res Rack        COM15        #target rebooted
        Create Logs        ${LOG2}    ${target}           
        Sleep    60s
        Kill Dlt 
        Run Keyword and Continue on Failure    Check Inc-srv Initialization DLTs    ${LOG2}        #Sucess checking DLTs for inc-srv messages
        Run Keyword and Continue on Failure    Check Ioc Abstraction DLTs    ${LOG2}    #Sucess cheking DLTs for ioc abstraction
        
        Logging In SOC        #Logging into SOC successful
        Send To Serial         /bin/systemctl is-active inc-srv
        Run Keyword and Continue on Failure    Success Check        active        #Message "active" should be received
        Send To Serial         /bin/systemctl is-active ioc-abstraction
        Run Keyword and Continue on Failure    Success Check        active        #Message "active" should be received

        Send to Serial        lxc-attach -n kombi
        Send to Serial        /bin/systemctl stop muniicd
        Send To Serial        /usr/bin/inc-demo_burst_clients -t 5 
        Sleep    10s
        Run Keyword and Continue on Failure    Check Burst Client        #The CAN interface checked with success
        Close Connection
    END

*** Test Cases ***
OSIS-8894_Check inc-srv initialization and ioc abstraction after the board turns on
    [Tags]    JIRA_TEST:OSIS-8894   
    Res Rack        COM15        #target rebooted
    Create Logs        ${LOG}    ${target}           
    Sleep    60s
    Kill Dlt 
    Check Inc-srv Initialization DLTs    ${LOG}    #Sucess checking DLTs for inc-srv messages
    Check Ioc Abstraction DLTs    ${LOG}        #Sucess cheking DLTs for ioc abstraction
    [Teardown]

OSIS-8899_Check demo heath data
    [Tags]    JIRA_TEST:OSIS-8899    
    Logging In SOC        #Logging into SOC successful
    Send To Serial        /usr/bin/inc-demo_healthdata_client        
    Success Check        ERROR_MESSAGE: SUCCESS        #Message "ERROR_MESSAGE: SUCCESS" should be received
    

OSIS-8897_Check inc-srv
    [Tags]    JIRA_TEST:OSIS-8897
    Logging In SOC        #Logging into SOC successful
    Send To Serial         /bin/systemctl is-active inc-srv
    Success Check        active        #Message "active" should be received

OSIS-8898_Check ioc-abstraction   
    [Tags]    JIRA_TEST:OSIS-8898
    Logging In SOC        #Logging into SOC successful
    Send To Serial         /bin/systemctl is-active ioc-abstraction
    Success Check        active        #Message "active" should be received

OSIS-8900_Check demo sysinfo
    [Tags]    JIRA_TEST:OSIS-8900
    Logging In SOC        #Logging into SOC successful
    Send To Serial         /usr/bin/inc-demo_sysinfo_client
    Success Check        ERROR_MESSAGE: SUCCESS        #Message "ERROR_MESSAGE: SUCCESS" should be received

OSIS-8930_Check the CAN INC Interface
    [Tags]    JIRA_TEST:OSIS-8930    
    Logging In SOC        #Logging into SOC successful
    Send To Serial        /bin/systemctl stop signalgateway 
    Check Demo CAN Client        #The CAN interface checked with success
    Send To Serial        /bin/systemctl start signalgateway

OSIS-8922_Check demo burst client
    [Tags]    JIRA_TEST:OSIS-8922    
    Logging In SOC        #Logging into SOC successful
    Send to Serial        lxc-attach -n kombi
    Send to Serial        /bin/systemctl stop muniicd
    Send To Serial        /usr/bin/inc-demo_burst_clients -t 5 
    Sleep    10s
    Check Burst Client        #The channel priority checked with success

OSIS-8929_Check if INC keeps working after 10 reboots
    [Tags]    JIRA_TEST:OSIS-8929
    INC Check
    [Teardown]
