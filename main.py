from kivymd.app import MDApp
from kivmob import KivMob, TestIds, RewardedListenerInterface
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
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
                size_hint=(None, None), size=(300, 300))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                content=Label(text='Please fill all inputs.'),
                size_hint=(None, None), size=(300, 300))

    pop.open()


def todaylimit():
    pop = Popup(title='Limit Reached',
                content=Label(text='See you tomorrow '),
                size_hint=(None, None), size=(300, 300))

    pop.open()


def resultcomming():
    pop = Popup(title='please wait',
                content=Label(text='result is coming  '),
                size_hint=(None, None), size=(300, 300))

    pop.open()


# fire_base_url = "https://kivydb-bc692-default-rtdb.firebaseio.com/Username.json"
# fire_base_url = fire_base_url[0:57] + st + fire_base_url[57:]
# res = requests.get(url=fire_base_url).json()


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
                    if res == None:
                        invalidLogin()
                    elif self.user.text != res[1] or self.password.text != res[2]:
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


# def seoreview():

class MainWindow(Screen):
    dropdow = ObjectProperty()

    def onstart(self):
        self.dropdow = MDDropdownMenu()
        self.dropdow.items.append(
            {"viewclass": "MDMenuItem",
             "text": "Logout", "callback": self.logout()}
        )

    def logout(self):
        # print("logout is called")
        f = open('abc.txt', 'r+')
        f.truncate(0)
        f.close()
        sm.current = "login"

    def letsgo(self):
        sm.current = "seo"

    def Alexa(self):
        sm.current = "alexa"


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
        resultcomming()
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
        # user = firereq[1]
        # pas = firereq[2]

        if int(firereq[0]) == 20:
            todaylimit()
            self.loggedintoseo = 0
        elif int(firereq[0]) != 20:
            if self.loggedintoseo == 0:

                self.requestforseoreview = self.logintoseoreview()
                self.loggedintoseo = 1
                url_input = self.ids.url
                url_label = self.ids.url_label
                da = self.ids.da
                pa = self.ids.PA
                mozrank = self.ids.mozrank
                Traffic = self.ids.traffic

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
                    raa = self.requestforseoreview.post("https://www.seoreviewtools.com/bulk-domain-rating-checker/", d,
                                                        headers=headers)
                    soup2 = BeautifulSoup(raa.content, 'lxml')
                    soup3 = soup2.find_all("td")
                    soup5 = soup3[2].text
                    DRText = f"DR: {soup5}"
                    DR.text = DRText
                except:
                    print("error")

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

    def home(self):
        sm.current = "main"
        
class AlexaRankChecker(Screen):
    def getresult(self):
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
        if int(firereq[4]) == 20:
            todaylimit()
            self.loggedintoseo = 0
        elif int(firereq[4]) != 20:

            url_input = self.ids.url
            url_label = self.ids.url_label
            Country = self.ids.country
            Global_rank = self.ids.global_rank
            Country_rank = self.ids.country_rank
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

            Countrytext = f"Country\n {hg[5]}"
            globalranktext = f"G. Rank {hg[3]}"
            Country.text = Countrytext
            Global_rank.text = globalranktext
            Countryranktext = f"C Rank {hg[7]}"
            Country_rank.text = Countryranktext
            globalranktext = f"G. Rank {hg[3]}"
            Country.text = Countrytext
            Global_rank.text = globalranktext
            Countryranktext = f"C Rank {hg[7]}"
            Country_rank.text = Countryranktext
            url_label.text = url_input.text
            url_input.text = ""
            
            new_res = int(firereq[0])
            new_res += 1
            new_res = str(new_res)
            firereq[4] = new_res
            res = json.dumps(firereq)
            req = requests.put(url=fire_base_url, json=json.loads(res))
            print("finish")
    def home(self):
        sm.current = "main"

    def logout(self):
        # print("logout is called")
        f = open('abc.txt', 'r+')
        f.truncate(0)
        f.close()
        sm.current = "login"


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
            pos_hint:{"center_x":.5,"center_y":.7}
            size_hint:.8,.2
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]
           
            MDRectangleFlatButton:
                text: "GET SEO INFORMATION"
                
                theme_text_color: "Custom"
                text_color: 63/255.0, 81/255.0, 181/255.0,1
                line_color: 0, 1, 1, 1  
                md_bg_color:1,1,1,1
                pos_hint:{"center_y":.5}   
                size_hint:.8,.7
              
                on_release:
                    root.letsgo()
          
        MDCard:
            pos_hint:{"center_x":.5,"center_y":.5}
            size_hint:.8,.2
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]
           
            MDRectangleFlatButton:
                text: "ALEXA RANK CHECKER"
                
                theme_text_color: "Custom"
                text_color: 63/255.0, 81/255.0, 181/255.0,1
                line_color: 0, 1, 1, 1  
                md_bg_color:1,1,1,1
                pos_hint:{"center_y":.5}   
                size_hint:.8,.7
              
                on_release:
                    root.Alexa()

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
        MDLabel:
            text:"Note: Please Wait After Clicking Get Result"
            halign:"center"
            pos_hint: {"center_y":0.85}
            font_style:"Subtitle2"
            theme_text_color :"Custom"
            text_color: 1,0,0,1
        MDLabel:
            text:"_______________"
            halign:"center"
            pos_hint: {"center_y":0.835}
            font_style:"Subtitle2"
            theme_text_color :"Custom"
            text_color: 1,0,0,1

        MDTextField:
            hint_text: "Enter URL(eg https://www.example.com)"
            id: url
            pos_hint: {"center_x": 0.47 , "center_y":0.77}
            current_hint_text_color:0,0,0,1
            size_hint_x: 0.8

        MDFlatButton:
            text: "GET RESULTS"
            theme_text_color: "Custom"
            theme_text_color:"Custom"
            pos_hint:{"center_x":.75,"center_y":.7}
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            theme_text_color :"Custom"
            text_color: 1, 1, 1,1
            border_radius: 20
            radius: [15]
            on_release:root.get_result()


        MDLabel:
            id:url_label
            text:"Results For:_/_"
            halign:"center"
            pos_hint:{"center_x":.5,"center_y":.65}
            font_style:"Subtitle1"
            theme_text_color :"Custom"
            text_color: 0,0,0,1
        MDCard:
            pos_hint:{"center_x":.2,"center_y":.57}
            size_hint:.25,.12
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]

            MDLabel:
                id:da
                text:"DA:_/_"
                halign:"center"
                pos_hint:{"center_y":.5}
                font_style:"Body2"
                theme_text_color :"Custom"
                text_color: 1,1,1,1

        MDCard:
            pos_hint:{"center_x":.75,"center_y":.57}
            size_hint:.25,.12
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]
            MDLabel:
                id: PA
                text:"PA:_/_"
                halign:"center"
                pos_hint:{"center_y":.5}
                font_style:"Body2"
                theme_text_color :"Custom"
                text_color: 1,1,1,1

        MDCard:
            pos_hint:{"center_x":.616,"center_y":.42}
            size_hint:.53,.12
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]
            MDLabel:
                id:traffic
                text:"Traffic:_/_"
                halign:"center"
                pos_hint:{"center_y":.5}
                font_style:"Body2"
                theme_text_color :"Custom"
                text_color: 1,1,1,1

        MDCard:
            pos_hint:{"center_x":.2,"center_y":.42}
            size_hint:.25,.12
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]

            MDLabel:
                id:mozrank
                text:"MOZ RANK:_/_"
                halign:"center"
                pos_hint:{"center_y":.5}
                font_style:"Body2"
                theme_text_color :"Custom"
                text_color: 1,1,1,1

        MDCard:
            pos_hint:{"center_x":.475,"center_y":.57}
            size_hint:.25,.12
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]

            MDLabel:
                id:dr
                text:"DR:_/_"
                halign:"center"
                pos_hint:{"center_y":.5}
                font_style:"Body2"
                theme_text_color :"Custom"
                text_color: 1,1,1,1

            
<AlexaRankChecker>:
    name:"alexa"
    MDFloatLayout:
        orientation:"vertical"
        MDToolbar:
            title:"ALEXA RANK"
            anchor_title: "center"
            left_action_items: [['home', lambda x:root.home()]]
            right_action_items: [['logout', lambda butt:root.logout()]]
            pos_hint: {"top":1}

        
        MDLabel:
            text:"Note: Please Wait After Clicking Get Result"
            halign:"center"
            pos_hint: {"center_y":0.85}
            font_style:"Subtitle2"
            theme_text_color :"Custom"
            text_color: 1,0,0,1
        
        
        
        MDLabel:
            text:"_________________________________"
            halign:"center"
            pos_hint: {"center_y":0.835}
            font_style:"Subtitle2"
            theme_text_color :"Custom"
            text_color: 1,0,0,1

        MDTextField:
            hint_text: "Enter Website(eg. example.com)"
            id: url
            pos_hint: {"center_x": 0.47 , "center_y":0.77}
            current_hint_text_color:0,0,0,1
            size_hint_x: 0.8

        MDFlatButton:
            text: "GET RESULTS"
            theme_text_color: "Custom"
            theme_text_color:"Custom"
            pos_hint:{"center_x":.75,"center_y":.7}
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            theme_text_color :"Custom"
            text_color: 1, 1, 1,1
            border_radius: 20
            radius: [15]
            on_release:root.getresult()
        MDLabel:
            id:url_label
            text:"Results For:_/_"
            halign:"center"
            pos_hint:{"center_x":.5,"center_y":.65}
            font_style:"Subtitle1"
            theme_text_color :"Custom"
            text_color: 0,0,0,1
        MDCard:
            pos_hint:{"center_x": 0.25,"center_y":.55}
            size_hint:.4,.12
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]

            MDLabel:
                id:country
                text:"Country:_/_"
                halign:"center"
                pos_hint:{"center_y":.5}
                font_style:"Body2"
                theme_text_color :"Custom"
                text_color: 1,1,1,1

        MDCard:
            pos_hint:{"center_x":.7,"center_y":.55}
            size_hint:.4,.12
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]

            MDLabel:
                id:country_rank
                text:"Country Rank:_/_"
                halign:"center"
                pos_hint:{"center_y":.5}
                font_style:"Body2"
                theme_text_color :"Custom"
                text_color: 1,1,1,1

        MDCard:
            pos_hint:{"center_x":.478,"center_y":.4}
            size_hint:.85,.12
            md_bg_color:63/255.0, 81/255.0, 181/255.0,1
            border_radius: 20
            radius: [15]

            MDLabel:
                id:global_rank
                text:"Global Rank:_/_"
                halign:"center"
                pos_hint:{"center_y":.5}
                font_style:"Body2"
                theme_text_color :"Custom"
                text_color: 1,1,1,1


"""
kv = Builder.load_string(mykv)

sm = WindowManager()


class MyMainApp(MDApp):
    ads = KivMob(TestIds.APP)

    def build(self):

        self.ads.new_banner(TestIds.BANNER,False  )
        self.ads.request_banner()
        self.ads.show_banner()
        self.ads.add_test_device('ZX1F24P83Z')
        Window.clearcolor = (1, 0, 1, 0)
        self.theme_cls.primary_palette = "Indigo"
        file = open("abc.txt", "r")
        file.seek(0)
        first_char = file.read(1)
        screens = [LoginWindow(name="login"), MainWindow(name="main"), Seochecker(name="seo"),AlexaRankChecker(name="alexa")]
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