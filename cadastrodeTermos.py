from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.action_builder import ActionBuilder
import pandas as pd
import keyboard
from datetime import date
import time
import os
import numpy as np


# 1. Acesso ao SIGAA
driver = webdriver.Firefox()
driver.get("https://sipac.ufrn.br/sipac/protocolo/mesa_virtual/lista.jsf")
time.sleep(1)

# 2. Identificação e entrada das credenciais (temporariamente)
# Aqui o programa espera você logar no SIPAC

# 3. Acessando a mesa virtual
mesaVirtual = WebDriverWait(driver, 10000).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "mesa-virtual"))
)

botaoCookies = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "btn.btn-primary"))
)
ActionChains(driver).click(botaoCookies).perform()
ActionChains(driver).click(mesaVirtual).perform()


# 4. Acessando a área de cadastro de documentos
abaDocumentos = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "menuForm:documentos_span"))
)
ActionChains(driver).click(abaDocumentos).perform()

cadastrarDocumento = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "menuForm:cadastrarDocumento:anchor"))
)
ActionChains(driver).click(cadastrarDocumento).perform()

ActionBuilder(driver).clear_actions()

# 5. Cadastro do documento
tabela = pd.read_csv('relacao.csv', delimiter=';')

n = 0

for i in tabela.itertuples():
    tipoDocumento = tabela.loc[n, "Tipo de Documento"]
    nomeAluno = tabela.loc[n, "Nome do Aluno"]
    if tabela.loc[n, "Cadastrado"] == "N":
        match tipoDocumento:
            case 'TCEO':
                inputTipoDocumento = WebDriverWait(driver, 100000).until(
                    EC.visibility_of_element_located((By.ID, "documentoForm:tipo"))
                ) 
                inputTipoDocumento.send_keys("TERMO DE COMPROMISSO DE ESTÁGIO CURRICULAR OBRIGATÓRI")

                inputTipoDocumento = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "documentoForm:suggestionTipoDocumento:suggest"))
                ) 
                ActionChains(driver).click(inputTipoDocumento).perform()

                time.sleep(2)

                naturezaDocumento = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "documentoForm:natureza"))
                )
                ActionChains(driver).click(naturezaDocumento).perform()
                time.sleep(0.5)

                keyboard.press_and_release('down')
                time.sleep(0.5)
                keyboard.press_and_release('enter')

                hipoteseLegal = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "documentoForm:hipoteseLegalRestritoDocumento"))
                )
                ActionChains(driver).click(hipoteseLegal).perform()
                time.sleep(0.5)

                keyboard.press_and_release('down')
                time.sleep(0.5)
                keyboard.press_and_release('down')
                time.sleep(0.5)
                keyboard.press_and_release('down')
                time.sleep(0.5)
                keyboard.press_and_release('enter')

                assuntoDetalhado = driver.find_element(By.ID, "documentoForm:c_assunto_detalhado")
                assuntoDetalhado.send_keys("Termo %s" % (nomeAluno))

                body = driver.find_element(By.TAG_NAME, "body")
                body.click()

                keyboard.send("end")
                time.sleep(2)

                formasDocumentos = driver.find_element(By.ID, "documentoForm:idFormaDocumento")
                labels = formasDocumentos.find_elements(By.TAG_NAME, "label")
                labels[1].click()
                time.sleep(0.5)
                keyboard.send("end")

                # Dados do documento

                data = date.today()

                ano = driver.find_element(By.ID, "documentoForm:c_ano")
                ano.send_keys(Keys.BACKSPACE)
                ano.send_keys(data.year)

                dataDocumento = driver.find_element(By.ID, "documentoForm:data")
                dataDocumento.send_keys(tabela.loc[n, "Data do Documento"])

                dataRecebimento = driver.find_element(By.ID, "documentoForm:datarecebimento")
        
                data= data.strftime("%d/%m/%Y")
                dataRecebimento.send_keys(data)

                tipoConferencia = driver.find_element(By.ID, "documentoForm:tipoConferencia")
                tipoConferencia.click()
                time.sleep(0.3)
                keyboard.press_and_release('down')
                time.sleep(0.5)
                keyboard.press_and_release('enter')

                arquivo = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "C:/Users/emanuel.varela.101/Documents/Testes com o Selenium/Documentos", "TCE %s.pdf" % (nomeAluno)))

                entradaArquivo = driver.find_element(By.ID, "documentoForm:arquivoDocumento")
                entradaArquivo.send_keys(arquivo)
                time.sleep(2)
                body = driver.find_element(By.TAG_NAME, "body")
                body.click()
                keyboard.send("end")
                time.sleep(1)

                # Painel de Assinantes dos Documentos

                def adicionarAssinantes(idAssinante, idPainelAssinante, idEntradaAsssinante, codAssinante, idSugestaoAssinante, idBotao, classFechar):

                    def opcoesAssinantes():
                        adicionarAssinante = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.ID, "documentoForm:btnAdicionarAssinante"))
                        )
                        ActionChains(driver).move_to_element(adicionarAssinante).perform()

                        opcoesAssinantes = driver.find_element(By.ID, "documentoForm:menuOpcoesAdicionarAssinantes")

                        return opcoesAssinantes

                    Assinante = WebDriverWait(opcoesAssinantes(), 10).until(
                        EC.visibility_of_element_located((By.ID, idAssinante))
                    )
                    Assinante.click()

                    painelAssinante = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.ID, idPainelAssinante))
                    )
                    codigo = painelAssinante.find_element(By.ID, idEntradaAsssinante)
                    codigo.send_keys("%s" % (codAssinante))

                    inputAssinante = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.ID, idSugestaoAssinante))
                    ) 
                    inputAssinante.click()

                    adicionarAssinante = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.ID, idSugestaoAssinante))
                    ) 
                    adicionarAssinante.click() 

                    botaoAluno = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.ID, idBotao))
                    ) 
                    ActionChains(driver).click(botaoAluno).perform()

                    fechar = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.ID, classFechar))
                    )
                    time.sleep(0.5)
                    ActionChains(driver).click(fechar).perform()

                    ActionBuilder(driver).clear_actions()

                    time.sleep(2)
                    keyboard.send("end")

                # Assinatura do Aluno

                if '%s' % (tabela.loc[n, "Cod. Aluno"]) != 'nan':
                    if type(tabela.loc[n, "Cod. Aluno"]) is np.float64:
                        codigoAluno = int(tabela.loc[n, "Cod. Aluno"])
                    else:
                        codigoAluno = tabela.loc[n, "Cod. Aluno"]
                    adicionarAssinantes("documentoForm:linkAdicionarAssinaturaDiscente", 
                                        "panelAdicionarAssinanteDiscenteContainer", 
                                        "formAdicionarAssinanteDiscente:nomeAluno",
                                        codigoAluno,
                                        "formAdicionarAssinanteDiscente:suggestionNomeAluno:suggest",
                                        "formAdicionarAssinanteDiscente:btnAdicionarAssDiscente",
                                        "hidelinkAdicionarAssinanteDiscente")
                    time.sleep(1)

                # Assinatura do Coordenador

                if '%s' % (tabela.loc[n, "Cod. Coordenador"]) != 'nan':
                    if type(tabela.loc[n, "Cod. Coordenador"]) is np.float64:
                        codigoCoordenador = int(tabela.loc[n, "Cod. Coordenador"])
                    else:
                        codigoCoordenador = tabela.loc[n, "Cod. Coordenador"]
                    adicionarAssinantes("documentoForm:linkAdicionarAssinaturaOutraUnidade", 
                                        "panelAdicionarAssinanteOutraUnidadeContainer", 
                                        "formAdicionarAssinanteOutraUnidade:nomeServidorAssinatura",
                                        codigoCoordenador,
                                        "formAdicionarAssinanteOutraUnidade:suggestionServidorAssinatura:suggest",
                                        "formAdicionarAssinanteOutraUnidade:j_id_jsp_1453459627_382",
                                        "hidelinkAdicionarAssinanteOutraUnidade")
                    time.sleep(1)

                # Assinatura do Orientador

                if '%s' % (tabela.loc[n, "Cod. Orientador"]) != 'nan':
                    if type(tabela.loc[n, "Cod. Orientador"]) is np.float64:
                        codigoOrientador = int(tabela.loc[n, "Cod. Orientador"])
                    else:
                        codigoOrientador = tabela.loc[n, "Cod. Orientador"]
                    adicionarAssinantes("documentoForm:linkAdicionarAssinaturaOutraUnidade", 
                            "panelAdicionarAssinanteOutraUnidadeContainer", 
                            "formAdicionarAssinanteOutraUnidade:nomeServidorAssinatura",
                            codigoOrientador,
                            "formAdicionarAssinanteOutraUnidade:suggestionServidorAssinatura:suggest",
                            "formAdicionarAssinanteOutraUnidade:j_id_jsp_1453459627_382",
                            "hidelinkAdicionarAssinanteOutraUnidade")
                    time.sleep(1)

                # Assinatura do Supervisor

                if '%s' % (tabela.loc[n, "Cod. Supervisor"]) != 'nan':
                    if type(tabela.loc[n, "Cod. Supervisor"]) is np.float64:
                        codigoSupervisor = int(tabela.loc[n, "Cod. Supervisor"])
                    else:
                        codigoSupervisor = tabela.loc[n, "Cod. Supervisor"]
                    # Se a concedente for a UFRN:
                    if '%s' % (tabela.loc[n, "UFRN"]) == 's':
                        adicionarAssinantes("documentoForm:linkAdicionarAssinaturaOutraUnidade", 
                                "panelAdicionarAssinanteOutraUnidadeContainer", 
                                "formAdicionarAssinanteOutraUnidade:nomeServidorAssinatura",
                                codigoSupervisor,
                                "formAdicionarAssinanteOutraUnidade:suggestionServidorAssinatura:suggest",
                                "formAdicionarAssinanteOutraUnidade:j_id_jsp_1453459627_382",
                                "hidelinkAdicionarAssinanteOutraUnidade")
                    # Se a concedente não for a UFRN:
                    else:
                        adicionarAssinantes("ddocumentoForm:linkAdicionarAssinaturaExterno", 
                                "panelAdicionarAssinanteExternoContainer", 
                                "formAdicionarAssinanteExterno:nomeExterno",
                                codigoSupervisor,
                                "formAdicionarAssinanteExterno:suggestionNomeExterno:suggest",
                                "formAdicionarAssinanteExterno:btnAdicionarAssExterno",
                                "hidelinkAdicionarAssinanteExterno")
                    time.sleep(1)

                # Assinatura da Concedente

                if '%s' % (tabela.loc[n, "Cod. Concedente"]) != 'nan':
                    if type(tabela.loc[n, "Cod. Concedente"]) is np.float64:
                        codigoConcedente = int(tabela.loc[n, "Cod. Concedente"])
                    else:
                        codigoConcedente = tabela.loc[n, "Cod. Concedente"]
                    # Se a concedente for a UFRN:
                    if '%s' % (tabela.loc[n, "UFRN"]) == 's':
                        adicionarAssinantes("documentoForm:linkAdicionarAssinaturaOutraUnidade", 
                                "panelAdicionarAssinanteOutraUnidadeContainer", 
                                "formAdicionarAssinanteOutraUnidade:nomeServidorAssinatura",
                                codigoConcedente,
                                "formAdicionarAssinanteOutraUnidade:suggestionServidorAssinatura:suggest",
                                "formAdicionarAssinanteOutraUnidade:j_id_jsp_1453459627_382",
                                "hidelinkAdicionarAssinanteOutraUnidade")
                    # Se a concedente não for a UFRN:
                    else:
                        adicionarAssinantes("ddocumentoForm:linkAdicionarAssinaturaExterno", 
                                "panelAdicionarAssinanteExternoContainer", 
                                "formAdicionarAssinanteExterno:nomeExterno",
                                codigoConcedente,
                                "formAdicionarAssinanteExterno:suggestionNomeExterno:suggest",
                                "formAdicionarAssinanteExterno:btnAdicionarAssExterno",
                                "hidelinkAdicionarAssinanteExterno")
                    time.sleep(1)

                # Assinatura do Agente de Integração

                if '%s' % (tabela.loc[n, "Cod. Agente"]) != 'nan':
                    if type(tabela.loc[n, "Cod. Agente"]) is np.float64:
                        codigoAgente = int(tabela.loc[n, "Cod. Agente"])
                    else:
                        codigoAgente = tabela.loc[n, "Cod. Agente"]
                    adicionarAssinantes("ddocumentoForm:linkAdicionarAssinaturaExterno", 
                            "panelAdicionarAssinanteExternoContainer", 
                            "formAdicionarAssinanteExterno:nomeExterno",
                            "codigoAgente",
                            "formAdicionarAssinanteExterno:suggestionNomeExterno:suggest",
                            "formAdicionarAssinanteExterno:btnAdicionarAssExterno",
                            "hidelinkAdicionarAssinanteExterno")
                    time.sleep(1)

        # Continuar
        continuar = driver.find_element(By.XPATH, "//input[@name='documentoForm:acaoContinuar']")
        continuar.click()

        continuar = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='documentoForm:j_id_jsp_73650832_53']"))
        )
        ActionChains(driver).click(continuar).perform()

        # Dados do interessado a ser inserido

        opAluno = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'interessadosForm:j_id_jsp_1031754454_16'))
        )
        ActionChains(driver).click(opAluno).perform()

        opAluno = driver.find_element(By.ID, "interessadosForm:nomeAluno")
        opAluno.send_keys(int(tabela.loc[n, "Matricula do Interessado"]))

        opAluno = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'rich-sb-cell-padding.richfaces_suggestionSelectValue'))
        ) 
        ActionChains(driver).click(opAluno).perform()

        time.sleep(0.5)

        inserir = driver.find_element(By.XPATH, "//input[@value='Inserir']")
        inserir.click()

        time.sleep(0.5)

        # Continuar
        continuar = driver.find_element(By.XPATH, "//input[@name='interessadosForm:j_id_jsp_1031754454_110']")
        continuar.click()

        # Movimentação Inicial

        unidadeDestino = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "arvore_unidades_codigo"))
        )
        if "%s" % (tabela.loc[n, "Unidade de Destino"]) == 'L':
            unidadeDestino.send_keys('11.39.00.03')
        else:
            unidadeDestino.send_keys('11.39.00.01')

        # Cotinuar

        continuar = driver.find_element(By.XPATH, "//input[@value='Continuar >>']")
        continuar.click()
        tabela.at[n, "Cadastrado"] = "S"
        
    n = n+1

print('Fim da aUtomação')