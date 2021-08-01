*** Settings ***
Library    ../Libraries/Serial/serial_api.py
Library    ../Libraries/Restart_Rack/restart.py

*** Variables ***

@{CAN}        /usr/bin/inc-demo_can_client -a    /usr/bin/inc-demo_can_client -s -b 1    /usr/bin/inc-demo_can_client -s -c 2    
...           /usr/bin/inc-demo_can_client -s -d 3    /usr/bin/inc-demo_can_client -s -e Testing1    /usr/bin/inc-demo_can_client -s -f Testing2    
...           /usr/bin/inc-demo_can_client -s -g Testing3    /usr/bin/inc-demo_can_client -v    /usr/bin/inc-demo_can_client -o

@{Environment Data Valid}    DCS_POWER    GNSS_ANT_SIGNAL    KL30B_POWER    KL30F_POWER    CID_POWER    DFE_POWER    HUD_POWER    ARC_POWER
...                          SOC_TEMP    UFS_TEMP    INTERNAL_AMBIENT_TEMP    EXTERNAL_AMBIENT_TEMP        
@{Environment Data Invalid}   POC_POWER    CPU_TEMP    BOARD_TEMP    OPTICAL_DRIVE_TEMP

*** Keywords ***

Logging In SOC
    Serial Port Init        COM13
    Serial Logging  

Check Demo CAN Client
    FOR    ${i}    IN RANGE    0    len(${CAN})
        Send To Serial        ${CAN}[${i}]    1.3
        Success Check        ERROR_MESSAGE: SUCCESS        #Message "ERROR_MESSAGE: SUCCESS" should be received
    END

Check Environment Data Valid
    FOR    ${i}    IN RANGE    0    len(${Environment Data Valid})
        Check Someip    ${Environment Data Valid}[${i}]     isValid?: 1    #Should be valid
    END

Check Environment Data Invalid
    FOR    ${i}    IN RANGE    0    len(${Environment Data Invalid})
        Check Someip    ${Environment Data Invalid}[${i}]     isValid?: 0    #Should be invalid
    END
        