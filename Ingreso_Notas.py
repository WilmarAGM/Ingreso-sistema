# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 12:42:25 2022

@author: willi
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
import time 
import math 
import pandas as pd
import numpy as np

# Opciones de navegación

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
options.add_argument('--disable-blink-features=AutomationControlled')

driver_path = r'C:\Users\willi\OneDrive\Documentos\Ingreso sistema\chrome_proxy.exe'
driver = webdriver.Chrome(options)

#Inicializarla en la pantalla
driver.set_window_position(2000, 0)
driver.maximize_window()
time.sleep(1)

arch = open(r'C:\Users\willi\OneDrive\Documentos\Inf\inf.txt', 'r')
L_a = []
for lines in arch:
    L_a.append(lines.strip())
user_w, pas_w = L_a

G =['G16','G17','G23'] #Grupos a calificar en el orden que aparece la tabla de grupos en el sia
Op = [1, 2, 3, 4]
E = ['P1','P2','P3','Q']


for i in range(3): #número de grupos 
    driver.get('https://autenticasia.unal.edu.co/oam/server/obrareq.cgi?encquery%3DQRxSGb8fdZA71BpVn7yvNiPQef2M%2FS9R9fwRkE2SFW3avyZ%2BP%2BToJSZmBmdxf%2Btz2FMJUL3nVlyXdbVTryUjb4vwYI8HJoRal79NXiGjWr3lJ7n5bGb27ALdIiS7cT8vLQD434NO3hbfTzLg6s4jedm7l8%2F8Oysihf1lKIswaR5RPvNMrJd4xpNIPNiO3%2FUsiY9Tl2jQ48cB7OHkrdFemMGdaN7drr%2Fg4Wqbl6%2B57qHEHgLobhsZxDJ5bh32HIJm7R%2FBI3S3%2FI8FQgYsuihpgVW9VGilqVFs9EDov0RnNQg%3D%20agentid%3DWT_UNAL_PROD%20ver%3D1%20crmethod%3D2%26cksum%3De124b5149df23168f74dfdd0c739b089e8e56669&ECID-Context=1.0068t7huy8X6YNuMwa3j6G00AhK%5E00Lamy%3BkXjE')
    usuario = driver.find_element(By.ID, "username")
    usuario.send_keys(user_w)
    time.sleep(2)
    usuario.send_keys(Keys.ENTER)
    
    clave = driver.find_element(By.ID,"password")
    clave.send_keys(pas_w)
    time.sleep(2)
    clave.send_keys(Keys.ENTER)
    time.sleep(3)
    
    driver.find_element(By.XPATH, "//span[text()='Rol de docente']").click()
    time.sleep(3)
    
    driver.find_element(By.XPATH, "//a[text()='Calificaciones']").click()
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(3)
    
    aux = driver.find_element(By.XPATH,'//a[@class="vMenuPrincipal"]')
    aux2= aux.get_attribute('href')
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[2])
    driver.get(aux2)
    time.sleep(3)
    #A = driver.find_elements_by_xpath("//a[@class='vActas']")
    A = driver.find_element(By.XPATH, "/html/body/form/table/tbody/tr[{}]/td[2]/a".format(i+2))
    A.click()
    for o in range(len(Op)):
        driver.find_element(By.XPATH, "/html/body/form[2]/table[1]/tbody/tr/td[1]/select/option[{}]".format(Op[o])).click()
        # Archivo con las notas
        ruta1 = r'C:\Users\willi\OneDrive\Documentos\Cálculo diferencial\Semestre 2s 2024\{}\Reporte_notas_{}.xlsx'.format(G[i],G[i])
        ruta2 = r'C:\Users\willi\OneDrive\Documentos\Cálculo diferencial\Semestre 2s 2024\{}\L{}.xls'.format(G[i],G[i])
        df1 = pd.read_excel(ruta1)
        df2 = pd.read_excel(ruta2)
        df1 = df1.set_index('CORREO')
        df1[E[o]] = df1[E[o]].apply(lambda x: math.floor(10*x+0.5)/10)
        df2 = df2.set_index('CORREO')     
        df = df2.join(df1[E[o]]).fillna(0)
        niter = math.ceil(len(df)/25)
        driver.find_element(By.XPATH, "/html/body/form[2]/table[1]/tbody/tr/td[1]/select/option[{}]".format(Op[o])).click()
        c=0
        for j in range(niter):
            for k in range(25):
                aux=df.iloc[c,2]
                driver.find_element(By.XPATH, "/html/body/form[3]/table[2]/tbody/tr[{}]/td[5]/input".format(k+2)).send_keys(str(aux))
                if (c+1 == len(df)):
                    break
                c+=1
            driver.find_element(By.XPATH, "/html/body/form[3]/table[3]/tbody/tr/td[3]/input").click()
            time.sleep(2)
            if j == 0:
                driver.find_element(By.XPATH, "/html/body/form[3]/table[3]/tbody/tr/td[4]/a").click()
            elif j< (niter-1):
                driver.find_element(By.XPATH, "/html/body/form[3]/table[3]/tbody/tr/td[4]/a[2]").click()
            else:
                break
        time.sleep(3)

    driver.find_element(By.XPATH, "/html/body/table[1]/tbody/tr[2]/td[3]/a[2]").click()
    driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td[3]/a[2]").click()
    time.sleep(20)
    




