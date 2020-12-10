import numpy as np
import linearReg as lr
import pandas as pd
import matplotlib.pyplot as plt
import funcoes_substpuras as fsp
import func_misturas as fm
import entrada_dados as ed


Tx =[]
Py=[]
# Define um operador para analisar a resposta dada.
valido = 0

print('Bem vindo ao TermoPython.\n\n --> Esse software foi feito para otimizar valores experimentais de pressão em sistemas de equilíbrios de fase líquido - vapor.\n --> Para consultar detalhes de uso do software acesse o tutorial e para detalhes de funcionamento acesse o manual.')
# Enquanto a resposta dada não for válida, o software requisita uma nova escolha e orienta novamente o usuário.
while valido == 0:
# pede ao usuário que escolha uma das aplicações do software e, de acordo com a opção escolhida, exibe o próximo input.
    algoritmo = input('Escolha o tipo de sistema que será usado (-substância pura/sp- ou -mistura binária/mb-): ')
    
    if algoritmo == 'substância pura' or algoritmo =='sp':
        valido = 1 # Aceita a resposta do usuário como válida.
        
        resposta = 0 # Cria outro operador para analisar as respostas do usuário.
        
        while resposta == 0: # Enquanto a resposta não for aceitável, requisita o input novamente.
            # Requisita ao usuário o método de input de dadods.
            command = input('Deseja inserir os dados da substância manualmente?(sim/s ou não/n): ')
            # Se o usuário optar por inserir os dados manualmente, requisita, dado a dado, o necessário para o algoritmo.
            if command == 'sim' or command == 's':
                tpt = float(input('Temperatura de ponto triplo(K): '))
                tc = float(input('Temperatura crítica(K): '))
                pc = float(input('Pressão crítica(MPa): '))
                w = float(input('Fator acêntrico:'))
                r = float(input('Constante universal dos gases(J/mol.K): '))
                tol = float(input('Tolerância para a pressão otimizada:' ))
                resposta = 1
            
            # Caso o usuário não escolha a entrada manual de dados, exibe uma lista de substância.
            # A partir da substância escolhida, o software retira os valores de um arquivo .xlsx  para completar os dados.
            if command == 'não' or command == 'n':
            
                dados = pd.read_excel('Dados_Subst_Puras.xlsx')
                substancias = dados["Substância"]
                print(substancias) # Exibe a lista de substâncias.
                i = float(input('Escolha uma substância de acordo com a lista acima (número): '))
                print(dados.loc[i]) # Exibe os dados que vão ser usados para a execução do algoritmo.
                # Atribui valores as variáveis, de acordo com a substância escolhida.
                tpt = ed.ler_dados_xlsx('Dados_Subst_Puras.xlsx',i)['tpt']
                tc = ed.ler_dados_xlsx('Dados_Subst_Puras.xlsx',i)['tc']
                pc = ed.ler_dados_xlsx('Dados_Subst_Puras.xlsx',i)['pc']
                w =  ed.ler_dados_xlsx('Dados_Subst_Puras.xlsx',i)['w']
                r = 8.3145
                tol = 0.000001
                resposta = 1
                
            if resposta == 0: # Caso a escolha esteja fora do ofericido pelo software, assume esse escolha como inválida.
                print('\nA opção inserida é inválida, escolha sua resposta de acordo com as escolhas dadas (sim/s ou não/n): ')
        
        # Cria outro operador para analisar e validar a resposta do usuário.
        marcador = 0
        # Enquanto a escolha do usuário não for válida, o software requisita uma nova escolha e orienta novamente o usuário.
        while marcador == 0:
            escolha = input('\nO software será usado para o cálculo de um único ponto de pressão, ou de uma curva de equilíbrio(-ponto/p- ou -curva/c-): \n')
            if escolha == 'ponto' or escolha == 'p':
                # Valida a resposta do usuário.
                marcador = 1
                # Pede os pontos de temperatura e pressão experimnetal
                t= float(input('Temperatura(K): '))
                p= float(input('Pressão experimental(Mpa): '))
                pexp=p
                
            if escolha == 'curva' or escolha == 'c':
                # Valida a resposta do usuário.
                marcador = 1
                # Orienta o usuário e requisita as sequências de dados que gerarão o gráfico da curva de equilíbrio de pressão.
                print('Observação: Devem ser fornecidos os mesmos números de pontos para pressão e temperatura.\n')
                t = input('Insira uma sequência de pontos para a temperatura(T1,T2,...,Tn): ')
                p = input('Insira uma sequência de pontos para a pressão experimental(P1,P2,...,Pn): ')
                # Organiza os dados em forma de listas para aplicá-los nos algoritmos.
                Tstr = t.split(',')
                T = list(map(float,Tstr))
                Pstr = p.split(',')
                P= list(map(float,Pstr))
                
            # Assume como inválida a resposta e orienta o usuário novamente das escolhas possíveis.
            if marcador == 0:
                print('\nEscolha inválida. As respostas devem ser \"ponto\"/\"p\" ou \"curva\"/\"c\".')
                
        # Se o usuário optar pela curva de equilíbrio, é defino a equação linear para a suposição das pressões e os limites para a construção do gráfico.
        if escolha == 'curva' or escolha == 'c':
            af, bf = lr.linearR(T,P)
            print('\nAviso: se os valores a seguir forem valores muito baixos, o algoritmo pode não convergir nos pontos próximos ao extremos.\n Recomenda-se uma distância mínima de 20 a 50 K, dependendo da substância.\n')
            imin = int(input('Distância do ponto triplo de temperatura: '))
            imax =int(input('Distância do ponto crítico de temperatura: '))
            Imin = int(tpt) + imin
            Imax = int(tc) - imax 
        
        # Se for escolhida a opção ponto, é limitado o loop a uma única iteração.
        if escolha == 'ponto' or escolha == 'p':
            Imin = 0
            Imax = 1
        
        # Define os dados básicos para o algoritmo e as listas que armazenarão os valores para o gráfico.
        r = 8.3145
        tol = 0.000001
        Tx =[]
        Py=[]
        # Aplica o algoritmo de acordo com as opções escolhidas, para vários pontos(curva) , ou para um único ponto.
        for i in range(Imin,Imax):
            
            # Aplica a linearização para chutar valores de pressão em função da temperatura.
            if escolha == 'curva' or escolha == 'c':
                t = i    
                p = af*t - bf
            
            # Se o chute for negativo, o chute é aproximado para um valor próximo de zero.
            if p < 0:
                p = 0.000002 
            # Chama a função para o cálculo da temperatura reduzida.
            tr = fsp.temp_reduzida(t,tc)
            
            # Chama a função para o cálculo do parâmetro de auxílio m.
            m = fsp.parametro_m(w)
            
            # Chama a função para o cálculo do parâmetro de correção.
            alpha = fsp.func_alpha(m,tr)
            
            # Chama a função para o cálculo das constantes de correção dos parãmetros de atração (a) e repulsão (b).
            a = fsp.constante_a(r,tc,pc,alpha)
            b = fsp.constante_b(r,tc,pc)
        
            # Chama a função para o cálculo dos parâmetros auxiliares da equação cúbica.
            A = fsp.constante_A(a,p,r,t)
            B = fsp.constante_B(b,p,r,t)
        
            # Chama a função para o cálculo dos coeficientes cf1, cf2 e cf3 para o cálculo de R e Q.
            cf1, cf2, cf3 = fsp.coeficientes_aux(A,B)
            
            # Chama as funções para o cálculo dos parâmetros Q e R da equação cúbica.
            Q = fsp.func_Q(cf1,cf2)
            R = fsp.func_R(cf1,cf2,cf3)
            
            # Chama a função que calcula o fator de análise para atribuir as raízes da equação cúbica.
            fa = fsp.numero_raizes(Q,R)
            
            # Chama a função que computa os fatores de compressibilidade do líquido(Zl) e do vapor(Zv).
            Zl, Zv = fsp.calcula_fatorcompress(fa,R,Q,cf1,cf2,cf3)
        
            # Chama a função que calcula os coeficientes de fugacidade do líquido(cl) e do vapor(cv).
            cL, cV = fsp.coef_fugacidade(Zl,Zv,A,B)
            
            # Inicia um loop que otimiza o valor da pressão até que os coeficientes de fugacidade do líquido e do vapor sejam numéricamente iguais.
            while abs((cV/cL) - 1) > tol:
                # Recalcula os fatores de correção A e B.
                A = fsp.constante_A(a,p,r,t)
                B = fsp.constante_B(b,p,r,t)
                
                # Recalcula os coeficientes auxilares da equação cúbica.
                cf1, cf2, cf3 = fsp.coeficientes_aux(A,B)
                
                # Recalcula os parâmetros Q e R da equação cúbica.
                Q = fsp.func_Q(cf1,cf2)
                R = fsp.func_R(cf1,cf2,cf3)
                
                # Computa novamente o fator de análise.
                fa = fsp.numero_raizes(Q,R)
                
                # Calcula novamente os fatores de compressibilidade do líquido e do vapor.
                Zl, Zv = fsp.calcula_fatorcompress(fa,R,Q,cf1,cf2,cf3)
                # Recalcula os coeficientes de fugacidade do líquido e do vapor.  
                cL, cV = fsp.coef_fugacidade(Zl,Zv,A,B)
            
                # Otimiza o valor da pressão a partir da razão entre os coeficientes de fugacidade do líquido e do vapor.
                razao = cL/cV
                p = p*razao
             
            # Armazena, caso seja escolhido a opção da curva, os valores das temperaturas experimentais e das pressões otimizadas para a construção do gráfico.
            Tx.append(t)
            Py.append(p)
        
        # Se a opção escolhida foi "ponto", gera um arquivo no formato .txt para exeibir os resultados e os dados usados no algoritmo.
        if escolha == 'ponto' or escolha == 'p':
            print(f'A pressão de equilíbrio para essa temperatura é {p:.4f} MPa')
            
            # Pede ao usuário um nome para o arquivo de resultados que vai ser gerado.
            nomeResultados = input('Escolha o nome do arquivo de resultados: ')
            with open(nomeResultados, 'w') as arq:
                
                # Transforma o arquivo .xlsx com os dados das substâncias em um dataFrame.
                dados = pd.read_excel('Dados_Subst_Puras.xlsx')
                
                # As linhas a seguri configuram o arquivo de resultados que será gerrado.
                arq.write(' Dados experimentais e Resultados '.center(60, '#')+'\n')
                arq.write('\n ----- Dados experimentais -----\n')
                arq.write(f'Pressão Crítica: {pc} Mpa\n')
                arq.write(f'Temperatura Crítica: {tc} K\n')
                arq.write(f'Fator Acêntrico: {w}\n')
                arq.write(f'Temperatura da substância: {t} K\n')
                arq.write(f'Pressão Experimental: {pexp} MPa\n')
                arq.write('\n ---------- Resultado ----------\n')
                arq.write(f'Pressão Calculada: {p:.4f} MPa\n')
                arq.write('#'*60+'\n')
            
            # Avisa ao usuário que o arquivo de resultados foi gerado.
            print('Um arquivo com o nome escolhido foi gerado no diretório em que se encontra o TermoPython')
        # Caso a opção escolhida tenha sido "curva", configura o gráfico da curva de pressão.
        if escolha == 'curva' or escolha == 'c':
            plt.figure()
            plt.grid()
            plt.title('Pressão de equilíbrio de fase x Temperatura')
            plt.plot(Tx,Py)
            plt.xlabel('Temperatura (K)')
            plt.ylabel('Pressão de equilíbrio(MPa)')
            plt.savefig('gráfico')
            plt.show()
            
            # Avisa ao usuário que o gráfico gerado foi baixado e onde foi baixado.
            print('\n O gráfico foi baixado em formato .png no diretório em que se encontra o TermoPython.')
    
        
    if algoritmo == 'mistura binária' or algoritmo =='mb':
        # Atualiza a escolha do sistema como válida.
        valido = 1
        
        # Cria um operador para analizar a escolha da forma de input de dados.
        resposta2 = 0
        
        # Enquanto a resposta for inválida, pede uma nova reposta ao usuário.
        while resposta2 == 0:
            command = input('Deseja inserir os dados da substância manualmente?(sim/s ou não/n): ')
            
            # Se o usuário escolher por inserir os dados manualmente, requisita a ele dado por dado.
            if command == 'sim' or command == 's':
                k = 1.13e-4
                t= float(input('Temperatura do sistema(K): '))
                r = 0.08205
                tc1= float(input('Temperatura crítica do 1º componente(K): '))
                tc2= float(input('Temperatura crítica do 2º componente(K): '))
                pc1= float(input('Pressão crítica do 1º componente(atm): '))
                pc2= float(input('Pressão crítica do 2º componente(atm): '))
                w1= float(input('fator acêntrico do 1º componente: '))
                w2= float(input('fator acêntrico do 2º componente: '))
                # Atualiza a resposta como válida.
                resposta2 = 1
            
            # Caso o usuário use a entrada a partir da base de dados,os valores serão atribuidos às variáveis a partir de um arquivo no formato .xlsx.
            if command == 'não' or command == 'n':
                # Transforma o arquivo .xlsx em um dataFrame.
                dados = pd.read_excel('Dados_Misturas.xlsx')
                
                # Exibe a lista de sistemas disponíveis para a entrada automática dos dados característicos do sistema.
                sistema = dados["Sistema"]
                print(sistema)
                i = float(input('Selecione um sistema de acordo com a lista acima (número): '))
                print(f'{dados.loc[i]}\n\n')
                
                # A partir da escolha do usuário, atribui os valores das variáveis por meio do arquivo .xlsx.
                t = t= float(input('Temperatura do sistema(K): '))
                k = 1.13e-4
                r = 0.08205
                tc1 = ed.ler_dados_mistura_xlsx('Dados_Misturas.xlsx',i)['tc1']
                tc2 = ed.ler_dados_mistura_xlsx('Dados_Misturas.xlsx',i)['tc2']
                pc1 = ed.ler_dados_mistura_xlsx('Dados_Misturas.xlsx',i)['pc1']
                pc2 = ed.ler_dados_mistura_xlsx('Dados_Misturas.xlsx',i)['pc2']
                w1 = ed.ler_dados_mistura_xlsx('Dados_Misturas.xlsx',i)['w1']
                w2 = ed.ler_dados_mistura_xlsx('Dados_Misturas.xlsx',i)['w2']
               
                # Assume a escolha do usuário como válida.
                resposta2 = 1
            
            # Caso a resposta continue inválida orienta o usuário novamente sobre o input.
            if resposta2 == 0:
                print('\nA opção inserida é inválida, escolha sua resposta de acordo com as escolhas dadas (sim/s ou não/n).')
        
        # Cria um operador para avaliar as escolhas de ponto e curva.
        marcador2 = 0
        
        # Enquanto a escolha n for de acordo com o proposto, pede novamente uma reposta ao usuário.
        while marcador2 == 0:
            escolha = input('\nQual cálculo será efetuado, de um único ponto, ou de uma curva de equilíbrio(-ponto/p- ou -curva/c-): ')
            if escolha == 'ponto' or escolha == 'p':
                # Atualiza a resposta como válida.
                marcador2 = 1
                
                # Pede os pontos experimentais para calcular a pressão otimizada.
                p= float(input('Pressão experimental(atm): '))
                pexp = p
                x1 = float(input('Fração molar da fase líquida: '))
                y1 = float(input('Fração molar da fase vapor: '))
                
            if escolha == 'curva' or escolha == 'c':
                
                # Atualiza a resposta como válida.
                marcador2 = 1
                
                # Pede a sequência de dados experimentais para aplicar ao algoritmo.
                print('Observação: Devem ser fornecidos a mesma quantidade de pontos para pressão e para cada fração molar.\n')
                p = input('Insira uma sequência de pontos para a pressão experimental(P1,P2,...,Pn): ')
                x  = input('Insira uma sequência de pontos para a fração molar da fase líquida(X1,X2,...,Xn): ')
                y = input('Insira uma sequência de pontos para a fração molar da fase vapor(Y1,Y2,...,Yn): ')
                
                # Separa os dados em forma de listas para serem processados no algoritmo.
                Pstr = p.split(',')
                P= list(map(float,Pstr))
                Xstr = x.split(',')
                X1 = list(map(float,Xstr))
                Ystr = y.split(',')
                Y1 = list(map(float,Ystr))
            
            # Se a escolha do usuário for inválida, ele é orientado sobre a forma correta de escolha e o input é rwquisitado novamente.
            if marcador2 == 0:
                print('\nEscolha inválida. As respostas devem ser \"ponto\"/\"p\" ou \"curva\"/\"c\".')
             
            
        
        
        # Aplica o algoritmo para a escolha "ponto".
        if escolha == 'ponto' or escolha == 'p':
            
            # Chama a função para o cáculo da temperatura reduzida dos dois componetes do sistema.
            tr1 = fsp.temp_reduzida(t,tc1)
            tr2 = fsp.temp_reduzida(t, tc2)
            
            # Chama a função para o cálculo dos parâmetros de auxílio m dos dois componentes do sistema.
            m1 = fsp.parametro_m(w1)
            m2 = fsp.parametro_m(w2)
            
            # Chama a função para o cálculo dos parâmetros de correção de cada componente do sistema.
            alpha_1 = fsp.func_alpha(m1,tr1)
            alpha_2 = fsp.func_alpha(m2,tr2)
            
            # Chama a função para o cálculo das constantes de correção do parâmetro de atração de cada componente.
            a1 = fsp.constante_a(r,tc1,pc1,alpha_1)
            a2 = fsp.constante_a(r,tc2,pc2,alpha_2)
            
            # Chama a função para o cálculo das constantes de correção do parâmetro de repulsão de cada componente.
            b1 = fsp.constante_b(r,tc1,pc1)
            b2 = fsp.constante_b(r,tc2,pc2)
            
            # Cálculo das frações molares complementares da fase líquida(x2) e da fase vapor(y2), a partir das frações fornecidas pelo usuário.
            x2 = 1 - x1
            y2 = 1 - y1
            
            #Arrays que armazenam os valores das frações molares de cada fase do sistema.
            Mx = np.array([x1,x2], dtype = float)
            My = np.array([y1,y2], dtype = float)
            
            # Array que armazena a temperatura reduzida de cada componente da mistura.
            Mtr = np.array([tr1,tr2], dtype = float)
            
            # Array que armazena o valor dos parâmetros de correção de cada componente.
            Malpha = np.array([alpha_1,alpha_2], dtype = float)
            
            # Array que armazena os valores dos parâmetros auxiliares dos componentes do sistema.
            Mm = np.array([m1,m2], dtype = float)  
            
            # Arrays que armazenam as constantes de correção dos fatores de atração(Mai) e de repulsão(Mbi).
            Mai = np.array([a1,a2], dtype = float)   
            Mbi = np.array([b1,b2], dtype = float)
            
            # Array de zeros 2 x 2 que vai armazenar os parâmetros aii e aij, que são usados para o cálculo do parâmetro de atração do líquido e do vapor.
            Ma = np.array([[0,0],
                          [0,0]],dtype = float)
            
            # loop que realiza os cálculos dos parâmetros para os dois componentes.
            for i in range(0,2):
                j = 1 - i 
                
                # Cálculo, respectivamente, do parâmetro aii e do parâmetro aij.
                Ma[i][i] = Mai[i]
                Ma[i][j] = fm.parametro_aij(a1,a2,k)
                
            
            # Chama a função que calcula os parâmetros de atração da fase líquida(al) e da fase vapor(av).
            al = fm.parametro_atract(Ma,Mx,My)['al']
            av = fm.parametro_atract(Ma,Mx,My)['av']
            
            # Chama a função que calcula os parâmetros de repulsão da fase líquida(bl) e da fase vapor(bv).
            bl = fm.parametro_repulse(Mbi,Mx,My)['bl']
            bv = fm.parametro_repulse(Mbi,Mx,My)['bv']
            
            # Chama a função que realiza o cálculo da constante A de auxílio do líquido(Al) e do vapor(Av) da equação cúbica.
            Al = fsp.constante_A(al,p,r,t)
            Av = fsp.constante_A(av,p,r,t)
            
            # Chama a função que realiza o cálculo da constante B de auxílio do líquido(Bl) e do vapor(Bv) da equação cúbica.
            Bl = fsp.constante_B(bl,p,r,t)
            Bv = fsp.constante_B(bv,p,r,t)
            
            # Arrays que armazenam as constantes de auxílio A e B da equação cúbica.
            MA = np.array([Al,Av]) 
            MB = np.array([Bl,Bv])
            
            # Chama a função que computa, a partir das raízes da equação cúbica.
            Zl = fm.fatorcompress(MA,MB)['l']
            Zv = fm.fatorcompress(MA,MB)['v']
            
            # Criação de arrays de zeros para armazenar os valores dos logaritmos dos coeficientes de fugacidade do líquido e do vapor e de seus respectivos coeficientes.
            Mln_l = np.array([0,0], dtype = float)
            Mln_v = np.array([0,0], dtype = float)
            Mphi_l = np.array([0,0], dtype = float)
            Mphi_v = np.array([0,0], dtype = float)
            
            # Chama a função que calcula os coeficientes de fugacidade do líquido e do vapor.
            Mphi_l = fm.coef_fugacidade(Zl,Zv,Mx,My,al,av,bl,bv,Ma,Mbi,MA,MB)['l']
            Mphi_v = fm.coef_fugacidade(Zl,Zv,Mx,My,al,av,bl,bv,Ma,Mbi,MA,MB)['v']
            
            # Chama a função que calcula a fugacidadde do líquido e do vapor a partir dos coeficientes de fugacidade.
            Mfl = fm.fugacidade(Mphi_l,Mphi_v,Mx,My,p)['l']
            Mfv = fm.fugacidade(Mphi_l,Mphi_v,Mx,My,p)['v']
            
            # Chama a função que otimiza o valor das fraçôes molares do vapor.
            MyI = fm.y_otimizado(My,Mfl,Mfv)
            
            # Laço recursivo que repete o algoritimo até que os valores da pressão e da fração molar do vapor estejam totalmente otimizados.
            while abs((Mfl[i]/Mfv[i])-1) >1e-14:
                
                # Otimiza o valor da pressão.
                p = p*np.sum(MyI)
                
                # Troca os valores antigos da fração molar do vapor(y) de cada componente, pelos valores otimizados a cada iteração do while.
                for i in range(0,2):
                    My[i] = MyI[i]
                
            # Refaz o algoritmo desde os cálculos dos parâmetros de atração e de repulsão para cada iteração do laço.
                al = fm.parametro_atract(Ma,Mx,My)['al']
                av = fm.parametro_atract(Ma,Mx,My)['av']
                
                bl = fm.parametro_repulse(Mbi,Mx,My)['bl']
                bv = fm.parametro_repulse(Mbi,Mx,My)['bv']
                
                Al = fsp.constante_A(al,p,r,t)
                Av = fsp.constante_A(av,p,r,t)
                
                Bl = fsp.constante_B(bl,p,r,t)
                Bv = fsp.constante_B(bv,p,r,t)
                
                MA = np.array([Al,Av]) 
                MB = np.array([Bl,Bv])
                
                Zl = fm.fatorcompress(MA,MB)['l']
                Zv = fm.fatorcompress(MA,MB)['v']
                
                Mln_l = np.array([0,0], dtype = float)
                Mln_v = np.array([0,0], dtype = float)
                Mphi_l = np.array([0,0], dtype = float)
                Mphi_v = np.array([0,0], dtype = float)
                
                
                Mphi_l = fm.coef_fugacidade(Zl,Zv,Mx,My,al,av,bl,bv,Ma,Mbi,MA,MB)['l']
                Mphi_v = fm.coef_fugacidade(Zl,Zv,Mx,My,al,av,bl,bv,Ma,Mbi,MA,MB)['v']
                
                
                Mfl = fm.fugacidade(Mphi_l,Mphi_v,Mx,My,p)['l']
                Mfv = fm.fugacidade(Mphi_l,Mphi_v,Mx,My,p)['v']
                
                MyI = fm.y_otimizado(My,Mfl,Mfv)
            
            # Exibe a pressão totalmente otimizada obtida ao fim da recursão.
            print(f'\nA pressão de equilíbrio para essa temperatura é {p:.4f} atm')
            
            # Requisita ao usuário um nome para o arquivo .txt que exibirá os resultados e os dados usados no algoritmo.
            nomeResultados = input('escolha o nome do arquivo de resultados: ')
            with open(nomeResultados, 'w') as arq:  

                # Constrói os dados usados e os resultados obtidos dentro do arquivo .txt.
                arq.write('Dados experimentais e Resultados'.center(60, '#')+'\n')
                arq.write('\n ----- Dados experimentais -----\n')
                arq.write(f'Pressão Crítica do Componente 1: {pc1} atm\n')
                arq.write(f'Pressão Crítica do Componente 2: {pc2}atm \n')
                arq.write(f'Temperatura Crítica do  Componente 1: {tc1} K\n')
                arq.write(f'Temperatura Crítica do Componente 2: {tc2} K\n')
                arq.write(f'Fator Acêntrico do Componente 1: {w1}\n')
                arq.write(f'Fator Acêntrico do Componente 2: {w2}\n')
                arq.write(f'Temperatura do Sistema: {t} K\n')
                arq.write(f'Fração Molar Experimental da Fase Líquida: {x1}\n')
                arq.write(f'Fração Molar Experimental da Fase Vapor: {y1}\n')
                arq.write(f'Pressão Experimental: {pexp} atm\n')
                arq.write('\n ---------- Resultado ----------\n')
                arq.write(f'Pressão Calculada: {p:.4f} atm\n')
                arq.write(f'Fração Calculada da Fase Vapor: {MyI[0]:.4f}\n')
                arq.write('#'*60+'\n')
            
            # Avisa o usuário que o arquvo foi gerado e onde ele foi gerado.
            print(f'O arquivo {nomeResultados} foi gerado no diretório em que se encontra o TermoPython')
                        
                
        # Se opção escolhida for "curva", realiza o algoritmo para a sequência de pontos fornecidas pelo usuário.
        if escolha == 'curva' or escolha == 'c':
            
            # Realiza o algoritmo para cada ponto fornecido pelo usuário.
            for i in range(len(P)):
                x1 = X1[i]
                y1 = Y1[i]
                p = P[i]
                
                # Chama a função para o cáculo da temperatura reduzida dos dois componetes do sistema.
                tr1 = fsp.temp_reduzida(t,tc1)
                tr2 = fsp.temp_reduzida(t, tc2)
                
                # Chama a função para o cálculo dos parâmetros de auxílio m dos dois componentes do sistema.
                m1 = fsp.parametro_m(w1)
                m2 = fsp.parametro_m(w2)
                
                # Chama a função para o cálculo dos parâmetros de correção de cada componente do sistema.
                alpha_1 = fsp.func_alpha(m1,tr1)
                alpha_2 = fsp.func_alpha(m2,tr2)
                
                # Chama a função para o cálculo das constantes de correção do parâmetro de atração de cada componente.
                a1 = fsp.constante_a(r,tc1,pc1,alpha_1)
                a2 = fsp.constante_a(r,tc2,pc2,alpha_2)
                
                # Chama a função para o cálculo das constantes de correção do parâmetro de repulsão de cada componente.
                b1 = fsp.constante_b(r,tc1,pc1)
                b2 = fsp.constante_b(r,tc2,pc2)
                
                # Cálculo das frações molares complementares da fase líquida(x2) e da fase vapor(y2), a partir das frações fornecidas pelo usuário.
                x2 = 1 - x1
                y2 = 1 - y1
                
                #Arrays que armazenam os valores das frações molares de cada fase do sistema.
                Mx = np.array([x1,x2], dtype = float)
                My = np.array([y1,y2], dtype = float)
                
                # Array que armazena a temperatura reduzida de cada componente da mistura.
                Mtr = np.array([tr1,tr2], dtype = float)
                
                # Array que armazena o valor dos parâmetros de correção de cada componente.
                Malpha = np.array([alpha_1,alpha_2], dtype = float)
                
                # Array que armazena os valores dos parâmetros auxiliares dos componentes do sistema.
                Mm = np.array([m1,m2], dtype = float)   
                
                # Arrays que armazenam as constantes de correção dos fatores de atração(Mai) e de repulsão(Mbi).
                Mai = np.array([a1,a2], dtype = float)   
                Mbi = np.array([b1,b2], dtype = float)
                
                # Array de zeros 2 x 2 que vai armazenar os parâmetros aii e aij, que são usados para o cálculo do parâmetro de atração do líquido e do vapor.
                Ma = np.array([[0,0],
                              [0,0]],dtype = float)
                
                
                # laço que realiza os cálculos dos parâmetros aii e aij para os dois componentes.
                for i in range(0,2):
                    j = 1 - i 
                     
                    Ma[i][i] = Mai[i]
                    Ma[i][j] = fm.parametro_aij(a1,a2,k)
                    
                
                # Chama a função que calcula os parâmetros de atração da fase líquida(al) e da fase vapor(av).
                al = fm.parametro_atract(Ma,Mx,My)['al']
                av = fm.parametro_atract(Ma,Mx,My)['av']
                
                # Chama a função para o cálculo das constantes de correção do parâmetro de repulsão de cada componente.
                bl = fm.parametro_repulse(Mbi,Mx,My)['bl']
                bv = fm.parametro_repulse(Mbi,Mx,My)['bv']
                
                # Chama a função que realiza o cálculo da constante A de auxílio do líquido(Al) e do vapor(Av) da equação cúbica.
                Al = fsp.constante_A(al,p,r,t)
                Av = fsp.constante_A(av,p,r,t)
                
                # Chama a função que realiza o cálculo da constante B de auxílio do líquido(Bl) e do vapor(Bv) da equação cúbica.
                Bl = fsp.constante_B(bl,p,r,t)
                Bv = fsp.constante_B(bv,p,r,t)
                
                # Arrays que armazenam as constantes de auxílio A e B da equação cúbica.
                MA = np.array([Al,Av]) 
                MB = np.array([Bl,Bv])
                
                # Chama a função que computa, a partir das raízes da equação cúbica.
                Zl = fm.fatorcompress(MA,MB)['l']
                Zv = fm.fatorcompress(MA,MB)['v']
                
                # Criação de arrays de zeros para armazenar os valores dos logaritmos dos coeficientes de fugacidade do líquido e do vapor e de seus respectivos coeficientes.
                Mln_l = np.array([0,0], dtype = float)
                Mln_v = np.array([0,0], dtype = float)
                Mphi_l = np.array([0,0], dtype = float)
                Mphi_v = np.array([0,0], dtype = float)
                
                # Chama a função que calcula os coeficientes de fugacidade do líquido e do vapor.
                Mphi_l = fm.coef_fugacidade(Zl,Zv,Mx,My,al,av,bl,bv,Ma,Mbi,MA,MB)['l']
                Mphi_v = fm.coef_fugacidade(Zl,Zv,Mx,My,al,av,bl,bv,Ma,Mbi,MA,MB)['v']
                
                # Chama a função que calcula a fugacidadde do líquido e do vapor a partir dos coeficientes de fugacidade.
                Mfl = fm.fugacidade(Mphi_l,Mphi_v,Mx,My,p)['l']
                Mfv = fm.fugacidade(Mphi_l,Mphi_v,Mx,My,p)['v']
                
                # Chama a função que otimiza o valor das fraçôes molares do vapor.
                MyI = fm.y_otimizado(My,Mfl,Mfv)
                
                # Laço recursivo que repete o algoritimo até que os valores da pressão e da fração molar do vapor estejam totalmente otimizados.
                while abs((Mfl[i]/Mfv[i])-1) >1e-14:
                    
                    # Otimiza o ponto de pressão
                    p = p*np.sum(MyI)
                    
                    # Troca os valores antigos da fração molar do vapor(y) de cada componente, pelos valores otimizados a cada iteração do while.
                    for i in range(0,2):
                        My[i] = MyI[i]
                    
                    # Refaz o algoritmo desde os cálculos dos parâmetros de atração e de repulsão para cada iteração do laço.
                    al = fm.parametro_atract(Ma,Mx,My)['al']
                    av = fm.parametro_atract(Ma,Mx,My)['av']
                    
                    bl = fm.parametro_repulse(Mbi,Mx,My)['bl']
                    bv = fm.parametro_repulse(Mbi,Mx,My)['bv']
                        
                    Al = fsp.constante_A(al,p,r,t)
                    Av = fsp.constante_A(av,p,r,t)
                    
                    Bl = fsp.constante_B(bl,p,r,t)
                    Bv = fsp.constante_B(bv,p,r,t)
                    
                    MA = np.array([Al,Av]) 
                    MB = np.array([Bl,Bv])
                    
                    Zl = fm.fatorcompress(MA,MB)['l']
                    Zv = fm.fatorcompress(MA,MB)['v']
                    
                    Mln_l = np.array([0,0], dtype = float)
                    Mln_v = np.array([0,0], dtype = float)
                    Mphi_l = np.array([0,0], dtype = float)
                    Mphi_v = np.array([0,0], dtype = float)
                    
                    
                    Mphi_l = fm.coef_fugacidade(Zl,Zv,Mx,My,al,av,bl,bv,Ma,Mbi,MA,MB)['l']
                    Mphi_v = fm.coef_fugacidade(Zl,Zv,Mx,My,al,av,bl,bv,Ma,Mbi,MA,MB)['v']
                    
                    
                    Mfl = fm.fugacidade(Mphi_l,Mphi_v,Mx,My,p)['l']
                    Mfv = fm.fugacidade(Mphi_l,Mphi_v,Mx,My,p)['v']
                    
                    MyI = fm.y_otimizado(My,Mfl,Mfv)
                    
                Py.append(p)
            
            # Avisa o usuário sobre o local em que será baixado o código.
            print('\n O gráfico foi baixado em formato .png no diretório em que se encontra o TermoPython.')
            
            # COnfigura o gráfico com as curvas de P em função de x1 e P em função de y1 e com os pontos experimentais de pressão respectivos para cada curva.
            plt.figure()
            plt.plot(X1,Py,label='Peq. x Fração molar do líquido',color ='b')
            plt.plot(Y1,Py,label='Peq. x Fração molar do vapor',color='r')
            plt.plot(X1,P,'o',label ='Pex. x Fração molar do líquido',color ='m')
            plt.plot(Y1,P,'o', label='Pex. x Fração molar do vapor',color ='k' )
            plt.title('Gráfico de comparação das pressões de equilíbrio(Peq.) e experimental(Pex.)\n')
            plt.grid()
            plt.xlabel('Pressão (atm)')
            plt.ylabel('Fração molar')
            plt.legend(fontsize='small')
            plt.savefig('gráfico')
            plt.show()
    
    if algoritmo == 'EEL':
        valido = 1
        eel = fm.leleno()
        print(eel)

    # Se a opção escolhida pelo usuário não for aceita, e requisitada uma nova escolha.
    if valido == 0:
        print('\n Resposta inválida. Seleciona o uso dentre as opções dadas.')
        
