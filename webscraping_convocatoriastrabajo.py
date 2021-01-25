from urllib.request import urlopen
from urllib.error import HTTPError
import bs4
from bs4 import BeautifulSoup
import requests
from controller import Controller
from configuration import CONVOCATORIATRABAJO


def contain_br(contents):
    for element in contents:
        if type(element) is bs4.element.Tag:
            if element.name == "br":
                return True
    return False


def get_content(contents):
    lista = []
    for element in contents:
        if type(element) is bs4.element.NavigableString:
            if str(element) is not None and str(element).strip() != "":
                lista.append(str(element))
    return lista


def encontrar_id_unico(cadena):
    i = 0
    indice = -1
    while i < len(cadena):
        if cadena[i] == "-":
            indice = i
        i = i+1
    auxiliar = cadena[indice+1:len(cadena)-5]
    return auxiliar


def scraping_ofertas(con, url_principal, prefix_url, sufix_url, pagina_inicial, cant_paginas, cant_ofertas, id_carga):
    controller = Controller()
    lista_oferta = []
    i = 1

    for i in range(CONVOCATORIATRABAJO["WS_PAGINA_INICIAL"], CONVOCATORIATRABAJO["WS_PAGINAS"]):

        # Recuperar el link de la pagina
        url_pagina = prefix_url

        # Acceder al link principal
        req = requests.get(url_pagina)
        soup = BeautifulSoup(req.text, "lxml")

        # Limitar el web scraping al area del codigo html pertinente
        avisos = soup.findAll("section")[0].find(
            "div", {"class": "info-convocatoria"}).findAll("article", {"class": "puesto"})

        # Listar las ofertas y buscar en cada una
        lista_oferta = []
        for el in avisos:

            oferta = {}

            # Obtiene el link para poder ver el detalle de la oferta
            href = el.find("h3").find("a")['href']
            link = url_principal + "/" + href

            # Se obtiene el identificador unico
            id_unico = encontrar_id_unico(href)
            print("El identificador unico de esta oferta es: " + id_unico)
            oferta["id_anuncioempleo"] = id_unico

            # Almacena el id de carga
            oferta["id_carga"] = id_carga

            # Almacena la url de la pagina
            oferta["url_pagina"] = url_pagina

            # Almacena la url de la oferta
            oferta["url"] = link

            redundancia = controller.evitar_redundancia(con, oferta)

            if(redundancia is None):
                print("Registro nuevo")

                # Almacena el puesto de la oferta
                oferta["puesto"] = el.find("h3").find("a").get_text()

                infoEmpresa = el.find({"div": "puesto-cont"}
                                      ).find({"div": "puesto-det"}).find_all("p")

                # Almacena el nombre de la empresa de la oferta
                if infoEmpresa[0] != None:
                    oferta["empresa"] = infoEmpresa[0].get_text()
                else:
                    oferta["empresa"] = ''

                lugar = infoEmpresa[1].get_text()
                lugarK = lugar.split("   ")

                # Almacena el lugar de la oferta
                if lugarK != None:
                    oferta["lugar"] = lugarK[0]
                else:
                    oferta["lugar"] = ''

                salario = lugarK[1]
                if salario != None:
                    oferta["salario"] = salario
                else:
                    oferta["salario"] = ''

                # Accede al contenido HTML del detalle de la oferta
                reqDeta = requests.get(oferta["url"])
                soup_deta = BeautifulSoup(reqDeta.text, "lxml")

                # LIMITAMOS EL SCRAPING SOLO AL CONTENIDO QUE SE DESEA
                aviso_deta = soup_deta.find({"article", "oferta"}).get_text()

                if aviso_deta != None:
                    oferta["detalle"] = aviso_deta
                # print("-----  IMPRIMIENTO AVISO_DETA------")
                # print(aviso_deta)

                # print("-------------------------------------------------------------------")
                # print("-------------------------OFERTA HASTA AHORA------------------------")
                # print(oferta)

                # Se agrega la oferta a la lista de ofertas
                lista_oferta.append(oferta)

                # print("-------------------------------------------------------------------")
                # Se registra la oferta en la base de datos.
                id_Oferta = controller.registrar_oferta(con, oferta)
                print("\nid de la oferta: ", id_Oferta)

                # print("-------------------------------------------------------------------")
                # Se guarda linea por linea la informacion de la oferta
                arreglo = str(aviso_deta).splitlines()

                # Se limpia la informacion obtenida
                # print("---------------------DESPUES DE TRATAR------------------------------")
                for k in arreglo:
                    if arreglo.count(k) > 1:
                        arreglo.pop(arreglo.index(k))
                arreglo.remove('')
                tamanio = len(arreglo)
                k = 0
                while k <= 6:
                    tamanio = len(arreglo)
                    arreglo.pop(tamanio-1)
                    k = k+1
                # print(arreglo)

                tuplas = []
                for elemento in arreglo:
                    detalle = {}
                    detalle["id_oferta"] = id_Oferta
                    detalle["descripcion"] = elemento
                    tuplas.append(detalle)

                controller.registrar_detalle_oferta(con, tuplas)

            else:
                print("Registro redundante")

    return lista_oferta


def replace_quote(list):
    new_list = []
    for el in list:
        el = el.replace("'", "''")
        new_list.append(el)
    return new_list
