*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${url}  https://readiness.codelab.systems/
${browser}  Chrome
${user}  test
${pass}  test

*** Test Cases ***
Login CCAN
    Open browser    ${url}   ${browser}
    Esperar por  name:username
    Input text  name:username   ${user}
    Input text  name:password   ${pass}
    Clic  xpath://*[@id="q-app"]/div/div/div/div/form/div/div[3]/button/span[2]/span

Acceder a Paciente
    Esperar por  xpath://*[@id="q-app"]/div/div[1]/aside/div[1]/div/div[3]/div/div/div/div/div[1]/div[3]/div
    Clic  xpath://*[@id="q-app"]/div/div[1]/aside/div[1]/div/div[3]/div/div/div/div/div[1]/div[3]/div
    Sleep  1s
    Clic  xpath:/html/body/div[1]/div/div[1]/aside/div[1]/div/div[3]/div/div/div/div/div[2]/div[1]/div/a/div[3]/div
    Esperar por  xpath:/html/body/div[1]/div/div[2]/main/section/div/div/div[1]/div[3]/div[2]/button[3]/span[2]/i
    Clic  xpath:/html/body/div[1]/div/div[2]/main/section/div/div/div[1]/div[3]/div[2]/button[3]/span[2]/i

Crear Paciente
    Esperar por  xpath:/html/body/div[1]/div/div[2]/main/section/div/div[2]/div/form/div[1]/div[2]/div[3]/label/div/div[1]/div[1]/input
    Input text  xpath:/html/body/div[1]/div/div[2]/main/section/div/div[2]/div/form/div[1]/div[2]/div[3]/label/div/div[1]/div[1]/input  5555555
    Sleep  5s
    close browser

*** Keywords ***
Clic
    [Arguments]    ${locator}
    Click Element    ${locator}

Esperar por
    [Arguments]    ${locator}
    Wait Until Page Contains Element    ${locator}    timeout=10s