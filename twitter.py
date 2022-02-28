from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Twitter:
    def __init__(self, email, password, headless):
        chrome_options = Options()
        if (headless == True):
            chrome_options.add_argument("--headless")

        self.browser = webdriver.Chrome(options=chrome_options)
        self.email = email
        self.password = password

    def signIn(self):
        self.browser.get("https://twitter.com/login")
        emailInput = WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[5]/label/div/div[2]/div/input')))
        emailInput.send_keys(self.email)
        emailInput.send_keys(Keys.ENTER)

        passwordInput = WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[3]/div/label/div/div[2]/div[1]/input')))
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)

    def tweet(self, tweet, image=None):
        self.browser.get("https://twitter.com/home")
        tweetInput = WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div')))
        tweetInput.send_keys(tweet)

        if (image != None):
            imageInput = self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[1]/input")
            imageInput.send_keys(image)

        tweetInput.send_keys(Keys.CONTROL + Keys.ENTER)
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div[1]/span')))
