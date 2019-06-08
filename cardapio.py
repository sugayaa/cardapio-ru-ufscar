import os
from html.parser import HTMLParser
from dateutil.parser import parse
import subprocess

###### GLOBAL VARIABLES ######################

TAB_SIZE = 35
SND_TAB_SIZE = 20
leiaCardapio = False
dias = -1
conjDias = []
qualRef = 0
whatItemAmI = 0

##############################################



####### CLASSES ##############################

class refeicao:
    'classe referente a almoços e jantares, refeicoes'
    def __init__(self):
       self.periodo = ""
       self.pratoPrincipalCarne = ""
       self.pratoPrincipalVegetariano = ""
       self.guarnicao = ""
       self.arroz = ""
       self.feijao = ""
       self.saladas = ""
       self.sobremesa = ""

    def imprime(self):
        print("Periodo:", self.periodo)
        print("Prato Principal Carne :", self.pratoPrincipalCarne)
        print("Prato Principal Vegetariano ♡:", self.pratoPrincipalVegetariano)
        print("Guarnicao:", self.guarnicao)
        print("Arroz:", self.arroz)
        print("Feijao:", self.feijao)
        print("Saladas:", self.saladas)
        print("Sobremesa:", self.sobremesa)

class diaDaSemana:
    'classe referente a um dia no ru'
    def __init__(self):
        self.data = ""
        self.diaDaSemana = ""
        self.almoco = refeicao()
        self.jantar = refeicao()

    def imprime(self):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("%d/%d/%d - %s" % (self.data.day, self.data.month, self.data.year, self.diaDaSemana))
        self.almoco.imprime()
        self.jantar.imprime()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

####### LOOSE GLOBAL VARIABLES ###############
semana = []
for dia in range(7):
    semana.append(diaDaSemana())
refeicaoAtual = refeicao()
#############################################

####### PROGRAM CORE ########################
class HTMLParser(HTMLParser):
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
        global semana
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

#############################################
#############################################


###### FUNCTIONS ##################################################################################
def getRes():
    x_output = subprocess.check_output(["xrandr"])
    res_ant = ""
    for it in x_output.split():
        curr_it = str(it)
        if "*" in curr_it:
            return res_ant
        res_ant = it

def getDataEDia(index):
    global semana
    dataEDia = ""

    dataEDia += printDate(getattr(semana[index], 'data'))
    dataEDia += " - "
    dataEDia += getattr(semana[index], 'diaDaSemana')
    dataEDia += " "

    return dataEDia

def getHeader(day):
    header = "~~ " + getDataEDia(day) + "~" * (TAB_SIZE - 3 - len(getDataEDia(day)))
    return header

def getFooter():
    return "~" * TAB_SIZE

def getMealLine(index):
    global semana
    refeicao = getattr(semana[index], 'almoco')
    carne = getattr(refeicao, 'pratoPrincipalCarne')
    mealLine = "* "
    if len(carne) > TAB_SIZE - 4:
        carne = carne[0:TAB_SIZE - 7]
        carne += "..."
        mealLine += carne
    else:
        mealLine += carne
        mealLine += " " * (TAB_SIZE - len(carne) - 4)

    mealLine += " *"
    return mealLine

def getMealLine(index, meal, attr):
    global semana
    refeicao = getattr(semana[index], meal)
    food = getattr(refeicao, attr)
    mealLine = "* "

    if attr == "arroz":
        mealLine += "Arroz "
    elif attr == "feijao":
        mealLine += "Feijão "
    elif attr == "saladas":
        mealLine += "Salada "

    if len(food) > TAB_SIZE - 4:
        food = food[0:TAB_SIZE - 5 - len(mealLine)] #3 from "..." + 2 from " *"
        food += "..."
        mealLine += food
    else:
        mealLine += food
        mealLine += " " * (TAB_SIZE - 2 - len(mealLine)) #2 from " *"

    mealLine += " *"
    return mealLine

def getBlankLine():
    blankLine = "*" + " " * (TAB_SIZE - 2) + "*"
    return blankLine

def getTitleLine(title):
    titleline = "* >>>"
    titleline += title.capitalize()
    titleline += " " * (TAB_SIZE - 12)
    titleline += "*"
    return titleline

def printDate(date):
    return '{}/{}/{}'.format(date.day, date.month, date.year)

def main():
    #html downloader and updater
    os.system("./download.sh")
    global TAB_SIZE
    global SND_TAB_SIZE

    #refeicaoAtual = refeicao()

    f = open("ru.html", "r")
    html = f.read()
    parser = HTMLParser()
    parser.feed(html)
    f.close()

    #for dia in semana:
    #    dia.imprime()


    r = getRes().decode("utf-8")
    if r == "1600x900":
        print("\t\t\t\t\t\t\t\t     CARDAPIO DA SEMANA")
        print(getHeader(0), "\t", sep='',end='')
        print(getHeader(1), "\t", sep='',end='')
        print(getHeader(2), "\t", sep='',end='')
        print(getHeader(3), "\n", sep='',end='')

        print(getTitleLine('almoço'),"\t",sep='',end='')
        print(getTitleLine('almoço'),"\t",sep='',end='')
        print(getTitleLine('almoço'),"\t",sep='',end='')
        print(getTitleLine('almoço'),"\n",sep='',end='')

        print(getMealLine(0,'almoco','pratoPrincipalCarne'),"\t",sep='',end='')
        print(getMealLine(1,'almoco','pratoPrincipalCarne'),"\t",sep='',end='')
        print(getMealLine(2,'almoco','pratoPrincipalCarne'),"\t",sep='',end='')
        print(getMealLine(3,'almoco','pratoPrincipalCarne'),"\n",sep='',end='')

        print(getMealLine(0,'almoco','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print(getMealLine(1,'almoco','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print(getMealLine(2,'almoco','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print(getMealLine(3,'almoco','pratoPrincipalVegetariano'),"\n",sep='',end='')

        print(getMealLine(0,'almoco','arroz'),"\t",sep='',end='')
        print(getMealLine(1,'almoco','arroz'),"\t",sep='',end='')
        print(getMealLine(2,'almoco','arroz'),"\t",sep='',end='')
        print(getMealLine(3,'almoco','arroz'),"\n",sep='',end='')

        print(getMealLine(0,'almoco','feijao'),"\t",sep='',end='')
        print(getMealLine(1,'almoco','feijao'),"\t",sep='',end='')
        print(getMealLine(2,'almoco','feijao'),"\t",sep='',end='')
        print(getMealLine(3,'almoco','feijao'),"\n",sep='',end='')

        print(getMealLine(0,'almoco','guarnicao'),"\t",sep='',end='')
        print(getMealLine(1,'almoco','guarnicao'),"\t",sep='',end='')
        print(getMealLine(2,'almoco','guarnicao'),"\t",sep='',end='')
        print(getMealLine(3,'almoco','guarnicao'),"\n",sep='',end='')

        print(getMealLine(0,'almoco','saladas'),"\t",sep='',end='')
        print(getMealLine(1,'almoco','saladas'),"\t",sep='',end='')
        print(getMealLine(2,'almoco','saladas'),"\t",sep='',end='')
        print(getMealLine(3,'almoco','saladas'),"\n",sep='',end='')

        print(getMealLine(0,'almoco','sobremesa'),"\t",sep='',end='')
        print(getMealLine(1,'almoco','sobremesa'),"\t",sep='',end='')
        print(getMealLine(2,'almoco','sobremesa'),"\t",sep='',end='')
        print(getMealLine(3,'almoco','sobremesa'),"\n",sep='',end='')

        print(getBlankLine(),"\t",sep='',end='')
        print(getBlankLine(),"\t",sep='',end='')
        print(getBlankLine(),"\t",sep='',end='')
        print(getBlankLine(),"\n",sep='',end='')

        print(getTitleLine('jantar'),"\t",sep='',end='')
        print(getTitleLine('jantar'),"\t",sep='',end='')
        print(getTitleLine('jantar'),"\t",sep='',end='')
        print(getTitleLine('jantar'),"\n",sep='',end='')

        print(getMealLine(0,'jantar','pratoPrincipalCarne'),"\t",sep='',end='')
        print(getMealLine(1,'jantar','pratoPrincipalCarne'),"\t",sep='',end='')
        print(getMealLine(2,'jantar','pratoPrincipalCarne'),"\t",sep='',end='')
        print(getMealLine(3,'jantar','pratoPrincipalCarne'),"\n",sep='',end='')

        print(getMealLine(0,'jantar','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print(getMealLine(1,'jantar','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print(getMealLine(2,'jantar','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print(getMealLine(3,'jantar','pratoPrincipalVegetariano'),"\n",sep='',end='')

        print(getMealLine(0,'jantar','arroz'),"\t",sep='',end='')
        print(getMealLine(1,'jantar','arroz'),"\t",sep='',end='')
        print(getMealLine(2,'jantar','arroz'),"\t",sep='',end='')
        print(getMealLine(3,'jantar','arroz'),"\n",sep='',end='')

        print(getMealLine(0,'jantar','feijao'),"\t",sep='',end='')
        print(getMealLine(1,'jantar','feijao'),"\t",sep='',end='')
        print(getMealLine(2,'jantar','feijao'),"\t",sep='',end='')
        print(getMealLine(3,'jantar','feijao'),"\n",sep='',end='')

        print(getMealLine(0,'jantar','guarnicao'),"\t",sep='',end='')
        print(getMealLine(1,'jantar','guarnicao'),"\t",sep='',end='')
        print(getMealLine(2,'jantar','guarnicao'),"\t",sep='',end='')
        print(getMealLine(3,'jantar','guarnicao'),"\n",sep='',end='')

        print(getMealLine(0,'jantar','saladas'),"\t",sep='',end='')
        print(getMealLine(1,'jantar','saladas'),"\t",sep='',end='')
        print(getMealLine(2,'jantar','saladas'),"\t",sep='',end='')
        print(getMealLine(3,'jantar','saladas'),"\n",sep='',end='')

        print(getMealLine(0,'jantar','sobremesa'),"\t",sep='',end='')
        print(getMealLine(1,'jantar','sobremesa'),"\t",sep='',end='')
        print(getMealLine(2,'jantar','sobremesa'),"\t",sep='',end='')
        print(getMealLine(3,'jantar','sobremesa'),"\n",sep='',end='')

        print(getFooter(),"\t",sep='',end='')
        print(getFooter(),"\t",sep='',end='')
        print(getFooter(),"\t",sep='',end='')
        print(getFooter(),"\n",sep='',end='')

        print() #jump 1 line

        print(" " * SND_TAB_SIZE, getHeader(4), " \t", sep='',end='')
        print(getHeader(5), "\t", sep='',end='')
        print(getHeader(6), "\n", sep='',end='')

        print(" " * SND_TAB_SIZE, getTitleLine('almoço')," \t",sep='',end='')
        print(getTitleLine('almoço'),"\t",sep='',end='')
        print(getTitleLine('almoço'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','pratoPrincipalCarne')," \t",sep='',end='')
        print(getMealLine(5,'almoco','pratoPrincipalCarne'),"\t",sep='',end='')
        print(getMealLine(6,'almoco','pratoPrincipalCarne'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','pratoPrincipalVegetariano')," \t",sep='',end='')
        print(getMealLine(5,'almoco','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print(getMealLine(6,'almoco','pratoPrincipalVegetariano'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','arroz')," \t",sep='',end='')
        print(getMealLine(5,'almoco','arroz'),"\t",sep='',end='')
        print(getMealLine(6,'almoco','arroz'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','feijao')," \t",sep='',end='')
        print(getMealLine(5,'almoco','feijao'),"\t",sep='',end='')
        print(getMealLine(6,'almoco','feijao'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','guarnicao')," \t",sep='',end='')
        print(getMealLine(5,'almoco','guarnicao'),"\t",sep='',end='')
        print(getMealLine(6,'almoco','guarnicao'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','saladas')," \t",sep='',end='')
        print(getMealLine(5,'almoco','saladas'),"\t",sep='',end='')
        print(getMealLine(6,'almoco','saladas'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','sobremesa')," \t",sep='',end='')
        print(getMealLine(5,'almoco','sobremesa'),"\t",sep='',end='')
        print(getMealLine(6,'almoco','sobremesa'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getBlankLine()," \t",sep='',end='')
        print(getBlankLine(),"\t",sep='',end='')
        print(getBlankLine(),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getTitleLine('jantar')," \t",sep='',end='')
        print(getTitleLine('jantar'),"\t",sep='',end='')
        print(getTitleLine('jantar'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','pratoPrincipalCarne')," \t",sep='',end='')
        print(getMealLine(5,'jantar','pratoPrincipalCarne'),"\t",sep='',end='')
        print(getMealLine(6,'jantar','pratoPrincipalCarne'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','pratoPrincipalVegetariano')," \t",sep='',end='')
        print(getMealLine(5,'jantar','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print(getMealLine(6,'jantar','pratoPrincipalVegetariano'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','arroz')," \t",sep='',end='')
        print(getMealLine(5,'jantar','arroz'),"\t",sep='',end='')
        print(getMealLine(6,'jantar','arroz'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','feijao')," \t",sep='',end='')
        print(getMealLine(5,'jantar','feijao'),"\t",sep='',end='')
        print(getMealLine(6,'jantar','feijao'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','guarnicao')," \t",sep='',end='')
        print(getMealLine(5,'jantar','guarnicao'),"\t",sep='',end='')
        print(getMealLine(6,'jantar','guarnicao'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','saladas')," \t",sep='',end='')
        print(getMealLine(5,'jantar','saladas'),"\t",sep='',end='')
        print(getMealLine(6,'jantar','saladas'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','sobremesa')," \t",sep='',end='')
        print(getMealLine(5,'jantar','sobremesa'),"\t",sep='',end='')
        print(getMealLine(6,'jantar','sobremesa'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getFooter()," \t",sep='',end='')
        print(getFooter(),"\t",sep='',end='')
        print(getFooter(),"\n",sep='',end='')

    elif r == "1366x768":

        TAB_SIZE = 30

        #first line
        print("\t\t\t\t\t\t\t\tCARDAPIO DA SEMANA")
        print(getHeader(0), "\t", sep='',end='')
        print(getHeader(1), "\t", sep='',end='')
        print(getHeader(2), "\t", sep='',end='')
        print(getHeader(3), "\n", sep='',end='')

        #second line
        print(getTitleLine('almoço'),"\t",sep='',end='')
        print(getTitleLine('almoço'),"\t",sep='',end='')
        print(getTitleLine('almoço'),"\t",sep='',end='')
        print(getTitleLine('almoço'),"\n",sep='',end='')

        #third line
        print(getMealLine(0,'almoco','pratoPrincipalCarne'),"\t",sep='',end='')
        print(getMealLine(1,'almoco','pratoPrincipalCarne'),"\t",sep='',end='')
        print(getMealLine(2,'almoco','pratoPrincipalCarne'),"\t",sep='',end='')
        print(getMealLine(3,'almoco','pratoPrincipalCarne'),"\n",sep='',end='')

        #fourth line
        print(getMealLine(0,'almoco','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print(getMealLine(1,'almoco','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print(getMealLine(2,'almoco','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print(getMealLine(3,'almoco','pratoPrincipalVegetariano'),"\n",sep='',end='')


        #fifth line
        print(getMealLine(0,'almoco','arroz'),"\t",sep='',end='')
        print(getMealLine(1,'almoco','arroz'),"\t",sep='',end='')
        print(getMealLine(2,'almoco','arroz'),"\t",sep='',end='')
        print(getMealLine(3,'almoco','arroz'),"\n",sep='',end='')

        #sixth line
        print(getMealLine(0,'almoco','feijao'),"\t",sep='',end='')
        print(getMealLine(1,'almoco','feijao'),"\t",sep='',end='')
        print(getMealLine(2,'almoco','feijao'),"\t",sep='',end='')
        print(getMealLine(3,'almoco','feijao'),"\n",sep='',end='')

        #seventh line
        print(getMealLine(0,'almoco','guarnicao'),"\t",sep='',end='')
        print(getMealLine(1,'almoco','guarnicao'),"\t",sep='',end='')
        print(getMealLine(2,'almoco','guarnicao'),"\t",sep='',end='')
        print(getMealLine(3,'almoco','guarnicao'),"\n",sep='',end='')

        #eighth line
        print(getMealLine(0,'almoco','saladas'),"\t",sep='',end='')
        print(getMealLine(1,'almoco','saladas'),"\t",sep='',end='')
        print(getMealLine(2,'almoco','saladas'),"\t",sep='',end='')
        print(getMealLine(3,'almoco','saladas'),"\n",sep='',end='')

        #ninth line
        print(getMealLine(0,'almoco','sobremesa'),"\t",sep='',end='')
        print(getMealLine(1,'almoco','sobremesa'),"\t",sep='',end='')
        print(getMealLine(2,'almoco','sobremesa'),"\t",sep='',end='')
        print(getMealLine(3,'almoco','sobremesa'),"\n",sep='',end='')

        #tenth line
        print(getBlankLine(),"\t",sep='',end='')
        print(getBlankLine(),"\t",sep='',end='')
        print(getBlankLine(),"\t",sep='',end='')
        print(getBlankLine(),"\n",sep='',end='')

        #eleventh line
        print(getTitleLine('jantar'),"\t",sep='',end='')
        print(getTitleLine('jantar'),"\t",sep='',end='')
        print(getTitleLine('jantar'),"\t",sep='',end='')
        print(getTitleLine('jantar'),"\n",sep='',end='')

        #twelveth line
        print(getMealLine(0,'jantar','pratoPrincipalCarne'),"\t",sep='',end='')
        print(getMealLine(1,'jantar','pratoPrincipalCarne'),"\t",sep='',end='')
        print(getMealLine(2,'jantar','pratoPrincipalCarne'),"\t",sep='',end='')
        print(getMealLine(3,'jantar','pratoPrincipalCarne'),"\n",sep='',end='')

        #thirteenth line
        print(getMealLine(0,'jantar','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print(getMealLine(1,'jantar','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print(getMealLine(2,'jantar','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print(getMealLine(3,'jantar','pratoPrincipalVegetariano'),"\n",sep='',end='')


        #fourteenth line
        print(getMealLine(0,'jantar','arroz'),"\t",sep='',end='')
        print(getMealLine(1,'jantar','arroz'),"\t",sep='',end='')
        print(getMealLine(2,'jantar','arroz'),"\t",sep='',end='')
        print(getMealLine(3,'jantar','arroz'),"\n",sep='',end='')

        #fifteenth line
        print(getMealLine(0,'jantar','feijao'),"\t",sep='',end='')
        print(getMealLine(1,'jantar','feijao'),"\t",sep='',end='')
        print(getMealLine(2,'jantar','feijao'),"\t",sep='',end='')
        print(getMealLine(3,'jantar','feijao'),"\n",sep='',end='')

        #sixteenth line
        print(getMealLine(0,'jantar','guarnicao'),"\t",sep='',end='')
        print(getMealLine(1,'jantar','guarnicao'),"\t",sep='',end='')
        print(getMealLine(2,'jantar','guarnicao'),"\t",sep='',end='')
        print(getMealLine(3,'jantar','guarnicao'),"\n",sep='',end='')

        #seventeenth line
        print(getMealLine(0,'jantar','saladas'),"\t",sep='',end='')
        print(getMealLine(1,'jantar','saladas'),"\t",sep='',end='')
        print(getMealLine(2,'jantar','saladas'),"\t",sep='',end='')
        print(getMealLine(3,'jantar','saladas'),"\n",sep='',end='')

        #eighteenth line
        print(getMealLine(0,'jantar','sobremesa'),"\t",sep='',end='')
        print(getMealLine(1,'jantar','sobremesa'),"\t",sep='',end='')
        print(getMealLine(2,'jantar','sobremesa'),"\t",sep='',end='')
        print(getMealLine(3,'jantar','sobremesa'),"\n",sep='',end='')

        #nineteenth line
        print(getFooter(),"\t",sep='',end='')
        print(getFooter(),"\t",sep='',end='')
        print(getFooter(),"\t",sep='',end='')
        print(getFooter(),"\n",sep='',end='')

        print() #jump 1 line

        print(" " * SND_TAB_SIZE, getHeader(4), " \t", sep='',end='')
        print(getHeader(5), "\t", sep='',end='')
        print(getHeader(6), "\n", sep='',end='')

        print(" " * SND_TAB_SIZE, getTitleLine('almoço')," \t",sep='',end='')
        print(getTitleLine('almoço'),"\t",sep='',end='')
        print(getTitleLine('almoço'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','pratoPrincipalCarne')," \t",sep='',end='')
        print(getMealLine(5,'almoco','pratoPrincipalCarne'),"\t",sep='',end='')
        print(getMealLine(6,'almoco','pratoPrincipalCarne'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','pratoPrincipalVegetariano')," \t",sep='',end='')
        print(getMealLine(5,'almoco','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print(getMealLine(6,'almoco','pratoPrincipalVegetariano'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','arroz')," \t",sep='',end='')
        print(getMealLine(5,'almoco','arroz'),"\t",sep='',end='')
        print(getMealLine(6,'almoco','arroz'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','feijao')," \t",sep='',end='')
        print(getMealLine(5,'almoco','feijao'),"\t",sep='',end='')
        print(getMealLine(6,'almoco','feijao'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','guarnicao')," \t",sep='',end='')
        print(getMealLine(5,'almoco','guarnicao'),"\t",sep='',end='')
        print(getMealLine(6,'almoco','guarnicao'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','saladas')," \t",sep='',end='')
        print(getMealLine(5,'almoco','saladas'),"\t",sep='',end='')
        print(getMealLine(6,'almoco','saladas'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','sobremesa')," \t",sep='',end='')
        print(getMealLine(5,'almoco','sobremesa'),"\t",sep='',end='')
        print(getMealLine(6,'almoco','sobremesa'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getBlankLine()," \t",sep='',end='')
        print(getBlankLine(),"\t",sep='',end='')
        print(getBlankLine(),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getTitleLine('jantar')," \t",sep='',end='')
        print(getTitleLine('jantar'),"\t",sep='',end='')
        print(getTitleLine('jantar'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','pratoPrincipalCarne')," \t",sep='',end='')
        print(getMealLine(5,'jantar','pratoPrincipalCarne'),"\t",sep='',end='')
        print(getMealLine(6,'jantar','pratoPrincipalCarne'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','pratoPrincipalVegetariano')," \t",sep='',end='')
        print(getMealLine(5,'jantar','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print(getMealLine(6,'jantar','pratoPrincipalVegetariano'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','arroz')," \t",sep='',end='')
        print(getMealLine(5,'jantar','arroz'),"\t",sep='',end='')
        print(getMealLine(6,'jantar','arroz'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','feijao')," \t",sep='',end='')
        print(getMealLine(5,'jantar','feijao'),"\t",sep='',end='')
        print(getMealLine(6,'jantar','feijao'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','guarnicao')," \t",sep='',end='')
        print(getMealLine(5,'jantar','guarnicao'),"\t",sep='',end='')
        print(getMealLine(6,'jantar','guarnicao'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','saladas')," \t",sep='',end='')
        print(getMealLine(5,'jantar','saladas'),"\t",sep='',end='')
        print(getMealLine(6,'jantar','saladas'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','sobremesa')," \t",sep='',end='')
        print(getMealLine(5,'jantar','sobremesa'),"\t",sep='',end='')
        print(getMealLine(6,'jantar','sobremesa'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getFooter()," \t",sep='',end='')
        print(getFooter(),"\t",sep='',end='')
        print(getFooter(),"\n",sep='',end='')
    elif r == "1920x1080":

        TAB_SIZE = 38
        SND_TAB_SIZE = 25

        print("\t\t\t\t\t\t\t\t\t\t     CARDAPIO DA SEMANA")
        print("\t",getHeader(0), "\t", sep='',end='')
        print("\t",getHeader(1), "\t", sep='',end='')
        print("\t",getHeader(2), "\t", sep='',end='')
        print("\t",getHeader(3), "\n", sep='',end='')

        print("\t",getTitleLine('almoço'),"\t",sep='',end='')
        print("\t",getTitleLine('almoço'),"\t",sep='',end='')
        print("\t",getTitleLine('almoço'),"\t",sep='',end='')
        print("\t",getTitleLine('almoço'),"\n",sep='',end='')

        print("\t",getMealLine(0,'almoco','pratoPrincipalCarne'),"\t",sep='',end='')
        print("\t",getMealLine(1,'almoco','pratoPrincipalCarne'),"\t",sep='',end='')
        print("\t",getMealLine(2,'almoco','pratoPrincipalCarne'),"\t",sep='',end='')
        print("\t",getMealLine(3,'almoco','pratoPrincipalCarne'),"\n",sep='',end='')

        print("\t",getMealLine(0,'almoco','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print("\t",getMealLine(1,'almoco','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print("\t",getMealLine(2,'almoco','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print("\t",getMealLine(3,'almoco','pratoPrincipalVegetariano'),"\n",sep='',end='')

        print("\t",getMealLine(0,'almoco','arroz'),"\t",sep='',end='')
        print("\t",getMealLine(1,'almoco','arroz'),"\t",sep='',end='')
        print("\t",getMealLine(2,'almoco','arroz'),"\t",sep='',end='')
        print("\t",getMealLine(3,'almoco','arroz'),"\n",sep='',end='')

        print("\t",getMealLine(0,'almoco','feijao'),"\t",sep='',end='')
        print("\t",getMealLine(1,'almoco','feijao'),"\t",sep='',end='')
        print("\t",getMealLine(2,'almoco','feijao'),"\t",sep='',end='')
        print("\t",getMealLine(3,'almoco','feijao'),"\n",sep='',end='')

        print("\t",getMealLine(0,'almoco','guarnicao'),"\t",sep='',end='')
        print("\t",getMealLine(1,'almoco','guarnicao'),"\t",sep='',end='')
        print("\t",getMealLine(2,'almoco','guarnicao'),"\t",sep='',end='')
        print("\t",getMealLine(3,'almoco','guarnicao'),"\n",sep='',end='')

        print("\t",getMealLine(0,'almoco','saladas'),"\t",sep='',end='')
        print("\t",getMealLine(1,'almoco','saladas'),"\t",sep='',end='')
        print("\t",getMealLine(2,'almoco','saladas'),"\t",sep='',end='')
        print("\t",getMealLine(3,'almoco','saladas'),"\n",sep='',end='')

        print("\t",getMealLine(0,'almoco','sobremesa'),"\t",sep='',end='')
        print("\t",getMealLine(1,'almoco','sobremesa'),"\t",sep='',end='')
        print("\t",getMealLine(2,'almoco','sobremesa'),"\t",sep='',end='')
        print("\t",getMealLine(3,'almoco','sobremesa'),"\n",sep='',end='')

        print("\t",getBlankLine(),"\t",sep='',end='')
        print("\t",getBlankLine(),"\t",sep='',end='')
        print("\t",getBlankLine(),"\t",sep='',end='')
        print("\t",getBlankLine(),"\n",sep='',end='')

        print("\t",getTitleLine('jantar'),"\t",sep='',end='')
        print("\t",getTitleLine('jantar'),"\t",sep='',end='')
        print("\t",getTitleLine('jantar'),"\t",sep='',end='')
        print("\t",getTitleLine('jantar'),"\n",sep='',end='')

        print("\t",getMealLine(0,'jantar','pratoPrincipalCarne'),"\t",sep='',end='')
        print("\t",getMealLine(1,'jantar','pratoPrincipalCarne'),"\t",sep='',end='')
        print("\t",getMealLine(2,'jantar','pratoPrincipalCarne'),"\t",sep='',end='')
        print("\t",getMealLine(3,'jantar','pratoPrincipalCarne'),"\n",sep='',end='')

        print("\t",getMealLine(0,'jantar','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print("\t",getMealLine(1,'jantar','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print("\t",getMealLine(2,'jantar','pratoPrincipalVegetariano'),"\t",sep='',end='')
        print("\t",getMealLine(3,'jantar','pratoPrincipalVegetariano'),"\n",sep='',end='')

        print("\t",getMealLine(0,'jantar','arroz'),"\t",sep='',end='')
        print("\t",getMealLine(1,'jantar','arroz'),"\t",sep='',end='')
        print("\t",getMealLine(2,'jantar','arroz'),"\t",sep='',end='')
        print("\t",getMealLine(3,'jantar','arroz'),"\n",sep='',end='')

        print("\t",getMealLine(0,'jantar','feijao'),"\t",sep='',end='')
        print("\t",getMealLine(1,'jantar','feijao'),"\t",sep='',end='')
        print("\t",getMealLine(2,'jantar','feijao'),"\t",sep='',end='')
        print("\t",getMealLine(3,'jantar','feijao'),"\n",sep='',end='')

        print("\t",getMealLine(0,'jantar','guarnicao'),"\t",sep='',end='')
        print("\t",getMealLine(1,'jantar','guarnicao'),"\t",sep='',end='')
        print("\t",getMealLine(2,'jantar','guarnicao'),"\t",sep='',end='')
        print("\t",getMealLine(3,'jantar','guarnicao'),"\n",sep='',end='')

        print("\t",getMealLine(0,'jantar','saladas'),"\t",sep='',end='')
        print("\t",getMealLine(1,'jantar','saladas'),"\t",sep='',end='')
        print("\t",getMealLine(2,'jantar','saladas'),"\t",sep='',end='')
        print("\t",getMealLine(3,'jantar','saladas'),"\n",sep='',end='')

        print("\t",getMealLine(0,'jantar','sobremesa'),"\t",sep='',end='')
        print("\t",getMealLine(1,'jantar','sobremesa'),"\t",sep='',end='')
        print("\t",getMealLine(2,'jantar','sobremesa'),"\t",sep='',end='')
        print("\t",getMealLine(3,'jantar','sobremesa'),"\n",sep='',end='')

        print("\t",getFooter(),"\t",sep='',end='')
        print("\t",getFooter(),"\t",sep='',end='')
        print("\t",getFooter(),"\t",sep='',end='')
        print("\t",getFooter(),"\n",sep='',end='')

        print() #jump 1 line

        print(" " * SND_TAB_SIZE, getHeader(4), " \t", sep='',end='')
        print(getHeader(5), "  \t", sep='',end='')
        print(getHeader(6), "\n", sep='',end='')

        print(" " * SND_TAB_SIZE, getTitleLine('almoço')," \t",sep='',end='')
        print(getTitleLine('almoço'),"  \t",sep='',end='')
        print(getTitleLine('almoço'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','pratoPrincipalCarne')," \t",sep='',end='')
        print(getMealLine(5,'almoco','pratoPrincipalCarne'),"  \t",sep='',end='')
        print(getMealLine(6,'almoco','pratoPrincipalCarne'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','pratoPrincipalVegetariano')," \t",sep='',end='')
        print(getMealLine(5,'almoco','pratoPrincipalVegetariano'),"  \t",sep='',end='')
        print(getMealLine(6,'almoco','pratoPrincipalVegetariano'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','arroz')," \t",sep='',end='')
        print(getMealLine(5,'almoco','arroz'),"  \t",sep='',end='')
        print(getMealLine(6,'almoco','arroz'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','feijao')," \t",sep='',end='')
        print(getMealLine(5,'almoco','feijao'),"  \t",sep='',end='')
        print(getMealLine(6,'almoco','feijao'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','guarnicao')," \t",sep='',end='')
        print(getMealLine(5,'almoco','guarnicao'),"  \t",sep='',end='')
        print(getMealLine(6,'almoco','guarnicao'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','saladas')," \t",sep='',end='')
        print(getMealLine(5,'almoco','saladas'),"  \t",sep='',end='')
        print(getMealLine(6,'almoco','saladas'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'almoco','sobremesa')," \t",sep='',end='')
        print(getMealLine(5,'almoco','sobremesa'),"  \t",sep='',end='')
        print(getMealLine(6,'almoco','sobremesa'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getBlankLine()," \t",sep='',end='')
        print(getBlankLine(),"  \t",sep='',end='')
        print(getBlankLine(),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getTitleLine('jantar')," \t",sep='',end='')
        print(getTitleLine('jantar'),"  \t",sep='',end='')
        print(getTitleLine('jantar'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','pratoPrincipalCarne')," \t",sep='',end='')
        print(getMealLine(5,'jantar','pratoPrincipalCarne'),"  \t",sep='',end='')
        print(getMealLine(6,'jantar','pratoPrincipalCarne'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','pratoPrincipalVegetariano')," \t",sep='',end='')
        print(getMealLine(5,'jantar','pratoPrincipalVegetariano'),"  \t",sep='',end='')
        print(getMealLine(6,'jantar','pratoPrincipalVegetariano'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','arroz')," \t",sep='',end='')
        print(getMealLine(5,'jantar','arroz'),"  \t",sep='',end='')
        print(getMealLine(6,'jantar','arroz'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','feijao')," \t",sep='',end='')
        print(getMealLine(5,'jantar','feijao'),"  \t",sep='',end='')
        print(getMealLine(6,'jantar','feijao'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','guarnicao')," \t",sep='',end='')
        print(getMealLine(5,'jantar','guarnicao'),"  \t",sep='',end='')
        print(getMealLine(6,'jantar','guarnicao'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','saladas')," \t",sep='',end='')
        print(getMealLine(5,'jantar','saladas'),"  \t",sep='',end='')
        print(getMealLine(6,'jantar','saladas'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getMealLine(4,'jantar','sobremesa')," \t",sep='',end='')
        print(getMealLine(5,'jantar','sobremesa'),"  \t",sep='',end='')
        print(getMealLine(6,'jantar','sobremesa'),"\n",sep='',end='')

        print(" " * SND_TAB_SIZE, getFooter()," \t",sep='',end='')
        print(getFooter(),"  \t",sep='',end='')
        print(getFooter(),"\n",sep='',end='')


###################################################################################################

if __name__ == "__main__":
    main()
