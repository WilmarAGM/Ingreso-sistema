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

# Opciones de navegación

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
options.add_argument('--disable-blink-features=AutomationControlled')

driver_path = r'C:\Users\willi\Downloads\chromedriver.exe'
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

G =['15','21'] #Grupos a calificar en el orden que aparece la tabla de grupos en el sia
Op = [1, 2, 3, 4, 5, 6, 7, 8, 9]
E = ['Q1C','Q2C','Q3C','Q4C','Q5C','A1','A2','P1','P2']


for i in range(2): #número de grupos 
    driver.get('https://autenticasia.unal.edu.co/oam/server/obrareq.cgi?encquery%3DYaooNeilR8gyk4gcly0IOXvfQzq4SxRkDVTjscgL7yQRm4htARkuSu02ZWibFx%2B2W%2BPzsXBxZiMW%2BvmyII%2BLQXyawnSEdILwX3ySU7ykAAfnwmj8HyQZ5LW6RxM634HnfmLtuycuT4u07bjgOV%2Fj3wWosv%2FUV0Eu7eYG953QKPcdfbg0PSF%2FVJ0BZBcGTqVlEJ5OYCgAbXLwAGJ%2FTGqjiBYDyMNtVdrK8FZ0E1kooJeBRmGgOYB0KUNPh2guXziwbjdEm9I0oylUDJTNo2ZWjRrx0dCVnWyT%2BfRI8dDGhVw%3D%20agentid%3DWTUNC_AWS%20ver%3D1%20crmethod%3D2&ECID-Context=1.005vPyeCJdz6MQRMyYbe6G0000Eg0008_b%3BkXjE')

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
        ruta1 = r'C:\Users\willi\OneDrive\Documentos\Cálculo diferencial\Semestre 1s 2023\G{}\QG{}.xlsx'.format(G[i],G[i]) #Ruta archivo de notas 
        # Lista actualizada 
        ruta2 = r'C:\Users\willi\OneDrive\Documentos\Cálculo diferencial\Semestre 1s 2023\G{}\LG{}.xls'.format(G[i], G[i]) #Ruta lista actualizada del sia
        df1 = pd.read_excel(ruta1)
        df2 = pd.read_excel(ruta2)
        df1 = df1.set_index('CORREO')
        df1[E[o]] = df1[E[o]].apply(lambda x: math.floor(10*x+0.5)/10)
        df2 = df2.set_index('CORREO')     
        df = df2.join(df1[E[o]]).fillna(0)
        #df.to_excel(r'C:\Users\willi\OneDrive\Documentos\Cálculo diferencial\Semestre 1s 2023\G{}\QG{}.xlsx'.format(G[i]))
        niter = math.ceil(len(df)/25)
        driver.find_element(By.XPATH, "/html/body/form[2]/table[1]/tbody/tr/td[1]/select/option[{}]".format(Op[o])).click()
        c=0
        for j in range(niter):
            for k in range(25):
                aux=df.iloc[c,1]
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
    




