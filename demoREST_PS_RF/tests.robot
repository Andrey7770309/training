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
    ${result}=    Get Json Value    ${response.content}    /headers/Host
    RequestsChecker.Common Check    ${response}
    Should Be Equal    ${result}    "httpbin.org"

Count response lines
    [Documentation]    Check number of lines in stream response is the same to a given one
    Set Test Variable    ${number_of_lines}    3
    ${response}=    Call steam      ${number_of_lines}
    ${result}=    Get Line Count    ${response.content}
    Should Be Equal As Numbers      ${result}    ${number_of_lines}
    RequestsChecker.Common Check    ${response}

*** Keywords ***
Authentication
    [Arguments]    ${base_name}    ${base_password}    ${check_name}    ${check_password}    ${status_code}
    [Documentation]    Check status_code from response after login attempt\n
    ...                with credentials
    ${response}=    Call basic auth    ${base_name}    ${base_password}    ${check_name}    ${check_password}
    RequestsChecker.Check Status Code    ${status_code}    ${response}
