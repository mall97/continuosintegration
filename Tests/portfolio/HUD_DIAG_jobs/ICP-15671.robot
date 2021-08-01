*** Settings ***
Resource    ../../resources/DLT.robot  
Resource    ../../resources/serial.robot
Resource    ../../resources/diagnoser.robot

*** Variables ***
${target}

*** Test Cases ***
ICP-15671 Check Dlt Traces for Display DiagJobs : STEUERN_CID_EIN - STEUERN_DISPLAY_ON
    [Tags]    JIRA_TEST:ICP-15671
    Logging In SOC
    Send to Serial      devcoding --caf 0x0000945e,/usr/share/sysfunc/coding/cafd_mgu_02_a.bin write HUD_VARIANTE 9
    Sleep    10s
    Res Rack        COM15
    Run Diagnoser    ICP-15671    ICP-15671    ${target}
    Sleep    10s 
    Check Diagnoser 2        ICP-15671    0x62, 0xDA, 0x0A
  
