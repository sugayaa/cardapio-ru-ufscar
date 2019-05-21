from html.parser import HTMLParser
from dateutil.parser import parse

leiaCardapio = False
dias = 0
conjDias = []
qualRef = 0
whereAmI = 0

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

class diaDaSemana():
    'classe referente a um dia no ru'
    data = ""
    diaDaSemana = ""
    almoco = refeicao()
    jantar = refeicao()

    def imprime(self):
        print("%d/%d/%d" % (self.data.day, self.data.month, self.data.year))

semana = []
for dia in range(7):
    semana.append(diaDaSemana())

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if(len(attrs) != 0):
                if attrs[0][0] == 'id' and attrs[0][1] =='cardapio':
                #for i in attrs:
                #    print(i)
                    print(attrs)
                    print("Encountered div tag :", tag)
                    global leiaCardapio
                    leiaCardapio = True


   # def handle_endtag(self, tag):
   #     print("Encountered and end tag :", tag)

   # def handle_data(self, data):
   #     print("Encountered some data :", data)
    def handle_data(self, data):
        global leiaCardapio
        global dias
        global conjDias
        global qualRef
        if(data == "Acompanhe as notícias da UFSCar também pelas redes sociais oficiais da Universidade "):
            leiaCardapio = False
        if(leiaCardapio):
            tam = data.split()
            if len(tam) > 0:
                print("Encontrei alguns dados:", data)
                try :
                    d = parse(data, dayfirst=True)
                    print("%d/%d/%d" % (d.day, d.month, d.year))
                    if d not in conjDias:
                        setattr(semana[dias], 'data', d)
                        conjDias.append(d)
                        qualRef = 0
                    else:
                        dias += 1
                        qualRef = 1
                except:
                    #if whereAmI == 0:
                    #if whereAmI == 1:


                    print("",end='')



f = open("ru.html", "r")
myhtml = f.read()
#print(myhtml)
parser = MyHTMLParser()
parser.feed(myhtml)
f.close()

print("MYDEBUG:")

print(semana)
print("ENDMYDEBUG")

for dia in semana:
    dia.imprime()
