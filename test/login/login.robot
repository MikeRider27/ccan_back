*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${url}  https://readiness.codelab.systems/
${navegador}    Chrome
${usuario}  test
${contraseña}    test

*** Test Cases ***
Login CCAN
    Open Browser    ${url}    ${navegador}

    Wait Until Page Contains Element    name:username
    Input Text    name:username    ${usuario}
    Input Text    xpath:/html/body/div[1]/div/div/div/div/form/div/div[2]/label[2]/div/div/div/input    ${contraseña}
    Click Element    xpath:/html/body/div[1]/div/div/div/div/form/div/div[3]/button/span[2]/span

Crear Paciente
    Sleep   5s
    Close Browser

*** Keywords ***
