#Funções para o Algorítimo de Substâncias Puras

import numpy as np

#Parâmetros iniciais
def temp_reduzida(t, tc): 
   '''
   Função para calcular a temperatura reduzida, 
   parâmetro que relaciona temperatura crítica
   e temperatura do ponto em questão.
   
   temp_reduzida(t, tc)

   Parâmetros
   ----------
   t : float
       Temperatura do ponto.
       
   tc : float
       Temperatura Crítica da substância.

   Retorno
   -------
   tr : float
       parâmetro Temperatura Reduzida.

   '''
   # Cálculo da razão entre as temperaturas do ponto e crítica da substância para encontrar a temperatura reduzida.
   tr = t/tc  
   return tr

def parametro_m(w):    
    '''
    Função para calcular o parâmetro m de auxílio para o 
    cálculo da função de correção alpha.

    parametro_m(w)

    Parâmetros
    ----------
    w : float
        Fator Acêntrico da substância

    Retorno
    -------
    m : float
        Parâmetro de auxílio m

    '''
    # Função para cálculo do parâmetro m do algoritmo de Peng Robinson.
    m = 0.37464 + 1.54226*w - 0.26992*w*w
    return m

def func_alpha(m,tr):
    '''
    Função do parâmetro alpha de correção 
    do termo de atração.

    func_alpha(m,tr)

    Parâmetros
    ----------
    m : float
        Parâmetro de auxílio m.
        
    tr : float
         Parâmetro Temperatura Reduzida.

    Retorno
    -------
    alpha : float
            Parâmetro de correção.

    '''
    # Função para cálculo do parâmetro alpha do algoritmo de Peng Robinson.
    alpha = (1 + m*(1-np.sqrt(tr)))**2
    return alpha

def constante_a(r,tc,pc,alpha):
    '''
    Cálculo da constante "a" que corrige o parâmetro de atração
    
    constante_a(r,tc,pc,alpha)
    
    Parâmetros
    ----------
    r : float
        Constante Universal dos Gases Perfeitos.
        
    tc : float 
         Temperatura Crítica da Substância.
         
    pc : float 
         Pressão Crítica da Substância.
         
    alpha : float
            Parâmetro de correção.

    Retorno
    -------
    a : float
        Constante do parâmetro de atração.

    '''
    # Função para cálculo da constante de correção "a".
    a = 0.45724*((r*r*tc*tc)/pc)*alpha
    return a

def constante_b(r,tc,pc):
    '''
    Cálculo da constante b que corrige o volume das moléculas.
    
    constante_b(r,tc,pc)
    
    Parâmetros
    ----------
    r : float
        Constante Universal dos Gases Perfeitos.
        
    tc : float
         Temperatura Crítica da Substância.
         
    pc : float
         Pressão Crítica da Substância.

    Retorno
    -------
    b : float
        Constante do volume das moléculas.

    '''
    # Função para cálculo da constante de correção "b".
    b = 0.0778*r*tc/pc
    return b

def constante_A(a,p,r,t):
    '''
    Constante A de ajuste do termo de atração 
    de volume para fator de compressibilidade 
    na equação cúbica.
    
    constante_A(a,p,r,t)
    
    Parâmetros
    ----------
    a : float
        Constante do parâmetro de atração.
        
    p : float
        Pressão do ponto.
        
    r : float
        Constante Universal dos Gases Perfeitos.
        
    t : float
        Temperatura do Ponto.

    Retorno
    -------
    A : float
        Constante A de ajuste da equação cúbica.

    '''
    # Cálculo do fator de correção da atração na equação do fator de compressibilidade.
    A = (a*p)/((r*t)**2)
    return A

def constante_B(b,p,r,t):
    '''
    Constante B de ajuste do termo de volume das moléculas
    de volume para fator de compressibilidade na equação 
    cúbica.

    constante_B(b,p,r,t)

    Parâmetros
    ----------
    b : float
        Constante do volume das moléculas.
        
    p : float
        Pressão do Ponto.
        
    r : float
        Constante Universal dos Gases Perfeitos.
        
    t : float
        Temperatura do Ponto.

    Retorno
    -------
    B : float
        Constante B de ajuste da equação cúbica.

    '''
    # Cálculo do fator de correção de repulsão na equação do fator de compressibilidade.
    B = (b*p)/(r*t)
    return B


def coeficientes_aux(A,B):
    '''
    Cálculo dos coeficientes de auxílio para a
    determinação do número de raízes da equação
    cúbica.

    coeficientes_aux(A,B)

    Parâmetros
    ----------
    A : float
        Constante A de ajuste da equação cúbica.
        
    B : float
        Constante B de ajuste da equação cúbica.

    Retornos
    -------
    cf1 : float 
          Primeiro coeficiente de auxílio.
          
    cf2 : float
          Segundo coeficiente de auxílio.
          
    cf3 : float
          Terceiro coeficiente de auxílio.

    '''
    # Aplicação das equações dos coeficientes iniciais, do método de Peng Robinson, para o cálculo numérico das raízes.
    cf1 = -(1 - B)
    cf2 = A - 2*B - 3*(B*B)
    cf3 = -A*B + B*B + B**3
    return cf1, cf2, cf3


def func_Q(cf1,cf2):
    '''
    Parâmetro de auxílio para definir se a equação 
    cúbica possui uma ou três raízes reais.

    func_Q(cf1,cf2)

    Parâmetros
    ----------
    cf1 : float 
          Primeiro coeficiente de auxílio.
          
    cf2 : float
          Segundo coeficiente de auxílio.

    Retorno
    -------
    Q : float
        Parâmetro Q da equação cúbica.

    '''
    # Função para cálculo do parâmetro "Q" para definir se a equação cúbica possui uma ou três raízes reais.
    Q = (cf1**2 - 3*cf2)/9
    return Q

def func_R(cf1,cf2,cf3):
    '''
    Parâmetro de auxílio para definir se a equação
    cúbica possui uma ou três raízes reais.
    
    func_R(cf1,cf2,cf3)

    Parâmetros
    ----------
    cf1 : float
          Primeiro coeficiente de auxílio.
          
    cf2 : float
          Segundo coeficiente de auxílio.
          
    cf3 : float
          Terceiro coeficiente de auxílio.

    Retorna
    -------
    R : Parâmetro R da equação cúbica.

    '''
    # Função para cálculo de um do parâmetro "R" para definir se a equação cúbica possui uma ou três raízes reais.
    R = (2*cf1**3 - 9*cf1*cf2 + 27*cf3)/54
    return R

def numero_raizes(Q,R):
    '''
    Cálculo da constante que relaciona os parâmetros
    Q e R para definir se a equação cúbica possui
    uma ou três raízes reais.

    numero_raizes(Q,R)

    Parâmetros
    ----------
    Q : float
        Parâmetro Q da equação cúbica.
        
    R : float
        Parâmetro R da equação cúbica.

    Retorno
    -------
    fa : float
         constante do número de raízes.

    '''
    # Função que relaciona os parâmetros "Q" e "R" definindo se a equação cúbica possui uma ou três raízes reais.
    fa = Q**3 - R**2  
    return fa

def calcula_fatorcompress(fa,R,Q,cf1,cf2,cf3):
    '''
    Calcula as raízes da equação cúbica e retorna 
    os fatores de compressibilidade, raiz mínima para
    o líquido e máxima para o vapor.

    calcula_fatorcompress(fa,R,Q,cf1,cf2,cf3)

    Parâmetros
    ----------
    fa : float
         constante do número de raízes.
         
    R : float
        Parâmetro R da equação cúbica.
        
    Q : float
        Parâmetro Q da equação cúbica.
        
    cf1 : float 
          Primeiro coeficiente de auxílio.
          
    cf2 : float
          Segundo coeficiente de auxílio.
          
    cf3 : float
          Segundo coeficiente de auxílio.

    Retornos
    -------
    Zl : float
         Fator de compressibilidade da fase líquida.
         
    Zv : float
         Fator de compressibilidade da fase vapor.

    '''
# Verificação do número de raízes da equação cúbica.
    # Condição em que a raiz é única.
    if fa < 0:
        # Condições que definem o fator do sinal da raiz.
        if R < 0:
            sgnR = -1

        elif R > 0:
            sgnR = 1

        else:
            sgnR = 0

        S =(np.sqrt(R*R - Q**3) + abs(R))**(1/3)
        # Expressão que calcula a raiz.
        r1 = -sgnR*(S + (Q/S))- cf1/3
        # Os fatores de compressibilidade serão iguais a raiz única.
        Zl = r1
        Zv = r1
    # Condição em que a raiz não é única.    
    else:
        theta = np.arccos(R/np.sqrt(Q**3))
        # Cálculo das 3 raízes.
        x1 = (-2*np.sqrt(Q)*np.cos(theta/3)) - (cf1/3)
        x2 = (-2*np.sqrt(Q)*np.cos((theta + 2*np.pi)/3)) - (cf1/3)
        x3 = (-2*np.sqrt(Q)*np.cos((theta + 4*np.pi)/3)) - (cf1/3)
        # Matriz de resultados. 
        X = [x1,x2,x3]
        Zl = min(X)
        Zv = max(X)
    
    return Zl, Zv

def coef_fugacidade(Zl,Zv,A,B):
    '''
    Cálculo dos coeficientes de fugacidade para 
    as fases líquida e vapor.

    coef_fugacidade(Zl,Zv,A,B)

    Parâmetros
    ----------
    Zl : float
         Fator de compressibilidade da fase líquida.
         
    Zv : float
         Fator de compressibilidade da fase vapor.
         
    A : float
        Constante A de ajuste da equação cúbica.
        
    B : float
        Constante B de ajuste da equação cúbica.

    Retornos
    -------
    cL : float
         Coeficiente de fugacidade da fase líquida.
         
    cV : float
         Coeficiente de fugacidade da fase vapor.

    '''
    # Cálculo dos logaritmos dos coeficientes de fugacidade: Líquido e vapor.
    ln_cL = (Zl-1)-(np.log(Zl-B))+((A/(2*np.sqrt(2)*B))*(np.log((Zl+((1-np.sqrt(2))*B))/(Zl+((1+np.sqrt(2))*B))))) 
    ln_cV = (Zv-1)-(np.log(Zv-B))+((A/(2*np.sqrt(2)*B))*(np.log((Zv+((1-np.sqrt(2))*B))/(Zv+((1+np.sqrt(2))*B))))) 
    # Cálculo dos coeficientes a partir dos logaritmos anteriores.        
    cL = np.exp(ln_cL)
    cV = np.exp(ln_cV) 
    
    return cL, cV
