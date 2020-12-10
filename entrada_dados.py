
import pandas as pd 

def ler_dados_xlsx(arquivo,i):
    """
    Parâmetros
    ----------
    arquivo : .xlsx
        Planilha em formato .xlsx com os dados experimentais
        para cada substância listada.

    Retornos
    -------
    subst : String
        Nome da Substância escolhida pelo usuário
    ppt : Float
        Pressão do Ponto Triplo em bar da substância escolhida
    tpt : Float
        Temperatura do Ponto Triplo em Kelvin da substância escolhida
    pc : Float
        Presão Ponto Crítico em bar da substância escolhida
    tc : Float
        Temperatura do Ponto Crítico da substância escolhida
    w : Float
        Fator acêntrico da substãncia escolhida.

    """
    # Cria um dataFrame do arquivo colocado na função
    dados = pd.read_excel(arquivo)
    
    #Extrai do arquivo os dados necessários para aplicar no algoritmo de substâncias simples.
    subst = dados["Substância"][i]
    ppt = dados["Pressão Ponto Triplo (MPa)"][i]
    tpt = dados["Temperatura Ponto Triplo (K) "][i]
    pc = dados["Pressão Ponto Crítico (MPa)"][i]
    tc = dados["Temperatura Ponto Crítico (K)"][i]
    w = dados["Fator acêntrico"][i]
    
    # Retorna os dados em um dissionário para que eles possam ser chamados individualmente. 
    return {'subs':subst,'ppt': ppt, 'tpt':tpt, 'pc':pc, 'tc':tc,'w': w}

def ler_dados_mistura_xlsx(arquivo,i):
    """
    Parâmetros
    ----------
    arquivo : .xlsx
        Planilha em formato .xlsx com os dados experimentais
        para cada sistema listado.
        
    i : Integer 
        Indica o número do sistem escolhido pelo usuário.

    Retornos
    -------
    pc1 : Float
        Pressão Crítica do Componente 1 da mistura escolhida em atm .
    pc2 : Float
        Pressão Crítica do Componente 2 da mistura escolhida em atm.
    tc1 : Float
        Temperatura Crítica do  Componente 1 da mistura em Kelvin.
    tc2 : Float
        Temperatura Crítica do  Componente 2 da mistura em Kelvin.
    w1 : Float
        Fator Acêntrico do Componente 1 da mistura escolhida.
    w2 : Float
        Fator Acêntrico do Componente 2 da mistura escolhida.

    """
    # Cria um dataFrame do arquivo colocado na função.
    dados_mistura = pd.read_excel(arquivo)
    
    # Retira as informações essenciais para o algoritmo de misturas desse arquivo.
    pc1 = dados_mistura["Pressão Crítica do Componente 1 (atm)"][i]
    pc2 = dados_mistura["Pressão Crítica do Componente 2 (atm)"][i]
    tc1 = dados_mistura["Temperatura Crítica do  Componente 1 (K)"][i]
    tc2 = dados_mistura["Temperatura Crítica do Componente 2 (K)"][i]
    w1 = dados_mistura["Fator Acêntrico do Componente 1"][i]
    w2 = dados_mistura["Fator Acêntrico do Componente 2"][i]
    
    # Retorna os dados em um dissionário para que eles possam ser chamados individualmente.
    return {"pc1": pc1,"pc2": pc2,"tc1": tc1,"tc2": tc2,"w1": w1,"w2": w2}