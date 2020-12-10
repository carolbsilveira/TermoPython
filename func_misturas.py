import numpy as np

def parametro_aij(a1,a2,k=0.0000001,i=0):
    '''
    parametro_aij(a1,a2,k,i=0):
    
    Calcula a constante da mistura pra correção do parâmetro de atração
    
    Parâmetros
    ----------
        a1 : float
            Constante de substância pura para a correção do 
            paâmetro de atração do componente 1.
            
        a2 : float
            Constante de substância pura para a correção do 
            paâmetro de atração do componente 2.
            
        k : float, opicional
            Parâmetro de interação binária.
            
        i : int, opcional 
            operador para selecionar o componente para o calculo de aij.

    Retornos
    -------
        float
            Constante da mistura pra correção do parâmetro de atração.

            
    '''
    j= 1-i # Índice "j" complementar a "i" para localizar os termos na matriz "Ma"
    Ma = np.array([a1,a2]) # Gera a matriz com as constantes de correção 1 e 2.
    
    return (1 - k)*np.sqrt(Ma[i]*Ma[j]) # Equação da constante da mistura para correção do parâmetro de atração.
    
def parametro_atract(Matr,Mx,My):
    '''
    parametro_atract(Matr,Mx,My):
        
        Calcula os parâmetros de atração do líquido, al, e do vapor, av.

    Parâmetros
    ----------
        Matr : array bidimensional
            Array com os valores dos parâmetros aij e aii de cada componente.
            
        Mx : array unidimensional
            Array que contém os valores das frações molares, x1 e x2, do líquido.
            
        My : array unidimensional
            Array que contém os valores das frações molares, y1 e y2, do vapor.
            

    Retornos
    -------
        dict{
            
            al: índice que retorna o parâmetro de atração da fase líquida.
            
            av: índice que retorna o parâmetro de atração da fase vapor.
            
            }

    '''
    alii = 0
    alij = 0
    
    avii = 0
    avij = 0
    
    for i in range(0,2):
        j = 1 - i # Índice "j" complementar a "i" para localizar os termos na matriz "Ma"           
        # Fatores para o cálculo do parâmetro de atração da fase líquida.
        axii = Matr[i,i]*Mx[i]*Mx[i]
        axij = Matr[i,j]*Mx[i]*Mx[j]
        # Fatores para o cálculo do parâmetro de atração da fase vapor.
        ayii = Matr[i,i]*My[i]*My[i]
        ayij = Matr[i,j]*My[i]*My[j]
        # Somatório dos valores dos fatores da fase líquida.
        alii += axii
        alij += axij 
        # Somatório dos valores dos fatores da fase líquida.
        avii += ayii
        avij += ayij 
    # Calcula os parâmetros de atração a partir dos somatórios obtidos.    
    atrl = alii + alij
    atrv = avii + avij
    return {'al':atrl,'av':atrv}

def parametro_repulse(Mrep,Mx,My):
    '''
    parametro_repulse(Mrep,Mx,My):
        Calcula os parâmetros de repulsão para

    Parâmetros
    ----------
        Mrep : array bidimensional
                Array com os valores dos parâmetros de redução de cada componente.
            
        Mx : array unidimensional
                Array que contém os valores das frações molares, x1 e x2, do líquido.
                
        My : array unidimensional
                Array que contém os valores das frações molares, y1 e y2, do vapor.

    Retornos
    -------
    
        dict{
            
            bl: índice que retorna o parâmetro de repulsão da fase líquida.
            
            bv: índice que retorna o parâmetro de repulsão da fase vapor.
            
            }

    '''
    bl = 0
    bv = 0
    #
    for i in range(0,2):
        # Fatores para o cálculo do parâmetro de repulsão da fase vapor.
        bli = Mx[i]*Mrep[i]
        bvi = My[i]*Mrep[i]
        # Somatório dos valores dos fatores da fase líquida e vapor.
        bl += bli
        bv += bvi
    
    return {'bl':bl,'bv':bv}


def fatorcompress(MA,MB):
    '''
    Calcula as raízes da equação cúbica e retorna 
    os fatores de compressibilidade, raiz mínima para
    o líquido e máxima para o vapor.

    calcula_fatorcompress(fa,R,Q,cf1,cf2,cf3)

    Parâmetros
    ----------
        
        MA: Array unidimensional
            Array que contém os valores das constantes de ajuste
            para os termos de atração do líquido e do vapor.
        
        MB: Array unidimensional
            Array que contém os valores das constantes de ajuste
            para os termos de repulsão do líquido e do vapor.
        
    Retornos
    -------
        dict{
        
            Zl : float
                 Fator de compressibilidade da fase líquida.
         
            Zv : float
                Fator de compressibilidade da fase vapor.
                
                }
    '''
    for i in range(0,2):
        # Aplicação das equações dos coeficientes iniciais, do método de Peng Robinson, para o cálculo numérico das raízes. 
        cf1 = -(1 - MB[i])
        cf2 = MA[i] - 2*MB[i] - 3*(MB[i]*MB[i])
        cf3 = (-MA[i]*MB[i]) + (MB[i]*MB[i]) + (MB[i]**3)
        # Função para cálculo do parâmetro "Q" para definir se a equação cúbica possui uma ou três raízes reais.
        Q = (cf1**2 - 3*cf2)/9
        # Função para cálculo de um do parâmetro "R" para definir se a equação cúbica possui uma ou três raízes reais.
        R = ((2*cf1**3) - (9*cf1*cf2) + (27*cf3))/54
        # Função que relaciona os parâmetros "Q" e "R" definindo se a equação cúbica possui uma ou três raízes reais.
        fa = (Q**3) - (R**2) 
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
    
            S =(np.sqrt((R*R) - (Q**3)) + abs(R))**(1/3)
            # Expressão que calcula a raiz.
            r1 = -sgnR*(S + (Q/S))- cf1/3
            # Atribui os valores calculados dos fatores de compressibilidade da fase líquida e gasosa para as variáveis Zl e Zv.
            if i == 0:
                Zl = r1
            if i == 1:
                Zv = r1
        # Condição em que a raiz não é única.        
        else:
            theta = np.arccos(R/np.sqrt(Q**3))
            # Cálculo das 3 raízes.
            x1 = ((-2*np.sqrt(Q)*np.cos(theta/3)) - (cf1/3))
            x2 = ((-2*np.sqrt(Q)*np.cos((theta + 2*np.pi)/3)) - (cf1/3))
            x3 = ((-2*np.sqrt(Q)*np.cos((theta + 4*np.pi)/3)) - (cf1/3))
            # Matriz de resultados.
            X = [x1,x2,x3]            
            # Atribui o valore mínimo calculado dos fatores de compressibilidade da fase líquida e gasosa para as variáveis Zl e Zv.
            if i == 0:
                Zl = min(X)                
            if i == 1: 
                Zv = max(X)
    
    return {'l':Zl,'v':Zv} 

def coef_fugacidade(Zl,Zv,Mx,My,al,av,bl,bv,Ma,Mbi,MA,MB,i=0):
    '''
    

    Parâmetros
    ----------
    Zl : float
        Fator de compressibilidade da fase líquida.
        
    Zv : float
        Fator de compressibilidade da fase vapor.
        
    Mx : array unidimensional
        Array que contém os valores das frações molares, x1 e x2, do líquido.
        
    My : array unidimensional
        Array que contém os valores das frações molares, y1 e y2, do vapor.
        
    al : float
         índice que retorna o parâmetro de atração da fase líquida.
        
    av : float
         índice que retorna o parâmetro de atração da fase vapor.
        
    bl : float
         índice que retorna o parâmetro de repulsão da fase líquida.
        
    bv : float
        índice que retorna o parâmetro de repulsão da fase vapor.
        
    Ma : array bidimensional
        Array com os valores dos parâmetros aij e aii de cada componente.
        
    Mbi : array unidimensional
        Array com os valores dos parâmetros de redução de cada componente.
        
    MA : array unidimensional
        Array que contém os valores das constantes de ajuste
            para os termos de atração do líquido e do vapor.
        
    MB : array unidimensional
        Array que contém os valores das constantes de ajuste
            para os termos de repulsão do líquido e do vapor.
        
    i : int, opcional
        operador para aplicar a função em cada componente. The default is 0.

    Retornos
    -------
    dict{
        
        Mphi_l: Array unidimensional que contém os valores dos coeficientes
                de fugacidade da fase líquido.
        
        Mphi_v: Array unidimensional que contém os valores dos coeficientes
                de fugacidade da fase vapor.
        
        }
        

    '''
    # Cria arrays para armazenar os valores dos logaritmos e dos coeficientes de fugacidade.
    Mln_l = np.array([0,0], dtype = float)
    Mln_v = np.array([0,0], dtype = float)
    Mphi_l = np.array([0,0], dtype = float)
    Mphi_v = np.array([0,0], dtype = float)
    
    for i in range(0,2):
        # Cálculo do lagaritmos dos coeficientes de fugacidade da fase líquida.
        cla = Mbi[i]/bl*(Zl-1)
        clb = np.log(Zl-MB[0])
        clc1 = MA[0]/(2*(np.sqrt(2))*MB[0])
        clc2 = ((2*((Mx[0]*Ma[0,i])+(Mx[1]*Ma[1,i])))/al)-(Mbi[i]/bl)
        clc3_1 = Zl - (0.41421356237309515*MB[0])
        clc3_2 = Zl + (2.414213562373095*MB[0])
        clc3 = np.log(clc3_1/clc3_2)
        clc = clc1*clc2*clc3 
        # Valores são salvos na matriz Mln_l a partir da soma dos componentes a cima.
        Mln_l[i] = cla - clb + clc
        # Cálculo do lagaritmos dos coeficientes de fugacidade da fase vapor.
        cva = Mbi[i]/bv*(Zv-1)
        cvb = np.log(Zv-MB[1])
        cvc1 = MA[1]/(2*(np.sqrt(2))*MB[1])
        cvc2 = ((2*((My[0]*Ma[0,i])+(My[1]*Ma[1,i])))/av)-(Mbi[i]/bv)
        cvc3_1 = Zv - (0.41421356237309515*MB[1])
        cvc3_2 = Zv + (2.414213562373095*MB[1])
        cvc3 = np.log(cvc3_1/cvc3_2)
        cvc = cvc1*cvc2*cvc3
        # Valores são salvos na matriz Mln_v a partir da soma dos componentes a cima.
        Mln_v[i] = cva - cvb + cvc
        # Matriz Mphi_l e Mphi_v salvam os valores dos coeficientes de fugacidade líquido e vapor.
        Mphi_l[i] = np.exp(Mln_l[i])
        Mphi_v[i] = np.exp(Mln_v[i])

    
    return {'l':Mphi_l,'v':Mphi_v}

def fugacidade(Mphil,Mphiv,Mx,My,p):
    '''
    
    Parâmetros
    ----------
    Mphil : Array unidimensional
        Array que contém os valores dos coeficientes
        de fugacidade da fase líquido.
        
    Mphiv : Array unidimensional
        Array que contém os valores dos coeficientes
        de fugacidade da fase vapor.
        
    Mx : Array unidimensional
        Array que contém os valores das frações molares, x1 e x2, do líquido.
        
    My : Array unidimensional
        Array que contém os valores das frações molares, y1 e y2, do vapor.
        
    p : float
        Pressão experimental.

    Retornos
    -------
    dict{
        
        Mfl: Array unidimencional que armazena os valores da fugacidade de 
             cada componente da fase líquida.
        
        Mfv: Array unidimencional que armazena os valores da fugacidade de 
             cada componente da fase vapor.
        }

    '''
    # Cria arrays para armazenar os valores da fugacidade de cada componente da fase líquida e vapor.
    Mfl = np.array([0,0], dtype = float)
    Mfv = np.array([0,0], dtype = float)
    
    for i in range(0,2):
        # Computa e armazena os valores da fugacidade de cada componente da fase líquida e vapor.
        Mfl[i] = Mphil[i]*Mx[i]*p
        Mfv[i] = Mphiv[i]*My[i]*p
    
    return{'l': Mfl,'v':Mfv}

def y_otimizado(My,Mfl,Mfv,i=0):
    '''
    

    Parâmetros
    ----------
    My : Array unidimensional
        Array que contém os valores das frações molares, y1 e y2, do vapor.
    Mfl : Array unidimensional
        Array que armazena os valores da fugacidade de 
             cada componente da fase líquida.
    Mfv : Array unidimensional
        DESCRIPTION.
    i : TYPE, optional
        DESCRIPTION. The default is 0.

    Retornos
    -------
    MyI : Array unidimensional
        Array que armazena os valores otimizados de y.

    '''
    MyI = np.array([0,0],dtype = float)
    # Loop que optimiza o valor de y.
    for i in range(0,2):
    
        MyI[i] = My[i]*(Mfl[i]/Mfv[i])
    
    return MyI