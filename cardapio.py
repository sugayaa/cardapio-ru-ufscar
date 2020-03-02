import os
from html.parser import HTMLParser
from dateutil.parser import parse
import subprocess
import sys

###### GLOBAL VARIABLES ######################

_T_TABSIZE = 9
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
def buildLine(no_meals, line_no):
    line = ""
    if line_no > 9:
        ref = "jantar"
    else:
        ref = "almoço"

    for i in range(no_meals):
        if line_no % 9 == 0:
            idx = line_no // 9
            if idx == 0:
                line += getHeader(i)
            elif idx == 1:
                line += getBlankLine()
            elif idx == 2:
                line += getFooter()
        if line_no % 9 == 1:
            line += getTitleLine(ref)
        if line_no % 9 == 2:
            line += getMealLine(i, ref,'pratoPrincipalCarne')
        if line_no % 9 == 3:
            line += getMealLine(i, ref,'pratoPrincipalVegetariano')
        if line_no % 9 == 4:
            line += getMealLine(i, ref,'arroz')
        if line_no % 9 == 5:
            line += getMealLine(i, ref,'feijao')
        if line_no % 9 == 6:
            line += getMealLine(i, ref,'guarnicao')
        if line_no % 9 == 7:
            line += getMealLine(i, ref,'saladas')
        if line_no % 9 == 8:
            line += getMealLine(i, ref,'sobremesa')

        if i == no_meals - 1:
            line += "\n"
            if line_no == 18:
                line += "\n"
        else:
            line += " "
    return line

def getRes():
    x_output = subprocess.check_output(["xrandr"])
    res_ant = ""
    for it in x_output.split():
        curr_it = str(it)
        if "*" in curr_it:
            return res_ant
        res_ant = it

def getTerRes():
    h, w = map(int, subprocess.check_output(["stty", "size"]).split())
    return h, w

def getDisp(h, w):
    if w < 38:
        print("Are you kidding me?")
        print("Enlarge your terminal")
        sys.exit(1)
    else:
        meal_space = 38
        no_meals = 0
        while w >= meal_space:
            w -= meal_space
            no_meals += 1
            if meal_space == 38:
                meal_space += 1

        return no_meals


def getDataEDia(index):
    global semana
    dataEDia = ""

    dataEDia += printDate(getattr(semana[index], 'data'))
    dataEDia += " - "
    dataEDia += getattr(semana[index], 'diaDaSemana')
    dataEDia += " "

    return dataEDia

def getMenuHeader(w):
    if w >= 18:
        center = w // 2
        center -= 9
        no_tabs = 0
        while center > 9:
            center -= 9
            no_tabs += 1

        return printTabs(no_tabs) + printAlignment(center) + "CARDAPIO DA SEMANA"
    else:
        return ""

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
    if meal == "almoço":
        meal = "almoco"
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

def newGetBlankLine():
    return "*"+ ""

def getTitleLine(title):
    titleline = "* >>>"
    titleline += title.capitalize()
    titleline += " " * (TAB_SIZE - 12)
    titleline += "*"
    return titleline

def printTabs(no):
    return '\t' * no

def printAlignment(leftover):
    spaces = 0
    while leftover >= 2:
        leftover -= 2
        spaces += 1

    return " " * spaces

def printDate(date):
    return '{}/{}/{}'.format(date.day, date.month, date.year)


def main():
    #html downloader and updater
    os.system("./download.sh")
    global TAB_SIZE
    global SND_TAB_SIZE


    f = open("ru.html", "r")
    html = f.read()
    parser = HTMLParser()
    parser.feed(html)
    f.close()

    #for dia in semana:
    #    dia.imprime()


    r = getRes().decode("utf-8")
    h, w = getTerRes()
    no_meals_per_line = getDisp(h, w)
    meals_left = 7

    print(getMenuHeader(w))

    while meals_left > 0:
        if meals_left < no_meals_per_line:
            no_meals_per_line = meals_left

        for i in range(19):
            print(buildLine(no_meals_per_line, i),end='')

        meals_left -= no_meals_per_line

###################################################################################################

if __name__ == "__main__":
    main()
