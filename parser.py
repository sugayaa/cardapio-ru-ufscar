import os
from html.parser import HTMLParser
from dateutil.parser import parse

leiaCardapio = False
dias = -1
conjDias = []
qualRef = 0
whatItemAmI = 0

os.system("./download.sh")

class refeicao():
    'classe referente a almoços e jantares, refeicoes'
    periodo = ""
    pratoPrincipalCarne = ""
    pratoPrincipalVegetariano = ""
    guarnicao = ""
    arroz = ""
    feijao = ""
    saladas = ""
    sobremesa = ""

    def imprime(self):
        print("Periodo:", self.periodo)
        print("Prato Principal Carne :", self.pratoPrincipalCarne)
        print("Prato Principal Vegetariano ♡:", self.pratoPrincipalVegetariano)
        print("Guarnicao:", self.guarnicao)
        print("Arroz:", self.arroz)
        print("Feijao:", self.feijao)
        print("Saladas:", self.saladas)
        print("Sobremesa:", self.sobremesa)

class diaDaSemana():
    'classe referente a um dia no ru'
    data = ""
    diaDaSemana = ""
    almoco = refeicao()
    jantar = refeicao()

    def imprime(self):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("%d/%d/%d - %s" % (self.data.day, self.data.month, self.data.year, self.diaDaSemana))
        self.almoco.imprime()
        self.jantar.imprime()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

semana = []
for dia in range(7):
    semana.append(diaDaSemana())

refeicaoAtual = refeicao()

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if(len(attrs) != 0):
                if attrs[0][0] == 'id' and attrs[0][1] =='cardapio':
                    global leiaCardapio
                    leiaCardapio = True


    def handle_data(self, data):
        global leiaCardapio
        global dias
        global conjDias
        global qualRef
        global whatItemAmI
        global refeicaoAtual
        reset = False

        if(data == "Acompanhe as notícias da UFSCar também pelas redes sociais oficiais da Universidade "):
            leiaCardapio = False

        if(leiaCardapio):
            tam = data.split()
            if len(tam) > 0:
                #print("Encontrei alguns dados:", data)
                try :
                    d = parse(data, dayfirst=True)
                    #print("%d/%d/%d" % (d.day, d.month, d.year))
                    if d not in conjDias:
                        dias += 1
                        setattr(semana[dias], 'data', d)
                        conjDias.append(d)
                        qualRef = 0
                        #print("-------->Data não está no conjunto de dias")
                    else:
                        #print("-------->Data está no conjunto de dias")
                        if qualRef == 0:
                            qualRef = 1
                        else:
                            print("qualRef está com valor estranho")
                except:
                    if whatItemAmI == 7 and data != "Sobremesa: ":
                        setattr(refeicaoAtual, 'sobremesa', data)
                        #print("Li oitavo item, sobremesa")
                        #print(data)
                        whatItemAmI += 1

                        #ultimo item, incrementando refeicao a dia
                        if qualRef == 0:
                            setattr(semana[dias], 'almoco', refeicaoAtual)
                        elif qualRef == 1:
                            setattr(semana[dias], 'jantar', refeicaoAtual)
                        else:
                            print("Erro ao atribuir refeicao a dia. handle_data:except:whatItemAmI == 7")

                        #limpando refeicao atual
                        refeicaoAtual = refeicao()
                        #recomecando leitura de nova refeicao
                        whatItemAmI = 0
                        reset = True


                    if whatItemAmI == 6 and data != "Saladas: ":
                        setattr(refeicaoAtual, 'saladas', data)
                        #print("Li setimo item, salada")
                        #print(data)
                        whatItemAmI += 1

                    if whatItemAmI == 5 and data != "Feijão: ":
                        setattr(refeicaoAtual, 'feijao', data)
                        #print("Li sexto item, feijao")
                        #print(data)
                        whatItemAmI += 1

                    if whatItemAmI == 4 and data != "Arroz: ":
                        setattr(refeicaoAtual, 'arroz', data)
                        #print("Li quinto item, arroz")
                        #print(data)
                        whatItemAmI += 1

                    if whatItemAmI == 3 and data != "Guarnição: ":
                        setattr(refeicaoAtual, 'guarnicao', data)
                        #print("Li quarto item, guarnicao")
                        #print(data)
                        whatItemAmI += 1

                    if whatItemAmI == 2 and data != "Prato Principal: ":
                        try:
                            carne, veg = data.split("/ ")
                            setattr(refeicaoAtual, 'pratoPrincipalCarne', carne)
                            setattr(refeicaoAtual, 'pratoPrincipalVegetariano', veg)
                            #print("Li terceiro item, prato principal")
                            #print("Carnista:",carne)
                            #print("Vegetariano:", veg)
                        except:
                            try: #sdds padroes
                                carne, veg = data.split("/")
                                setattr(refeicaoAtual, 'pratoPrincipalCarne', carne)
                                setattr(refeicaoAtual, 'pratoPrincipalVegetariano', veg)
                            except:
                                #print("Valor indefinido")
                                setattr(refeicaoAtual, 'pratoPrincipalCarne', data)
                        whatItemAmI += 1


                    if whatItemAmI == 1 and data != " - ":
                        setattr(refeicaoAtual, 'periodo', data.capitalize())
                        #print("Li segundo item, periodo")
                        #print(data.capitalize())
                        whatItemAmI += 1

                    if whatItemAmI == 0 and data != ": " and not reset:
                        if data != "Bebida: " and data != "Não Definido.":
                            setattr(semana[dias], 'diaDaSemana', data)
                            #print("Li primeiro item, dia da semana")
                            #print(data)
                            whatItemAmI += 1



                    print("",end='')



f = open("ru.html", "r")
myhtml = f.read()
#print(myhtml)
parser = MyHTMLParser()
parser.feed(myhtml)
f.close()

#print("MYDEBUG:")

#print(semana)
#print("ENDMYDEBUG")

print()
print()

#semana[0].imprime()
#semana[1].imprime()
for dia in semana:
    dia.imprime()

print("\tI like to eat avocados\tAVOCADOS")


