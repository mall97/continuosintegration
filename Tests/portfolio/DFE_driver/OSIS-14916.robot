*** Settings ***
Resource    ../../../resources/diagnoser.robot
Resource    ../../../resources/serial.robot

*** Variables ***
${target}

*** Test Cases ***
OSIS-14916_Diag Jobs DFE Display APIX3 Register_DISPLAY_DFE_GENERISCH 0xF042-Sub ID -II
    [Tags]    JIRA_TEST:OSIS-14916
    Res Rack        COM15
    Run Diagnoser    OSIS_14916    OSIS_14916    ${target}
    Check Diagnoser 2        OSIS_14916    0x71, 0x01, 0xF0, 0x42, 0x00, 0x06, 0x62, 0x06