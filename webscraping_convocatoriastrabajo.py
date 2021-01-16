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


def scraping_ofertas(con, url_principal, prefix_url, sufix_url, pagina_inicial, cant_paginas, cant_ofertas, id_carga):
    controller = Controller()
    lista_oferta = []
    i = 1
    # for i in range(pagina_inicial, cant_paginas):
    for i in range(CONVOCATORIATRABAJO["WS_PAGINA_INICIAL"], CONVOCATORIATRABAJO["WS_PAGINAS"]):

        # MODIFICADO-----------------------------
        url_pagina = prefix_url
        #print("------------------for i in range(pagina_inicial, cant_paginas)-------------------")
        # print(i)

        req = requests.get(url_pagina)
        soup = BeautifulSoup(req.text, "lxml")

        avisos = soup.findAll("section")[0].find(
            "div", {"class": "info-convocatoria"}).findAll("article", {"class": "puesto"})

        lista_oferta = []
        for el in avisos:

            # el=el.find("article","puesto")

            # print("-------avisos--------")
            # print(len(avisos))
            oferta = {}
            #cont = cont + 1
            # if cant_ofertas is not None:
            #    if cont > cant_ofertas:
            #        break
            # Obtiene el link para poder ver el detalle de la oferta
            href = el.find("h3").find("a")['href']
            link = url_principal + "/" + href
            # print(link)
            oferta["id_carga"] = id_carga
            # Almacena la url de la pagina
            oferta["url_pagina"] = url_pagina
            # Almacena la url de la oferta
            oferta["url"] = link

            # MODIFICADO

            oferta["puesto"] = el.find("h3").find("a").get_text()
            #print("Puesto " + oferta["puesto"])

            infoEmpresa = el.find({"div": "puesto-cont"}
                                  ).find({"div": "puesto-det"}).find_all("p")
            #empresa = infoEmpresa[0]
            # print(empresa.get_text())
            if infoEmpresa[0] != None:
                oferta["empresa"] = infoEmpresa[0].get_text()
            else:
                oferta["empresa"] = ''

            lugar = infoEmpresa[1].get_text()
            lugarK = lugar.split("   ")

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
            print("-----  IMPRIMIENTO AVISO_DETA------")
            print(aviso_deta)

            # print("-------------------------------------------------------------------")
            print("-------------------------OFERTA HASTA AHORA------------------------")
            print(oferta)
            lista_oferta.append(oferta)
            print("-------------------------------------------------------------------")
            # print("-------------------------------------------------------------------")
            id_Oferta = controller.registrar_oferta(con, oferta)
            print("id de la oferta: ", id_Oferta)
            aviso_deta_aux = aviso_deta
            # print(aviso_deta)
            # print("-------------------------------------------------------------------")
            # print("-------------------------------------------------------------------")
            arreglo = str(aviso_deta).splitlines()
            #print("----------------------ANTES DE TRATAR-------------------------------")
            # print(arreglo)
            print("---------------------DESPUES DE TRATAR------------------------------")
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
            print(arreglo)

            tuplas = []
            for elemento in arreglo:
                detalle = {}
                detalle["id_oferta"] = id_Oferta
                detalle["descripcion"] = elemento
                tuplas.append(detalle)

            controller.registrar_detalle_oferta(con, tuplas)

    return lista_oferta


def replace_quote(list):
    new_list = []
    for el in list:
        el = el.replace("'", "''")
        new_list.append(el)
    return new_list
