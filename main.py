from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs

PORT = 8080
link = "https://vafs.u.nus.edu/adfs/ls/?SAMLRequest=fZLRT8IwEMbf%2FSuWvm%2FdJiA02xKEGElQCUwffDHdeoMmWzt7Lep%2F7xgSMVFfr9%2FvvvvumiBv6pZNnd2pNbw6QOu9N7VC1j%2BkxBnFNEeJTPEGkNmSbaZ3SxYHIWuNtrrUNTlD%2Fic4IhgrtSLeYp6Sl3FRxSCqwhfVeOQPRAh%2BUUDhR5PxcBzGk0JccuI9gcGOSUnXogMRHSwUWq5sVwrjgR9GfjzK45ANr9hg9Ey8eZdDKm57amdti4zSPa8wcIFyGIBwlIsKaY2UeNPTVDOt0DVgNmD2soTH9fKbLrnaczzRAW5prbdS0UNo4q2%2BVnEtlZBq%2B%2F8WiqMI2W2er%2FzVwyYnWXLow%2FpsJjt4%2Fmp5EMUJPdcmxwvedy6L%2BUrXsvzwbrRpuP17iCiI%2BooUftVLmVPYQikrCaLbR13rt5kBbiEl1jggNDua%2Fvwp2cUn&SigAlg=http%3A%2F%2Fwww.w3.org%2F2001%2F04%2Fxmldsig-more%23rsa-sha256&Signature=cwV5i36TNHhCcuogDSBou%2F5bq%2Fa%2FsRnee%2FLEjHOMRB%2BrBtpUl8L802opknG2%2FNO021%2B1J3SZyxvLY9l8zXsj07DYsiCqbkoaxhD3flO1e%2FewezYexxK9FfHKqjDmrSqHBKsU%2FuTLDmi6nS3%2BQMdHrcr0zniCIpXbM0WEPVayH4BXIhj2wslpMoTTsfTNV4cxet66JcJZsulKh9eyGdZj253l%2BT12qx9py9fn1bPES9i7X4kztZim0LI6YC2jvmQsCgvLBQ5if5rXnsgdlg0fIa876JTvvCUuX7g6O8ZXsKxJeNKN3FZC%2FEd9TzWfd66g4InKsh3O4dSDAdtPQZRt%2FA%3D%3D"

def getCookie(user, password):
  options = webdriver.ChromeOptions()

  options.add_argument('--headless')
  driver = webdriver.Chrome(options=options)
  driver.get(link)

  print(driver.title)

  driver.find_element(By.NAME,"UserName").send_keys(user)
  driver.find_element(By.NAME,"Password").send_keys(password)
  driver.find_element(By.ID,"submitButton").click()

  return driver.get_cookie("canvas_session")["value"]

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
      # get params
      print(self.path)

      parsed_url = urlparse(self.path)
      user = parse_qs(parsed_url.query)['user'][0]
      password = parse_qs(parsed_url.query)['password'][0]
      print(user)
      print(password)

      token = getCookie(user, password)
      self.send_response(200)
      self.end_headers()
      self.wfile.write(bytes(token, 'utf8'))
      return

server = HTTPServer(('localhost', PORT), HTTPRequestHandler)
server.serve_forever()
