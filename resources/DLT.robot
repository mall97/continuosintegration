*** Settings *** 
Library   ../Libraries/dlt_viewer/dlt_local_windows.py

*** Variables ***
@{INC_SRV_INIT}    INC SERVER version 0.5.2    INC IOC version: 0.5.0 is compatible    
...                INC SERVER is Ready for use

@{INC_ABS_INIT}    Starting ioc-abstraction service    IOWatchdog: requestInitialAttributesValue    Successfully Registered IOWatchdog Service    
...                Successfully Registered IOWatchdog Service    IOEnvironment: requestInitialAttributesValues    Successfully Registered IOEnvironment Service  
...                Successfully Registered NetworkManagementService Service    IOLifecycle: requestInitialAttributesValue    IOLifecycle: received attribute wakeUpReason
...                IOLifecycle: received attribute lifecycleCounter    IOLifecycle: received attribute errorResetCounter    IOLifecycle: received attribute mayInitiatePONR
...                IOLifecycle: received attribute cooldownInterval    IOLifecycle: received attribute pwfState    IOLifecycle: received attribute commStatus
...                IOLifecycle: received attribute standbyTimeRemaining    Successfully Registered IOLifeCycle Service    IOTesting: requestInitialAttributesValue
...                Successfully Registered IOTesting Service    Successfully Registered IOLogging Service    Successfully Registered IONetwork Service
...                IOC Abstraction is Ready

@{NSM}    ResetReason = 7    WAKEUP_REASON_APPLICATION

@{SHUTDOWN_FULL_OFF}    SHUTDOWN_FULL_OFF    WAKEUP_REASON_ETHERNET_ACTIVE

@{DISPLAY}    DataServices_DcmDspData_DisplayOn | No dataIN    DataServices_DcmDspData_DisplayOn | ErrorCode 0    DataServices_DcmDspData_DisplayOff_WriteData | No dataIn
...           DataServices_DcmDspData_DisplayOff_WriteData | ErrorCode 0    RoutineServices_TestVervauDisplay_RequestResult | No dataIn    RoutineServices_TestVervauDisplay_RequestResult | ErrorCode 3
...           DataServices_CidDetailInformationExtended_ConditionCheckRead | No dataIn    DataServices_CidDetailInformationExtended_ConditionCheckRead | Return E_OK
...           DataServices_CidDetailInformationExtended_ReadData | No dataIn    DataServices_CidDetailInformationExtended_ReadData | Return E_OK    DataServices_CidDetailInformationExtended_ReadData | Output data 0108f4... (49 bytes)
...           DataServices_DcmDspData_TestbildDisplay_WriteData | dataIn 98    DataServices_DcmDspData_TestbildDisplay_WriteData | Domain ErrorCode 00    DataServices_DcmDspData_DisplaySwVersion_ConditionCheckRead | No dataIn
...           DataServices_DcmDspData_DisplaySwVersion_ConditionCheckRead | Return E_OK    DataServices_DcmDspData_DisplaySwVersion__ReadData | No dataIn    DataServices_DcmDspData_DisplaySwVersion__ReadData | Return E_OK. Output 140615
...           RoutineServices_DisplayPrbsCheck_Start | dataIn 1155443322    RoutineServices_DisplayPrbsCheck_Start | Return 00 Domain ErrorCode 22    RoutineServices_DisplayPrbsCheck_RequestResult | No dataIn
...           RoutineServices_DisplayPrbsCheck_RequestResult | Return 01 Domain ErrorCode 22                        

@{STEUERN_DISPLAY_ON}    CidDiagIf_DisplayOn | In    CidDiagIf_DisplayOn | Out | RET: 0 

@{STEUERN_DISPLAY_OFF}    CidDiagIf_DisplayOff_WriteData | In    CidDiagIf_DisplayOff_WriteData | Out | RET: 0   

@{STEUERN_TEST_VERBAU_DISPLAY}    CidDiagIf_TestVerbauDisplay_Start | In    CidDiagIf_TestVerbauDisplay_Start | Out | RET: 0    CidDiagIf_TestVerbauDisplay_RequestResul | In    CidDiagIf_TestVerbauDisplay_RequestResul | Out | RET: 0             

@{STATUS_DISPLAY_DETAIL_INFORMATION_EXTENDED}    CidDiagIf_CidDetailInformationExtended_C | In    CidDiagIf_CidDetailInformationExtended_C | Out | RET: 0    CidDiagIf_CidDetailInformationExtended_R | Out | RET: 0 
...                                              CidDiagIf_CidDetailInformationExtended_R | In 

@{STEUERN_DISPLAY_TESTBILD_ERWEITERT}    CidDiagIf_TestbildDisplay_WriteData | In    CidDiagIf_TestbildDisplay_WriteData | Out | RET: 0    

@{STATUS_DISPLAY_SW_VERSION}    CidDiagIf_DisplaySwVersion_ConditionChec | In    CidDiagIf_DisplaySwVersion_ConditionChec | Out | RET: 0    CidDiagIf_DisplaySwVersion_ReadData | In    CidDiagIf_DisplaySwVersion_ReadData | Out | RET: 0 

@{CBS_0x1004}   0x22 0x10 0x04    0xFA 0xCE 0xDE 0xAD 0xBE 0xEF 0x04 0x77    Merge IocSocReq: merge start, totalSize

@{CBS_0x4201}   0x22 0x42 0x01      0xFA 0xCE 0xDE 0xAD 0xBE 0xEF 0x00 0x99     Merge IocSocReq: merge start, totalSize        

${LOG}    OSIS-8894
${LOG2}    OSIS-8922
${LOG3}    OSIS-8871
${LOG4}    OSIS-8870
${LOG5}    ICP-12552
${DISPLAY_LOG}     ICP-5927


*** Keywords ***
Check Inc-srv Initialization DLTs
    [Arguments]    ${file}    
    FOR    ${i}    IN RANGE    0    len(${INC_SRV_INIT})
        Run Keyword and Continue on Failure    Read Dlt        ${file}    ${INC_SRV_INIT}[${i}]        
    END

Check Ioc Abstraction DLTs
    [Arguments]    ${file}
    FOR    ${i}    IN RANGE    0    len(${INC_ABS_INIT})
        Run Keyword and Continue on Failure    Read Dlt        ${file}    ${INC_ABS_INIT}[${i}]        
    END

Check NSM Reason
    [Arguments]    ${file} 
    FOR    ${i}    IN RANGE    0    len(${NSM})
        Run Keyword and Continue on Failure    Read Dlt        ${file}    ${NSM}[${i}]        
    END

Check Shutdown
    [Arguments]    ${file}
    FOR    ${i}    IN RANGE    0    len(${SHUTDOWN_FULL_OFF})
        Run Keyword and Continue on Failure    Read Dlt        ${file}    ${SHUTDOWN_FULL_OFF}[${i}]        
    END

Check Display DiagJobs
    [Arguments]    ${file}
    FOR    ${i}    IN RANGE    0    len(${DISPLAY})
        Run Keyword and Continue on Failure    Read Dlt        ${file}    ${DISPLAY}[${i}]        
    END

Check STEUERN_DISPLAY_ON
    [Arguments]    ${file}
    FOR    ${i}    IN RANGE    0    len(${STEUERN_DISPLAY_ON})
        Run Keyword and Continue on Failure    Read Dlt        ${file}    ${STEUERN_DISPLAY_ON}[${i}]        
    END

Check STEUERN_DISPLAY_OFF
    [Arguments]    ${file}
    FOR    ${i}    IN RANGE    0    len(${STEUERN_DISPLAY_OFF})
        Run Keyword and Continue on Failure    Read Dlt        ${file}    ${STEUERN_DISPLAY_OFF}[${i}]        
    END

Check STEUERN_TEST_VERBAU_DISPLAY
    [Arguments]    ${file}
    FOR    ${i}    IN RANGE    0    len(${STEUERN_TEST_VERBAU_DISPLAY})
        Run Keyword and Continue on Failure    Read Dlt        ${file}    ${STEUERN_TEST_VERBAU_DISPLAY}[${i}]        
    END

Check STATUS_DISPLAY_DETAIL_INFORMATION_EXTENDED
    [Arguments]    ${file}
    FOR    ${i}    IN RANGE    0    len(${STATUS_DISPLAY_DETAIL_INFORMATION_EXTENDED})
        Run Keyword and Continue on Failure    Read Dlt        ${file}    ${STATUS_DISPLAY_DETAIL_INFORMATION_EXTENDED}[${i}]        
    END

Check STEUERN_DISPLAY_TESTBILD_ERWEITERT
    [Arguments]    ${file}
    FOR    ${i}    IN RANGE    0    len(${STEUERN_DISPLAY_TESTBILD_ERWEITERT})
        Run Keyword and Continue on Failure    Read Dlt        ${file}    ${STEUERN_DISPLAY_TESTBILD_ERWEITERT}[${i}]        
    END

Check STATUS_DISPLAY_SW_VERSION
    [Arguments]    ${file}
    FOR    ${i}    IN RANGE    0    len(${STATUS_DISPLAY_SW_VERSION})
        Run Keyword and Continue on Failure    Read Dlt        ${file}    ${STATUS_DISPLAY_SW_VERSION}[${i}]        
    END

Check CBS_0x1004
    [Arguments]    ${file}
    FOR    ${i}    IN RANGE    0    len(${CBS_0x1004})
        Run Keyword and Continue on Failure    Read Dlt        ${file}    ${CBS_0x1004}[${i}]        
    END
    
Check CBS_0x4201
    [Arguments]    ${file}
    FOR    ${i}    IN RANGE    0    len(${CBS_0x4201})
        Run Keyword and Continue on Failure    Read Dlt        ${file}    ${CBS_0x4201}[${i}]        
    END