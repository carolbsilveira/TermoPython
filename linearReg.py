
# Metodo dos mínimos quadrados:
    
def linearR(M1,M2): 
    '''
    Obtém uma equação linear que supõe chutes para a pressão experimental,
    aceitáveis para o algoritmo.

    Parâmetros
    ----------
    M1 : lista, ou array, unidimensional
        Sequência de valores para o eixo x.
    
    M2 : lista, ou array, unidimensional
        Sequência de valores para o eixo x..

    Retornos
    -------
    af : float
        Coeficiente angular da equação linearizada.
        
    bf : float
        Coeficiente linear da equação linearizada.

    '''
    
    
    # Registra o número de valores em M1.
    n = len(M1)
    
    sa1=0
    sa2=0    
    sb1=0
    sb2=0

    for n in range(len(M1)):
        # Cálculo da soma dos quadrados.
        a1 = M1[n]*M1[n]
        sa1 += a1
        # Soma dos elementos de M1
        a2 = M1[n]
        sa2 += a2
        # Soma dos produtos de cada elemento de "M1" e "M2".
        b1 = M1[n]*M2[n]
        sb1 += b1
        # A soma de elementos de "M2".  
        b2 = M2[n]
        sb2 += b2
    # Parametros para o calculo dos coeficientes.    
    Aline = sa1 - ((sa2*sa2))/n
    Bline = sb1 - (sa2*sb2)/n
    # Coeficiente angular da reta. 
    af = Bline/Aline
    # Coeficiente linear da reta.
    bf = (sb2/n) - ((sa2/n)*af)

    return af, bf     