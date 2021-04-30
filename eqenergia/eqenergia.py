from selenium.webdriver            import Firefox
from selenium.webdriver            import FirefoxProfile,FirefoxOptions
from selenium.webdriver.common.by  import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support    import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os,re,warnings
from time import sleep
from random import randint
warnings.filterwarnings("ignore")

class Automation(object):
    def __init__(self,email,passwd,name,uc,directory,month=None,delay=60):
        self.__email     = email
        self.__passwd    = passwd
        self.__directory = directory 
        self.__name      = name
        self.__delay     = delay
        self.__baseUrl   = 'https://pa.equatorialenergia.com.br/sua-conta/emitir-segunda-via/#'
        self.__mimeTypes = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml"
        self.__driver    = self.getBrowser()
        self.__uc        = uc
        self.__month     = month

    def getBrowser(self):
        firefox_profile = FirefoxProfile()
        firefox_profile.set_preference('permissions.default.stylesheet', 2)
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        firefox_profile.set_preference("browser.download.folderList", 2)
        firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
        firefox_profile.set_preference("browser.download.dir", os.path.join(os.getcwd(),self.__directory))
        firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", self.__mimeTypes)
        firefox_profile.set_preference("plugin.disable_full_page_plugin_for_types", self.__mimeTypes)
        firefox_profile.set_preference("pdfjs.disabled", True)
        driver = Firefox(firefox_profile=firefox_profile)
        return driver
    
    def selectUC(self):
        try:
            self.__driver.find_element_by_xpath(f"//select[@id='conta_contrato']/option[text()='{self.__uc}']").click()
        except:
            print(f"[-] {self.__uc} não encontrado!")
            exit(0)

    def verifyAlert(self):
        try:
            btn = self.__driver.find_element_by_xpath("//div[@class='jconfirm-buttons']/button[@class='btn btn-default']")
            btn.click()
        except Exception as e:
            pass
        try:
            self.__driver.find_element_by_xpath("//div[@class='lgpd_button']").click()
        except Exception as e:
            pass

    def login(self):
        self.__driver.get(self.__baseUrl)
        self.verifyAlert()
        try:
            btnEntrar = self.__driver.find_element_by_xpath("//a[@class='btn btn-hi account-show-login']")
            btnEntrar.click()
            inputId   = self.__driver.find_element_by_xpath("//input[@id='identificador']")
            inputPass = self.__driver.find_element_by_xpath("//input[@id='senha-identificador']") 
            for c in self.__email:
                inputId.send_keys(c)
                sleep(0.1)
            inputId.send_keys(Keys.TAB)
            inputPass.send_keys(self.__passwd)
            btnLogin = self.__driver.find_element_by_xpath("//button[@id='envia-identificador']")
            btnLogin.click()
        except Exception as e:
            print(f"[-] {str(e)}")

    def renameFile(self,name):
        pathOld = os.path.join(os.path.join(os.getcwd(),self.__directory),"pdf")    
        pathNew = os.path.join(os.path.join(os.getcwd(),self.__directory),name)
        if os.path.isfile(pathOld):
            os.rename(pathOld,pathNew)
            return True
        return False

    def getUc(self):
        try:
            self.__uc = self.__driver.find_element_by_xpath(f"//select[@id='conta_contrato']/option").text
        except:
            print(f"[-] {self.__uc} não encontrado!")
            exit(0)
    def downloadBills(self):
        
        WebDriverWait(self.__driver, self.__delay).until(EC.presence_of_element_located((By.ID, "conta_contrato")))
        sleep(randint(10,15))
        self.__driver.refresh()
        try:    
            tableBills = WebDriverWait(self.__driver, self.__delay).until(EC.presence_of_element_located((By.TAG_NAME, 'tr')))
            trs = self.__driver.find_elements_by_tag_name("tr")
        except Exception as e:
            print(f"[-] {str(e)}")
        parentWindow = self.__driver.window_handles[0]

        if self.__uc:
            self.selectUC()
        else:
            self.getUc()

        if not self.__month:
            for tr in trs:
                td = tr.find_element_by_tag_name("td")
                month = td.text.strip("Referente a\n")
                month = month.replace('/','')
                WebDriverWait(self.__driver,self.__delay).until(EC.element_to_be_clickable((By.TAG_NAME, "td")))
                td.click()
                while self.__driver.find_element_by_xpath("//a[@class='btn download-pdf']").text == 'Aguarde':
                    sleep(0.1)
                self.__driver.find_element_by_xpath("//a[@class='btn download-pdf']").click()
                while True:
            	    if self.renameFile(f"{self.__name}_{month}_{self.__uc}.pdf"):
                        break
                self.__driver.find_element_by_xpath("//div[@class='modal-close']").click()

            # for window in self.__driver.window_handles:
            #     if not window == parentWindow:
            #         try:
            #             self.__driver.switch_to.window(window)
            #             WebDriverWait(self.__driver, self.__delay).until(EC.presence_of_element_located((By.XPATH, "//button[@id='download']")))
            #             btnDownload = self.__driver.find_element_by_xpath("//button[@id='download']")
            #             btnDownload.click()
            #             if self.__uc:
            #                 uc = self.__uc
            #             else:
            #                 uc = ''
            #             while True:
            #                 if self.renameFile(f"{self.__month}_{self.__uc}.pdf"):
            #                     break
            #             self.__driver.close()
            #         except Exception as e:
            #             print(str(e))
            # self.__driver.switch_to.window(parentWindow)
            # self.__driver.close()
        else:
            for tr in trs:
                td = tr.find_element_by_tag_name("td")

                if self.__month in td.text:
                    WebDriverWait(self.__driver,self.__delay).until(EC.element_to_be_clickable((By.TAG_NAME, "td")))
                    td.click()
                    while self.__driver.find_element_by_xpath("//a[@class='btn download-pdf']").text == 'Aguarde':
                        sleep(0.1)
                    self.__driver.find_element_by_xpath("//a[@class='btn download-pdf']").click()
                    while True:
            	        if self.renameFile(f"{self.__month}_{self.__uc}.pdf"):
                            break
                    self.__driver.find_element_by_xpath("//div[@class='modal-close']").click()

            # for window in self.__driver.window_handles:
            #     if not window == parentWindow:
            #         try:
            #             self.__driver.switch_to.window(window)
            #             WebDriverWait(self.__driver, self.__delay).until(EC.presence_of_element_located((By.XPATH, "//button[@id='download']")))
            #             btnDownload = self.__driver.find_element_by_xpath("//button[@id='download']")
            #             btnDownload.click()
            #             if self.__uc:
            #                 uc = self.__uc
            #             else:
            #                 uc = ''
            #             while True:
            #                 print("as")
            #                 if self.renameFile(f"{self.__month}_{self.__uc}.pdf"):
            #                     break
            #             self.__driver.close()
            #         except Exception as e:
            #             print(str(e))
            #             pass
            # self.__driver.switch_to.window(parentWindow)
            # self.__driver.close()
        # self.closeBrowser()

    def closeBrowser(self):
        self.__driver.close()

def test():
    cnpj  = "04986320005263"
    email = "direcao.maraba@unama.br"
    aut   = Automation(cnpj,email,'/home/gustavoid/Documentos/projects/web-scrapper-alex/src')
    aut.login()    
    aut.downloadBills()

if __name__ == '__main__':
    test()
