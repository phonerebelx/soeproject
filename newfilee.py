from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen,NoTransition
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.window import Window
import requests
import json
from bs4 import BeautifulSoup
import time


def invalidLogin():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid username or password.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                content=Label(text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()

def todaylimit():
    pop = Popup(title='Limit Reached',
                content=Label(text='Your Todays Limit has been reached come back tomorrow.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()


class LoginWindow(Screen):
    user = ObjectProperty(None)
    password = ObjectProperty(None)


    def loginBtn(self):
        global st
        st = ""
        for i in self.user.text:
            if i.isnumeric():
                st += i
        if self.user.text == "" or self.password.text == "":
            invalidForm()

        else:
            if st == "":
                invalidLogin()
            else:
                if st != "":
                    fire_base_url = "https://kivydb-bc692-default-rtdb.firebaseio.com/Username.json"
                    fire_base_url = fire_base_url[0:57] + st + fire_base_url[57:]
                    global res
                    res = requests.get(url=fire_base_url).json()
                    if self.user.text != res[1] or self.password.text != res[2]:
                        # print("galat")
                        invalidLogin()
                    elif self.user.text == res[1] and self.password.text == res[2]:
                        # print("ok")
                        file = open("abc.txt", "w")
                        file.seek(0)
                        # first_char = file.read(1)
                        file.write(f"{self.user.text}:{self.password.text}")
                        file.close()
                        sm.current = "main"

class MainWindow(Screen):
    dropdow = ObjectProperty()
    def onstart(self):
        self.dropdow = MDDropdownMenu()
        self.dropdow.items.append(
            {"viewclass":"MDMenuItem",
             "text":"Logout","callback":self.logout()}
        )
    def logout(self):
        # print("logout is called")
        f = open('abc.txt', 'r+')
        f.truncate(0)
        f.close()
        sm.current = "login"

    def letsgo(self):
        sm.current = "seo"

class Seochecker(Screen):
    loggedintoseo = 0
    requestforseoreview = None
    def logintoseoreview(self):
        a = open("abc.txt", "r")
        line = a.readline()
        am = line.split(":")
        req = requests.session()
        payload = {
            "log": am[0],
            'pwd': am[1]}
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        }
        xa = req.post("https://www.seoreviewtools.com/wp-login.php", data=payload, headers=headers)
        return req
    def logout(self):
        # print("logout is called")
        f = open('abc.txt', 'r+')
        f.truncate(0)
        f.close()
        sm.current = "login"


    def get_result(self):
        xa = open("abc.txt", "r")
        lines = xa.readline()
        aa = ""
        for i in lines:
            if i == ":":
                break
            elif i.isnumeric():
                aa += i
        fire_base_url1 = "https://kivydb-bc692-default-rtdb.firebaseio.com/Username.json"
        fire_base_url = fire_base_url1[0:57] + aa + fire_base_url1[57:]
        firereq = requests.get(url=fire_base_url).json()


        if int(firereq[0]) == 20:
            todaylimit()
            self.loggedintoseo = 0
        elif int(firereq[0]) != 0:
            if self.loggedintoseo == 0:
                self.requestforseoreview = self.logintoseoreview()
                self.loggedintoseo = 1
                url_input = self.ids.url
                url_label = self.ids.url_label
                da = self.ids.da
                pa = self.ids.PA
                mozrank = self.ids.mozrank
                Traffic = self.ids.traffic
                globalrank = self.ids.global_rank
                Country = self.ids.country
                Countryrank = self.ids.country_rank
                DR = self.ids.dr
                abc = f"Results for: {url_input.text}"
                url_label.text = abc

                # print(url_input.text)
                reqformoz = requests.session()
                m = {"url": url_input.text,
                     "submit": "Submit"
                     }
                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
                }
                a = reqformoz.post("https://demo.atozseotools.com/mozrank-checker/output", m, headers=headers)
                x = a.content
                # print(x)
                soup1 = BeautifulSoup(x, 'lxml')
                lst1 = []
                counter = 0
                for tagb in soup1.find_all("td"):
                    if counter <= 5:
                        lst1.append(tagb.text)
                    else:
                        pass

                # print(lst1)
                datext = f"DA:{lst1[7]}"
                patext = f"PA:{lst1[5]}"
                mozranktext = f"MozRank:{lst1[3]}"

                pa.text = patext
                da.text = datext
                mozrank.text = mozranktext
                reqfortraff = requests.session()
                m = {
                    "ckwebsite": url_input.text,
                    "submitter": "Check"
                }
                a = reqfortraff.post("https://websiteseochecker.com/website-traffic-checker/", m, headers=headers)
                counter = 0
                lst2 = []
                soup2 = BeautifulSoup(a.content, 'lxml')
                for tagb in soup2.find_all("td"):
                    if counter <= 5:
                        lst2.append(tagb.text)
                    else:
                        pass
                Traffictext = f"Mon. Traffic:{lst2[2]}"
                Traffic.text = Traffictext
                b = "https://demo.atozseotools.com/alexa-rank-checker/output"
                x = url_input.text
                m = {
                    "url": x,
                    "submit": "Submit"
                }
                reqforalexa = requests.session()
                ra = reqforalexa.post(b, m)
                counter = 0
                lst2 = []
                soup2 = BeautifulSoup(ra.content, 'lxml')
                for tagb in soup2.find_all("tbody"):
                    if counter <= 5:
                        lst2.append(tagb.text)
                    else:
                        pass
                f = lst2[0]
                z = f.split("\n")
                hg = []
                for i in range(17):
                    if z[i] == "":
                        pass
                    else:
                        hg.append(z[i])
                d = {
                    "urls": f"https://www.{url_input.text}",
                    "captcha": "",
                    "cc": 105,
                    "submit": ""
                }
                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
                }
                try:
                    raa = self.requestforseoreview.post("https://www.seoreviewtools.com/bulk-domain-rating-checker/", d, headers=headers)
                    soup2 = BeautifulSoup(raa.content, 'lxml')
                    soup3 = soup2.find_all("td")
                    soup5 = soup3[2].text
                    DRText = f"DR: {soup5}"
                    DR.text = DRText
                except:
                    print("error")
                Countrytext = f"Country\n {hg[5]}"
                globalranktext  = f"G. Rank {hg[3]}"
                Country.text = Countrytext
                globalrank.text = globalranktext
                Countryranktext = f"C Rank {hg[7]}"
                Countryrank.text = Countryranktext
                url_input.text = ""
                new_res = int(firereq[0])
                new_res += 1
                new_res = str(new_res)
                firereq[0] = new_res
                res = json.dumps(firereq)
                req = requests.put(url=fire_base_url, json=json.loads(res))
            elif self.loggedintoseo == 1:
                url_input = self.ids.url
                url_label = self.ids.url_label
                da = self.ids.da
                pa = self.ids.PA
                mozrank = self.ids.mozrank
                Traffic = self.ids.traffic
                globalrank = self.ids.global_rank
                Country = self.ids.country
                Countryrank = self.ids.country_rank
                DR = self.ids.dr
                abc = f"Results for: {url_input.text}"
                url_label.text = abc

                reqformoz = requests.session()
                m = {"url": url_input.text,
                     "submit": "Submit"
                     }
                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
                }
                a = reqformoz.post("https://demo.atozseotools.com/mozrank-checker/output", m, headers=headers)
                x = a.content
                soup1 = BeautifulSoup(x, 'lxml')
                lst = []
                counter = 0
                for tagb in soup1.find_all("td"):
                    if counter <= 5:
                        lst.append(tagb.text)
                    else:
                        pass
                datext = f"DA:{lst[7]}"
                patext = f"PA:{lst[5]}"
                mozranktext = f"MozRank:{lst[3]}"

                pa.text = patext
                da.text = datext
                mozrank.text = mozranktext
                reqfortraff = requests.session()
                m = {
                    "ckwebsite": url_input.text,
                    "submitter": "Check"
                }
                a = reqfortraff.post("https://websiteseochecker.com/website-traffic-checker/", m, headers=headers)
                counter = 0
                lst2 = []
                soup2 = BeautifulSoup(a.content, 'lxml')
                for tagb in soup2.find_all("td"):
                    if counter <= 5:
                        lst2.append(tagb.text)
                    else:
                        pass
                Traffictext = f"Mon. Traffic:{lst2[2]}"
                Traffic.text = Traffictext
                b = "https://demo.atozseotools.com/alexa-rank-checker/output"
                x = url_input.text
                m = {
                    "url": x,
                    "submit": "Submit"
                }
                reqforalexa = requests.session()
                ra = reqforalexa.post(b, m)
                counter = 0
                lst2 = []
                soup2 = BeautifulSoup(ra.content, 'lxml')
                for tagb in soup2.find_all("tbody"):
                    if counter <= 5:
                        lst2.append(tagb.text)
                    else:
                        pass
                f = lst2[0]
                z = f.split("\n")
                hg = []
                for i in range(17):
                    if z[i] == "":
                        pass
                    else:
                        hg.append(z[i])
                d = {
                    "urls": f"https://www.{url_input.text}",
                    "captcha": "",
                    "cc": 105,
                    "submit": ""
                }
                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
                }
                try:
                    raa = self.requestforseoreview.post("https://www.seoreviewtools.com/bulk-domain-rating-checker/", d,
                                                        headers=headers)
                    soup2 = BeautifulSoup(raa.content, 'lxml')
                    soup3 = soup2.find_all("td")
                    soup5 = soup3[2].text
                    DRText = f"DR: {soup5}"
                    DR.text = DRText
                except:
                    print("error")
                Countrytext = f"Country\n {hg[5]}"
                globalranktext = f"G. Rank {hg[3]}"
                Country.text = Countrytext
                globalrank.text = globalranktext
                Countryranktext = f"C Rank {hg[7]}"
                Countryrank.text = Countryranktext
                url_input.text = ""
                new_res = int(firereq[0])
                new_res += 1
                new_res = str(new_res)
                firereq[0] = new_res
                res = json.dumps(firereq)
                req = requests.put(url=fire_base_url, json=json.loads(res))
    def home(self):
        sm.current = "main"
class WindowManager(ScreenManager):
    pass


mykv = """
<LoginWindow>:
    name: "login"

    user: user
    password:password

    MDFloatLayout:
        MDLabel:
            text:"Login"
            pos_hint: {"center_y":.85}
            font_style:"H3"
            halign:"center"
            theme_text_color :"Custom"
            text_color: 0,0,0,1
        MDLabel:
            text:"SEO HOME"
            pos_hint: {"center_y":.7}
            font_style:"H5"
            halign:"center"
            theme_text_color :"Custom"
            text_color: 0,0,0,1

        MDTextField:
            hint_text: "Enter your Username"
            id: user
            pos_hint: {"center_x": 0.5 , "center_y":0.6}
            current_hint_text_color:0,0,0,1
            size_hint_x: 0.8
        MDTextField:
            hint_text: "Enter your Password"
            id: password
            pos_hint: {"center_x": 0.5 , "center_y":0.45}
            current_hint_text_color:0,0,0,1
            size_hint_x: 0.8
            password:True


        MDRaisedButton:
            text:"Log In"
            pos_hint: {"center_x": 0.5 , "center_y":0.3}
            size_hint_x: 0.5
            on_release:root.loginBtn()


<MainWindow>:
    name: "main"
    MDFloatLayout:
        orientation:"vertical"
        MDToolbar:
            title:"SEO HOME"
            anchor_title: "center"
            left_action_items: [['home', lambda x:x]]
            right_action_items: [['logout', lambda butt:root.logout()]]
            pos_hint: {"top":1}


        MDLabel:
            text:"Available Seo Tools"
            font_style:"H5"
            halign:"center"
            pos_hint: {"center_x": .5, "center_y": .82}
        MDCard:
            pos_hint:{"center_x":.5,"center_y":.6}
            size_hint:.7,.3
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]
            MDIconButton: 
                icon:"toolbox-outline"
                pos_hint:{"center_x":.1,"center_y":.8}
                user_font_size:"40sp"
                theme_text_color:"Custom"
                text_color:1,1,1,1
            MDLabel:
                text:"Complete SEO Information!!"
                halign:"center"
                pos_hint:{"center_y":.5}
                font_style:"H6"
                theme_text_color :"Custom"
                text_color: 1,1,1,1
            MDFlatButton:
                text: "LETS GO"
                theme_text_color: "Custom"
                theme_text_color:"Custom"
                text_color:1,1,1,1
                pos_hint:{"center_x":.4,"center_y":.2}
                md_bg_color:1, 1, 1,1
                theme_text_color :"Custom"
                text_color: 63/255.0, 81/255.0, 181/255.0,1
                on_release:
                    root.letsgo()
        MDCard:
            pos_hint:{"center_x":.5,"center_y":.28}
            size_hint:.7,.3
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]
            MDIconButton: 
                icon:"typewriter"
                pos_hint:{"center_x":.1,"center_y":.8}
                user_font_size:"40sp"
                theme_text_color:"Custom"
                text_color:1,1,1,1
                
            MDLabel:
                text:"More Tools Coming Soon"
                halign:"center"
                pos_hint:{"center_y":.5}
                font_style:"H6"
                theme_text_color :"Custom"
                text_color: 1,1,1,1
            MDIconButton: 
                icon:"codepen"
                pos_hint:{"center_x":.4,"center_y":.2}
                user_font_size:"40sp"
                theme_text_color:"Custom"
                text_color:1,1,1,1
                
            
<Seochecker>:
    name:"seo"
    da:da
    MDFloatLayout:
        orientation:"vertical"
        MDToolbar:
            title:"SEO TOOLS"
            anchor_title: "center"
            left_action_items: [['home', lambda butt:root.home()]]
            right_action_items: [['logout', lambda butt:root.logout()]]
            pos_hint: {"top":1}  
            
        MDTextField:
            hint_text: "Enter URL(eg https://www.example.com)"
            id: url
            pos_hint: {"center_x": 0.5 , "center_y":0.82}
            current_hint_text_color:0,0,0,1
            size_hint_x: 0.8 
        
        MDFlatButton:
            text: "GET RESULTS"
            theme_text_color: "Custom"
            theme_text_color:"Custom"
            pos_hint:{"center_x":.8,"center_y":.75}
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            theme_text_color :"Custom"
            text_color: 1, 1, 1,1
            size: 90, 50
            on_release:root.get_result()
            
        MDLabel:
            id:url_label
            text:"Results For: __/__"
            halign:"center"
            pos_hint:{"center_y":.68}
            font_style:"Subtitle1"
            theme_text_color :"Custom"
            text_color: 0,0,0,1    
        MDCard:
            pos_hint:{"center_x":.2,"center_y":.55}
            size_hint:.25,.12
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]
                
            MDLabel:
                id:da
                text:"DA:__/__"
                halign:"center"
                pos_hint:{"center_y":.5}
                font_style:"Body2"
                theme_text_color :"Custom"
                text_color: 1,1,1,1
                
        MDCard:
            pos_hint:{"center_x":.75,"center_y":.55}
            size_hint:.25,.12
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]
            MDLabel:
                id: PA
                text:"PA:__/__"
                halign:"center"
                pos_hint:{"center_y":.5}
                font_style:"Body2"
                theme_text_color :"Custom"
                text_color: 1,1,1,1
                
        MDCard:
            pos_hint:{"center_x":.475,"center_y":.45}
            size_hint:.25,.12
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]   
            MDLabel:
                id:traffic
                text:"Traffic:__/__"
                halign:"center"
                pos_hint:{"center_y":.5}
                font_style:"Body2"
                theme_text_color :"Custom"
                text_color: 1,1,1,1
                
        MDCard:
            pos_hint:{"center_x":.2,"center_y":.35}
            size_hint:.25,.12
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]
                
            MDLabel:
                id:mozrank
                text:"MOZ RANK:__/__"
                halign:"center"
                pos_hint:{"center_y":.5}
                font_style:"Body2"
                theme_text_color :"Custom"
                text_color: 1,1,1,1
                
        MDCard:
            pos_hint:{"center_x":.75,"center_y":.35}
            size_hint:.25,.12
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]
                
            MDLabel:
                id:dr
                text:"DR:__/__"
                halign:"center"
                pos_hint:{"center_y":.5}
                font_style:"Body2"
                theme_text_color :"Custom"
                text_color: 1,1,1,1
        MDCard:
            pos_hint:{"center_x":.475,"center_y":.25}
            size_hint:.25,.12
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]
                
            MDLabel:
                id:global_rank
                text:"Global Rank:__/__"
                halign:"center"
                pos_hint:{"center_y":.5}
                font_style:"Body2"
                theme_text_color :"Custom"
                text_color: 1,1,1,1
                
        MDCard:
            pos_hint:{"center_x":.2,"center_y":.15}
            size_hint:.25,.12
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]
                
            MDLabel:
                id:country
                text:"Country:__/__"
                halign:"center"
                pos_hint:{"center_y":.5}
                font_style:"Body2"
                theme_text_color :"Custom"
                text_color: 1,1,1,1
        MDCard:
            pos_hint:{"center_x":.75,"center_y":.15}
            size_hint:.25,.12
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]
                
            MDLabel:
                id:country_rank
                text:"Country Rank:__/__"
                halign:"center"
                pos_hint:{"center_y":.5}
                font_style:"Body2"
                theme_text_color :"Custom"
                text_color: 1,1,1,1
            
        
            
            
                
        
        
              
"""
kv = Builder.load_string(mykv)

sm = WindowManager()


class MyMainApp(MDApp):
    def build(self):
        Window.clearcolor = (1, 0, 1, 0)
        self.theme_cls.primary_palette = "Indigo"
        file = open("abc.txt", "r")
        file.seek(0)
        first_char = file.read(1)
        screens = [LoginWindow(name="login"), MainWindow(name="main"),Seochecker(name="seo")]
        for screen in screens:
            sm.add_widget(screen)
        sm.current = "login"
        if first_char != "":
            sm.current = "main"
            file.close()
            return sm
        else:
            return sm


MyMainApp().run()