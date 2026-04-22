# -*- coding: utf-8 -*-
import os
import shutil
import time
import math
import logging
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    NoAlertPresentException,
    WebDriverException,
)

logger = logging.getLogger(__name__)


def _find_chrome_binary():
    """Detecta el binario de Chrome/Chromium en Linux y macOS."""
    candidates = [
        # Linux — rutas comunes
        '/usr/bin/google-chrome',
        '/usr/bin/google-chrome-stable',
        '/usr/bin/chromium-browser',
        '/usr/bin/chromium',
        '/snap/bin/chromium',
        '/usr/local/bin/chromium',
        # macOS
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '/Applications/Chromium.app/Contents/MacOS/Chromium',
    ]
    # Buscar también en PATH
    for name in ('google-chrome', 'google-chrome-stable', 'chromium-browser', 'chromium'):
        found = shutil.which(name)
        if found:
            return found
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


class GradeBot:
    def __init__(self, headless=True):
        self.options = Options()
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--disable-blink-features=AutomationControlled')

        if headless:
            self.options.add_argument('--headless=new')
            self.options.add_argument('--window-size=1920,1080')

        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)

        chrome_binary = _find_chrome_binary()
        if chrome_binary:
            logger.info(f"Chrome encontrado en: {chrome_binary}")
            self.options.binary_location = chrome_binary
        else:
            logger.warning("No se encontró Chrome automáticamente; Selenium intentará con la ruta por defecto.")

        self.driver = webdriver.Chrome(options=self.options)

        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        self.wait = WebDriverWait(self.driver, 25)
        self.driver.set_window_position(0, 0)

    def login(self, username, password, status_callback=None):
        def report(msg):
            if status_callback:
                status_callback(msg)
            logger.info(msg)

        login_url = 'https://autenticasia.unal.edu.co/oam/server/obrareq.cgi?encquery%3DOiqDM2%2FbKs%2F7S1j2OCfNjO8cJRj6gp%2FEKcxPDw2jhQTGrk4LLTTlnyMALD4y1L00FiDrVM4oTJZvDxOoWi3x3dTNnzbD9waYX2DS3ZSo3YLHqrCQ3O%2FTNH4BPHJFJ7eZK6%2FsQ%2BtJm4UKuO%2FNOD9j4P3w0%2BUocHGvd16XfGUCqUYhvPJ73kJ8trkkHoHFeY%2BoQ9YUvjWFCAK8Tn9XuQ7jLMoO%2FEAnaJKONvKQKucYn0I3uSP0Xy7%2FUdK38gduiqIwUx8%2FH9HtMV9rN%2BP175Ym4RxcIZJBkQKUFH1ujbHD5PG9l2U36KTC5MZ%2B9xFHUtaXU0cPvM%2BuXrY7zWQd48kFEY9wShVH%2BEscJtR1XK%2FIHNCwYNbCidQ7eQopBKe3q0aUu5C7nlbB4Qy7e%2F%2FU3l3EdxVrUZVCSvAfLJftCvtzeEfmwQgXe%2B12xTIrzKED%2B8Ipew%2FVG0SyH56LT6VJub5uQhoTB%2BSgPZ%2BTyrk3cmTgA4TxulLaPLGTzU6BM4WvRdeYpDC0tD5gsFV6PckTdeJHGg%2FfXQFIVcScjt50bWpGxbFUnIn082GWYE%2FCDokZ%2BxSYQj4GSFd7ctGoiDFbLG03awAwRg684AL012mcFjHcvqJz%2FB20IhVbSGOe1Fsr%2BZZaBpkabILVfInntvtgtWYDhk7vQK%2BFIjpLYgeTEUbZ4eixykBv8AbS5R3wQnLIpITnSNcpX2WvbXw7OHC%2BfF21qqGZfwstnl6trX2oZbOh4UxLFMxgCOVSCPfj5YGZinMBoD%2FtjO5mGgk%2Bo7If91zb%2Bj73Tth8vM%2FWz9QJS7FmIju%2FrL%2BDT%2BFubQUesKqQJOB6gP8hTE%2FZWm4btGWNdWVqKHdfjdRMpoOQP2Oh6TDuAqycyzoWphkLd8yqlg5Ofdlx5skYG%2F8FpTaNYECdtmZHriEmH93sN5W98ulwstiAY8TAyWmc3XdoqpgyrltTxBJOc%2FwsTHAzHOYRD2tPcaAyrMYvUMXkXpy7zsa4AcVJ5h5HIxKMeVkiqW%2F62rxzKMcZZSNS%2BPcn8bM0LyYUfjffNcVHq9BWr6WT9p3sM1Sv6YtFxRkHfu8RIHe8vXPWisokZFXTaCffIiWYYGjdbDiBOAag7TlXQEn4OZZIT4Gw1hy4J4g%2FWIwfQdFmvHRks3QbhEP9cRSylrKc9tiX8xyHErbS1aHi%2FmnUv7lhm8xTfJlGBp1ksyM5jAKUB9i%2BowymUZPtA%2FcI%2FCKbrgAiqNFGWgsG%2FudlF7SACkuj%2F3k5A1El0RtTXL8ZRqGl4qevk%2FPs%20agentid%3DWT_UNAL_PROD%20ver%3D1%20crmethod%3D2%26cksum%3Deea9512d47276d43823536267496021938093bef&ECID-Context=1.006EgZlvFv16YNuMwa3j6G0027CT01L8kG%3BkXjE'

        try:
            report("🚀 Iniciando motor de automatización...")
            self.driver.get(login_url)

            report("🌐 Abriendo portal UNAL - Autenticación...")
            user_field = self.wait.until(EC.visibility_of_element_located((By.ID, "username")))
            user_field.send_keys(username)
            user_field.send_keys(Keys.ENTER)

            report("🔐 Validando credenciales...")
            pass_field = self.wait.until(EC.visibility_of_element_located((By.ID, "password")))
            pass_field.send_keys(password)
            pass_field.send_keys(Keys.ENTER)

            report("👨‍🏫 Accediendo al rol de Docente...")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), 'Rol de docente')]"))).click()

            report("📚 Preparando panel de calificaciones...")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Calificaciones')]"))).click()

            report("📂 Organizando ventanas de gestión...")
            self.wait.until(lambda d: len(d.window_handles) > 1)
            self.driver.switch_to.window(self.driver.window_handles[1])

            report("✅ ¡Acceso concedido! Cargando tus grupos...")
            aux = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="vMenuPrincipal"]')))
            self.menu_url = aux.get_attribute('href')

            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[2])
            self.driver.get(self.menu_url)

        except (TimeoutException, WebDriverException) as e:
            screenshot_path = os.path.join(os.getcwd(), "error_login.png")
            try:
                self.driver.save_screenshot(screenshot_path)
                logger.error(f"Captura guardada en: {screenshot_path}")
            except WebDriverException:
                logger.warning("No se pudo guardar captura de pantalla")
            logger.error(f"ERROR DURANTE EL LOGIN: {e}")
            raise

    def get_groups_list(self):
        rows = self.driver.find_elements(By.XPATH, "//form//table//tr")
        groups = []
        for i, row in enumerate(rows[1:]):  # skip header
            try:
                row.find_element(By.TAG_NAME, "a")
                groups.append({
                    "id": i + 2,
                    "name": row.text.strip()
                })
            except NoSuchElementException:
                continue
        return groups

    def enter_group(self, group_id):
        ruta_grupo = f"//form//table//tr[{group_id}]//a"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, ruta_grupo))).click()

    def get_grading_options(self):
        select = self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form[2]/table[1]/tbody/tr/td[1]/select")))
        options = select.find_elements(By.TAG_NAME, "option")
        return [{"id": i + 1, "name": opt.text.strip()} for i, opt in enumerate(options)]

    def start_grading(self, exam_mappings, df, log_callback):
        """
        exam_mappings: list of {"op_id": int, "exam_col": str, "name": str}
        """
        total_results = []

        col_doc = next((c for c in df.columns if str(c).strip().lower() == 'documento'), None)
        if not col_doc:
            log_callback("ERROR: No se encontró columna 'Documento' en el archivo.")
            return None

        df = df.rename(columns={col_doc: 'Documento'})
        df['Documento'] = df['Documento'].fillna(0).astype(int)

        for mapping in exam_mappings:
            op_id = mapping['op_id']
            exam_col = mapping['exam_col']
            exam_name = mapping['name']

            log_callback(f"-------------------------------------------")
            log_callback(f"🎯 PROCESANDO: {exam_name}")
            log_callback(f"-------------------------------------------")

            try:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/form[2]/table[1]/tbody/tr/td[1]/select/option[{op_id}]"))).click()
                time.sleep(2)
            except TimeoutException as e:
                log_callback(f"❌ Error al seleccionar opción {exam_name}: {str(e)}")
                continue

            if exam_col not in df.columns:
                log_callback(f"⚠️ Saltando {exam_name}: Columna '{exam_col}' no encontrada en el Excel.")
                continue

            exam_df = df.copy()
            exam_df[exam_col] = exam_df[exam_col].apply(lambda x: math.floor(10 * float(x) + 0.5) / 10 if pd.notnull(x) else 0.0)

            stats = {
                "name": exam_name,
                "total": 0,
                "passed": 0,
                "failed": 0,
                "average": 0,
                "bins": [0, 0, 0, 0, 0]
            }
            all_grades = []

            j = 0
            while True:
                log_callback(f"[{exam_name}] Procesando página {j+1}...")
                for k in range(25):
                    xpath_alumno = f"/html/body/form[3]/table[2]/tbody/tr[{k+2}]/td[1]"
                    xpath_input = f"/html/body/form[3]/table[2]/tbody/tr[{k+2}]/td[5]/input"

                    try:
                        elemento_alumno = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath_alumno)))
                        texto_alumno = elemento_alumno.text

                        match = re.search(r'\[(\d+)\]', texto_alumno)
                        if match:
                            doc_estudiante = int(match.group(1))
                            fila_estudiante = exam_df[exam_df['Documento'] == doc_estudiante]

                            if not fila_estudiante.empty:
                                valor = fila_estudiante.iloc[0][exam_col]

                                campo = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_input)))
                                campo.clear()
                                campo.send_keys(str(valor))

                                stats["total"] += 1
                                all_grades.append(valor)
                                if valor >= 3.0:
                                    stats["passed"] += 1
                                else:
                                    stats["failed"] += 1

                                if 0 <= valor < 1:
                                    stats["bins"][0] += 1
                                elif 1 <= valor < 2:
                                    stats["bins"][1] += 1
                                elif 2 <= valor < 3:
                                    stats["bins"][2] += 1
                                elif 3 <= valor < 4:
                                    stats["bins"][3] += 1
                                elif 4 <= valor <= 5:
                                    stats["bins"][4] += 1
                    except TimeoutException:
                        break

                try:
                    btn_env = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/form[3]/table[3]/tbody/tr/td[3]/input")))
                    btn_env.click()
                    time.sleep(2)
                    try:
                        alert = self.driver.switch_to.alert
                        alert.accept()
                    except NoAlertPresentException:
                        pass
                except TimeoutException:
                    log_callback(f"❌ Error al guardar página en {exam_name}")

                try:
                    celda_nav = self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form[3]/table[3]/tbody/tr/td[4]")))
                    enlaces = celda_nav.find_elements(By.TAG_NAME, "a")
                    btn_next = next((l for l in enlaces if "Siguiente" in l.text), None)

                    if btn_next:
                        btn_next.click()
                        j += 1
                        time.sleep(2)
                    else:
                        break
                except TimeoutException:
                    break

            if stats["total"] > 0:
                stats["average"] = round(sum(all_grades) / stats["total"], 2)

            total_results.append(stats)
            log_callback(f"✅ Finalizado: {exam_name} ({stats['total']} notas)")

        return total_results

    def return_to_menu(self):
        if hasattr(self, 'menu_url'):
            self.driver.get(self.menu_url)

    def close(self):
        self.driver.quit()
