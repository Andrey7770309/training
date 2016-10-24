*** Settings ***
Documentation     Test demo REST service
Library     String
Library     HttpLibrary.HTTP
Library     demo_rest.DemoREST
Library     RequestsChecker
Resource    status_codes.txt

*** Variables ***
${VALID_NAME}        us@43!_er
${VALID_PASSWORD}    pas@!_s

*** Test Cases ***
Auth request
    [Documentation]    Check status_code from response after login attempt
    ...                with credentials specified in Template
    [Template]    Authentication
    #Positive
    ${VALID_NAME}    ${VALID_PASSWORD}    ${VALID_NAME}    ${VALID_PASSWORD}    ${STATUS_OK}
    #Negative
    ${VALID_NAME}    ${VALID_PASSWORD}    nameInvalid      passInvalid          ${STATUS_UNAUTHORIZED}
    ${VALID_NAME}    ${VALID_PASSWORD}    ${VALID_NAME}    passInvalid          ${STATUS_UNAUTHORIZED}
    ${VALID_NAME}    ${VALID_PASSWORD}    nameInvalid      ${VALID_PASSWORD}    ${STATUS_UNAUTHORIZED}
    ${VALID_NAME}    ${VALID_PASSWORD}    ${VALID_NAME}    ${EMPTY}             ${STATUS_UNAUTHORIZED}
    ${VALID_NAME}    ${VALID_PASSWORD}    ${EMPTY}         ${VALID_PASSWORD}    ${STATUS_UNAUTHORIZED}
    ${VALID_NAME}    ${VALID_PASSWORD}    nameInvalid      ${EMPTY}             ${STATUS_UNAUTHORIZED}
    ${VALID_NAME}    ${VALID_PASSWORD}    ${EMPTY}         passInvalid          ${STATUS_UNAUTHORIZED}

Get response header
    [Documentation]    Check the Host from response headers
    ${response}=    Call get
    ${result}=    Get Json Value    json_string=${response.content}    json_pointer=/headers/Host
    RequestsChecker.Common Check    response=${response}
    Should Be Equal    first=${result}    second="httpbin.org"

Count response lines
    [Documentation]    Check number of lines in stream response is the same to a given one
    Set Test Variable    ${number_of_lines}    3
    ${response}=    Call steam      lines_number=${number_of_lines}
    ${result}=    Get Line Count    string=${response.content}
    RequestsChecker.Common Check    response=${response}
    Should Be Equal As Numbers      first=${result}    second=${number_of_lines}

*** Keywords ***
Authentication
    [Documentation]    Check status_code from response after login attempt\n
    ...                with credentials
    [Arguments]    ${base_name}    ${base_password}    ${check_name}    ${check_password}    ${status_code}
    ${response}=    Call basic auth      base_name=${base_name}      base_password=${base_password}
    ...                                  check_name=${check_name}    check_password=${check_password}
    RequestsChecker.Check Status Code    code=${status_code}         response=${response}
