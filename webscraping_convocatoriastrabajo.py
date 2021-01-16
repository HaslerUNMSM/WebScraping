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
            empresa = infoEmpresa[0]
            print(empresa.get_text())
            if empresa != None:
                oferta["empresa"] = empresa.get_text()
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
            # print(aviso_deta)

            # print("-------------------------------------------------------------------")
            print("-------------------------OFERTA HASTA AHORA------------------------")
            print(oferta)
            lista_oferta.append(oferta)
            print("-------------------------------------------------------------------")
            # print("-------------------------------------------------------------------")
            id_Oferta = controller.registrar_oferta(con, oferta)
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

    return lista_oferta


def scraping_ofertadetalle(url_pagina, link, id_carga):
    oferta = {}
    # Almacena la url de la pagina
    oferta["url_pagina"] = url_pagina
    # Almacena la url de la oferta
    oferta["url"] = link
    # Accede al contenido HTML de la cabecera de la oferta
    reqCab = requests.get(oferta["url_pagina"])
    soup_cab = BeautifulSoup(reqCab.text, "lxml")
    oferta["puesto"] = soup_cab.find(
        "div", {"class": "jobsearch-SerpJobCard"}).find("h2", {"class": "title"}).get_text()
    empresa = soup_cab.find(
        "div", {"class": "jobsearch-SerpJobCard"}).find_all("span", {"class": "company"})
    print(len(empresa))
    oferta["empresa"] = empresa[0].get_text()

    oferta["lugar"] = soup_cab.find("div", {"class": "jobsearch-SerpJobCard"}).find(
        "span", {"class": "location accessible-contrast-color-location"})
    oferta["salario"] = soup_cab.find(
        "div", {"class": "jobsearch-SerpJobCard"}).find("span", {"class": "salaryText"})

    #title=bsObj.find_all("div", {"class": "summary"})

    # Accede al contenido HTML del detalle de la oferta
    reqDeta = requests.get(oferta["url"])
    # print(oferta["url"])
    soup_deta = BeautifulSoup(reqDeta.text, "lxml")
    # Obtiene el nombre del puesto de trabajo
    #oferta["puesto"] = soup_deta.find("div", {"id": "vjs-jobtitle"})
    # Obtiene el nombre de la empresa
    #oferta["empresa"] = soup_deta.find("span", {"id": "vjs-cn"})
    #oferta["lugar"] = soup_deta.find("span", {"id": "vjs-loc"})
    #oferta["salario"] = soup_deta.find("div", {})
    # Obtiene los div z-group en el cual esta contenido los datos resumen de la oferta, tales como:
    # Lugar, Tiempo de Publicacion, Salario, Tipo de Puesto, Area
    #aviso_deta = soup_deta.find("div", {"id": "vjs-desc"})
    #aviso_deta1= aviso_deta
    # for ed in aviso_deta:
    # Obtiene el titulo del dato resumen
    #cabecera_deta = ed.find("div", {"class": "spec_attr"})
    # Obtiene el contenido del dato resumen
    #children_descripcion_deta = ed.find("div", {"class": "spec_def"}).findChildren()
    #descripcion_deta = children_descripcion_deta[len(children_descripcion_deta) - 1].text.strip()
    # if cabecera_deta.find("h2", {"class": "lugar"}) is not None:
    #    oferta["lugar"] = descripcion_deta
    # elif cabecera_deta.find("h2", {"class": "fecha"}) is not None:
    #    oferta["tiempoPublicado"] = descripcion_deta
    # elif cabecera_deta.find("h2", {"class": "salario"}) is not None:
    #    oferta["salario"] = descripcion_deta
    # elif cabecera_deta.find("h2", {"class": "tipo_puesto"}) is not None:
    #    oferta["tipoPuesto"] = descripcion_deta
    # elif cabecera_deta.find("h2", {"class": "area"}) is not None:
    #    oferta["area"] = descripcion_deta
    #oferta["prop_area"] = soup_deta.find('input', {'id': 'area'}).get("value")
    #oferta["prop_subarea"] = soup_deta.find('input', {'id': 'subarea'}).get("value")
    # Obtiene la descripcion de la Oferta(Requisitos)
    # Almacena lo contenido en etiquetas <p> y <li>
    # Extrae informacion de etiquetas <p>
    #aviso_descripcion = soup_deta.find("div", {"class": "aviso_description"})
    #descripcion_deta_p = aviso_descripcion.find_all("p")
    #lista_detalle = []
    # for ed in descripcion_deta_p:
    #    content = ed.contents
    #    if content is not None and contain_br(content):
    #        lista_detalle.extend(get_content(content))
    #    else:
    #        if ed.text is not None and ed.text.strip() != "":
    #            lista_detalle.append(ed.text)

    # Extrae informacion de etiquetas <li>
    #descripcion_deta_ul = aviso_descripcion.find_all("ul")
    # for ed in descripcion_deta_ul:
    #    descripcion_deta_ul_li = ed.find_all("li")
    #    for edc in descripcion_deta_ul_li:
    #        children = edc.findChildren()
    #        descripcion = {}
    #        if len(children) > 0:
    #            text = children[len(children) - 1].text.strip()
    #            descripcion["descripcion"] = text
    #            if text is not None and text.strip() != "":
    #                lista_detalle.append(text)
    #       else:
    #            text = edc.text
    #            descripcion["descripcion"] = text
    #            if text is not None and text.strip() != "":
    #                lista_detalle.append(text)
    # lista_detalle.append(aviso_deta.get_text())
    # lista_detalle=aviso_deta.get_text()
    #oferta["listaDescripcion"] = replace_quote(lista_detalle)
    #oferta["listaDescripcion"] = aviso_deta1
    oferta["id_carga"] = id_carga

    print(oferta)
    return oferta


def replace_quote(list):
    new_list = []
    for el in list:
        el = el.replace("'", "''")
        new_list.append(el)
    return new_list
