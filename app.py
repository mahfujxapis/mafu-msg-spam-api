import requests, os, psutil, sys, jwt, pickle, json, binascii, time, urllib3, base64, datetime, re, socket, threading
import random
from protobuf_decoder.protobuf_decoder import Parser
from xP import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, Lock, Event
from flask import Flask, request, jsonify

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

socket_lock = Lock()
data_lock = Lock()
connected_clients = {}
connected_clients_lock = threading.Lock()

app = Flask(__name__)

class FF_CLient():
    def __init__(self, id, password):
        self.id = id
        self.password = password
        self.thread_pool = ThreadPoolExecutor(max_workers=20)
        self.active_threads = []
        self.thread_timeout = 30
        self.InPuTMsG = ""
        self.DeCode_CliEnt_Uid = ""
        self.CliEnts = None
        self.CliEnts2 = None
        
        with connected_clients_lock:
            connected_clients[self.id] = self
        
        self.Get_FiNal_ToKen_0115()
        


    def GeTinFoSqMsG(self, teamcode):
        try:
            if hasattr(self, 'CliEnts2') and self.CliEnts2:
                self.CliEnts2.send(JoinSq(teamcode, self.key, self.iv))
                time.sleep(1)
                
                if hasattr(self, 'DaTa2') and len(self.DaTa2.hex()) > 4 and '0500' in self.DaTa2.hex()[0:4]:
                    dT = json.loads(DeCode_PackEt(self.DaTa2.hex()[10:]))
                    if '5' in dT and 'data' in dT["5"]:
                        idT = dT["5"]["data"]["1"]["data"]
                        if '14' in dT["5"]["data"] and 'data' in dT["5"]["data"]["14"]:
                            sq = dT["5"]["data"]["14"]["data"]
                        else:
                            sq = "1"
                        
                        self.CliEnts2.send(ExitSq('000000', self.key, self.iv))
                        time.sleep(0.2)
                        
                        return {"success": True, "team_id": idT, "sq": sq}
            
            return {"success": False}
            
        except Exception as e:
            return {"success": False}

    def SeNd_SpaM_MsG(self, team_id, sq, message):
        try:
            threads = []

            message_clients = list(connected_clients.values())[:3]
                
            for client in message_clients:
                thread = threading.Thread(target=self.SeNd_MsG, args=(client, team_id, sq, message))
                threads.append(thread)
                thread.start()
            
            for thread in threads:
                thread.join(timeout=30)
                
        except Exception as e:
            pass

    def SeNd_MsG(self, client, team_id, sq, message):
        try:
            if hasattr(client, 'CliEnts') and client.CliEnts:
                client.CliEnts.send(OpenCh(team_id, sq, client.key, client.iv))
                time.sleep(0.5)

                for i in range(100):
                    client.CliEnts.send(MsqSq(f'[b][c]{generate_random_color()}{message}', team_id, client.key, client.iv))
                    time.sleep(0.5)
                    
        except Exception as e:
            pass

            
    def Connect_SerVer_OnLine(self, Token, tok, host, port, key, iv, host2, port2):
        self.key = key
        self.iv = iv
        while True:
            try:
                self.CliEnts2 = socket.create_connection((host2, int(port2)))
                self.CliEnts2.send(bytes.fromhex(tok))                  
                
                while True:
                    try:
                        self.DaTa2 = self.CliEnts2.recv(99999)
                        if not self.DaTa2:
                            break
                        if len(self.DaTa2.hex()) > 4 and '0500' in self.DaTa2.hex()[0:4] and len(self.DaTa2.hex()) > 30:	         	    	    
                            self.packet = json.loads(DeCode_PackEt(f'08{self.DaTa2.hex().split("08", 1)[1]}'))
                            if '5' in self.packet and 'data' in self.packet['5'] and '7' in self.packet['5']['data'] and 'data' in self.packet['5']['data']['7']:
                                self.AutH = self.packet['5']['data']['7']['data']
                    except Exception as e:
                        break
                    
            except Exception as e:
                time.sleep(2)
                continue
                
    def cleanup_threads(self):
        current_time = time.time()
        self.active_threads = [t for t in self.active_threads 
                              if t['thread'].is_alive() and 
                              current_time - t['start_time'] < self.thread_timeout]
                                                              
    def Connect_SerVer(self, Token, tok, host, port, key, iv, host2, port2):
        self.key = key
        self.iv = iv
        try:
            self.CliEnts = socket.create_connection((host, int(port)))
            self.CliEnts.send(bytes.fromhex(tok))  
            self.DaTa = self.CliEnts.recv(1024)          
        except Exception as e:
            time.sleep(2)
            self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2)
            return
        
        secondary_thread = threading.Thread(target=self.Connect_SerVer_OnLine, args=(Token, tok, host, port, key, iv, host2, port2), daemon=True)
        secondary_thread.start()
               			      	

    def GeT_Key_Iv(self, serialized_data):
        try:
            import xK
            my_message = xK.MyMessage()
            my_message.ParseFromString(serialized_data)
            timestamp, key, iv = my_message.field21, my_message.field22, my_message.field23
            timestamp_obj = Timestamp()
            timestamp_obj.FromNanoseconds(timestamp)
            timestamp_seconds = timestamp_obj.seconds
            timestamp_nanos = timestamp_obj.nanos
            combined_timestamp = timestamp_seconds * 1_000_000_000 + timestamp_nanos
            return combined_timestamp, key, iv            
        except Exception as e:
            return None, None, None

    def GuestLogin(self , uid , password):
        self.url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        self.headers = {"Host": "100067.connect.garena.com","User-Agent": "{Device}","Content-Type": "application/x-www-form-urlencoded","Accept-Encoding": "gzip, deflate","Connection": "close",}
        self.dataa = {"uid": f"{uid}","password": f"{password}","response_type": "token","client_type": "2","client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3","client_id": "100067",}
        try:
            self.response = requests.post(self.url, headers=self.headers, data=self.dataa).json()
            self.Access_ToKen , self.Access_Uid = self.response['access_token'] , self.response['open_id']
            time.sleep(0.2)
            return self.MajorLogin(self.Access_ToKen , self.Access_Uid)
        except Exception: 
            sys.exit()
                                        
    def DataLogin(self , JwT_ToKen , PayLoad):
        self.UrL = 'https://clientbp.ggpolarbear.com/GetLoginData'
        self.HeadErs = {
            'Expect': '100-continue',
            'Authorization': f'Bearer {JwT_ToKen}',
            'X-Unity-Version': '2022.3.47f1',
            'X-GA': 'v1 1',
            'ReleaseVersion': 'OB52',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'clientbp.ggpolarbear.com',
            'Connection': 'close',
            'Accept-Encoding':  'gzip'}     
        try:
                self.Res = requests.post(self.UrL , headers=self.HeadErs , data=PayLoad , verify=False)
                self.DaTa_Pb2 = json.loads(DeCode_PackEt(self.Res.content.hex()))  
                address , address2 = self.DaTa_Pb2['32']['data'] , self.DaTa_Pb2['17']['data'] 
                ip , ip2 = address[:len(address) - 6] , address2[:len(address) - 6]
                port , port2 = address[len(address) - 5:] , address2[len(address2) - 5:]             
                return ip , port , ip2 , port2          
        except requests.RequestException as e:
                pass
        return None, None   

    def MajorLogin(self , Access_ToKen , Access_Uid):
        self.UrL = "https://loginbp.ggpolarbear.com/MajorLogin"
        self.HeadErs = {
            'X-Unity-Version': '2022.3.47f1',
            'ReleaseVersion': 'OB52',
            'Content-Type': 'application/x-www-form-urlencoded',    
            'X-GA': 'v1 1',
            'Content-Length': '928',
            'Host': 'loginbp.ggpolarbear.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'}   

        self.dT = bytes.fromhex('1a13323032352d31312d32362030313a35313a3238220966726565206669726528013a07312e3132302e314232416e64726f6964204f532039202f204150492d3238202850492f72656c2e636a772e32303232303531382e313134313333294a0848616e6468656c64520c4d544e2f537061636574656c5a045749464960800a68d00572033234307a2d7838362d3634205353453320535345342e3120535345342e32204156582041565832207c2032343030207c20348001e61e8a010f416472656e6f2028544d292036343092010d4f70656e474c20455320332e329a012b476f6f676c657c36323566373136662d393161372d343935622d396631362d303866653964336336353333a2010e3137362e32382e3133392e313835aa01026172b201203433303632343537393364653836646134323561353263616164663231656564ba010134c2010848616e6468656c64ca010d4f6e65506c7573204135303130ea014063363961653230386661643732373338623637346232383437623530613361316466613235643161313966616537343566633736616334613065343134633934f00101ca020c4d544e2f537061636574656cd2020457494649ca03203161633462383065636630343738613434323033626638666163363132306635e003b5ee02e8039a8002f003af13f80384078004a78f028804b5ee029004a78f029804b5ee02b00404c80401d2043d2f646174612f6170702f636f6d2e6474732e667265656669726574682d66705843537068495636644b43376a4c2d574f7952413d3d2f6c69622f61726de00401ea045f65363261623933353464386662356662303831646233333861636233333439317c2f646174612f6170702f636f6d2e6474732e667265656669726574682d66705843537068495636644b43376a4c2d574f7952413d3d2f626173652e61706bf00406f804018a050233329a050a32303139313139303236a80503b205094f70656e474c455332b805ff01c00504e005be7eea05093372645f7061727479f205704b717348543857393347646347335a6f7a454e6646775648746d377171316552554e6149444e67526f626f7a4942744c4f695943633459367a767670634943787a514632734f453463627974774c7334785a62526e70524d706d5752514b6d654f35766373386e51594268777148374bf805e7e4068806019006019a060134a2060134b2062213521146500e590349510e460900115843395f005b510f685b560a6107576d0f0366')
        
        self.dT = self.dT.replace(b'2025-07-30 14:11:20' , str(datetime.now())[:-7].encode())        
        self.dT = self.dT.replace(b'c69ae208fad72738b674b2847b50a3a1dfa25d1a19fae745fc76ac4a0e414c94' , Access_ToKen.encode())
        self.dT = self.dT.replace(b'4306245793de86da425a52caadf21eed' , Access_Uid.encode())
        self.PaYload = bytes.fromhex(EnC_AEs(self.dT.hex()))  
        self.ResPonse = requests.post(self.UrL, headers = self.HeadErs ,  data = self.PaYload , verify=False)        
        if self.ResPonse.status_code == 200 and len(self.ResPonse.text) > 10:
            self.DaTa_Pb2 = json.loads(DeCode_PackEt(self.ResPonse.content.hex()))
            self.JwT_ToKen = self.DaTa_Pb2['8']['data']           
            self.combined_timestamp , self.key , self.iv = self.GeT_Key_Iv(self.ResPonse.content)
            ip , port , ip2 , port2 = self.DataLogin(self.JwT_ToKen , self.PaYload)            
            return self.JwT_ToKen , self.key , self.iv, self.combined_timestamp , ip , port , ip2 , port2
        else:
            sys.exit()

    def Get_FiNal_ToKen_0115(self):
        token , key , iv , Timestamp , ip , port , ip2 , port2 = self.GuestLogin(self.id , self.password)
        self.JwT_ToKen = token        
        try:
            self.AfTer_DeC_JwT = jwt.decode(token, options={"verify_signature": False})
            self.AccounT_Uid = self.AfTer_DeC_JwT.get('account_id')
            self.EncoDed_AccounT = hex(self.AccounT_Uid)[2:]
            self.HeX_VaLue = DecodE_HeX(Timestamp)
            self.TimE_HEx = self.HeX_VaLue
            self.JwT_ToKen_ = token.encode().hex()
        except Exception as e:
            return
        try:
            self.Header = hex(len(EnC_PacKeT(self.JwT_ToKen_, key, iv)) // 2)[2:]
            length = len(self.EncoDed_AccounT)
            self.__ = '00000000'
            if length == 9: self.__ = '0000000'
            elif length == 8: self.__ = '00000000  '
            elif length == 10: self.__ = '000000'
            elif length == 7: self.__ = '000000000'
            else:
                pass                
            self.Header = f'0115{self.__}{self.EncoDed_AccounT}{self.TimE_HEx}00000{self.Header}'
            self.FiNal_ToKen_0115 = self.Header + EnC_PacKeT(self.JwT_ToKen_ , key , iv)
        except Exception as e:
            pass
        self.AutH_ToKen = self.FiNal_ToKen_0115
        self.Connect_SerVer(self.JwT_ToKen , self.AutH_ToKen , ip , port , key , iv , ip2 , port2)        
        return self.AutH_ToKen , key , iv

def ChEck_Commande(team_code):
    return bool(team_code and len(team_code) >= 6)

ACCOUNTS = [
    {"id":"4674815268","password":"MAFU-XOCUN3DAN-CORE"},
    {"id":"4674815270","password":"MAFU-AQHIW5FSG-CORE"},
    {"id":"4674815273","password":"MAFU-TSJEWAYAM-CORE"},    
    {"id":"4674815271","password":"MAFU-1G02KSKTJ-CORE"},
    {"id":"4674815269","password":"MAFU-K6NOXSWGP-CORE"}
]

def start_account(account):
    try:
        FF_CLient(account['id'], account['password'])
    except Exception as e:
        start_account(account)

import threading

@app.route('/msg', methods=['GET', 'POST'])
def send_message():
    try:
      
        if request.method == 'GET':
            teamcode = request.args.get('teamcode')
            message = request.args.get('message')
    
        else:
            data = request.get_json()
            teamcode = data.get('teamcode')
            message = data.get('message')

        if not teamcode or not message:
            return jsonify({'status': 'error', 'message': 'Teamcode and message are required'}), 400

        if not ChEck_Commande(teamcode):
            return jsonify({'status': 'error', 'message': 'Invalid teamcode'}), 400

    
        response = jsonify({'status': 'success', 'message': 'Processing started...'})
        
    
        def background_job(teamcode, message):
            try:
                with connected_clients_lock:
                    if len(connected_clients) == 0:
                        return
                
                    first_client = list(connected_clients.values())[0]
                    team_data = first_client.GeTinFoSqMsG(teamcode)

                    if not team_data["success"]:
                        return

                    team_id = team_data["team_id"]
                    sq = team_data["sq"]
                    first_client.SeNd_SpaM_MsG(team_id, sq, message)
            except Exception as e:
                print("Background error:", str(e))

       
        threading.Thread(target=background_job, args=(teamcode, message)).start()

        return response, 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def start_bot():
    time.sleep(10)         
    print(f"\n - Bot is Online")
    print(f" - Connected Successfully!\n")    
    
    threads = []
    
    for account in ACCOUNTS:
        thread = threading.Thread(target=start_account, args=(account,))
        thread.daemon = True
        threads.append(thread)
        thread.start()
        time.sleep(5)
    
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()
    
    app.run(host='0.0.0.0', port=5000, debug=False)