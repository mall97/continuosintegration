*** Settings ***
Resource    ../../resources/diagnoser.robot

*** Variables ***
${target}

*** Test Cases ***
OSIS-8886_MGU_related_diagnostic_service_job
    [Tags]    JIRA_TEST:OSIS-8886
    Run Diagnoser    MGU_DIAG    OSIS-8886    ${target}
    Sleep    60s
    Check Diagnoser    OSIS-8886

OSIS-8884_IDC_related_diagnostic_service_jobs
    [Tags]    JIRA_TEST:OSIS-8884
    Run Diagnoser    IDC_DIAG    OSIS-8884    ${target}
    Sleep    60s
    Check Diagnoser    OSIS-8884
