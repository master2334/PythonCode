import requests
from bs4 import BeautifulSoup
import sqlite3
import time

reply_url = 'http://rs.xidian.edu.cn/home.php?mod=space&uid=295336&do=thread&view=me&type=reply&from=space'
home_url = 'http://rs.xidian.edu.cn/home.php?mod=space&uid=295336&do=profile'

cookies = """Q8qA_2132_nofavfid=1; UM_distinctid=175c10d8d927c3-08da4a7c5aae47-930346c-1fa400-175c10d8d9347e; Q8qA_2132_home_diymode=1; Q8qA_2132_ignore_notice=1; Q8qA_2132_smile=13D1; Q8qA_2132_home_readfeed=1607512524; Q8qA_2132_saltkey=JwbbUoXK; Q8qA_2132_lastvisit=1607746249; Q8qA_2132_seccode=26566.c328eb16ebd1b6b107; Q8qA_2132_lastcheckfeed=325969%7C1607750308; Q8qA_2132_auth=6dc4rkp5qBPwNq5gVunSbUv03G3bFRjsT%2BQWWQkCXNnrVGkFqW4LlS0ZIg%2FvnPAkHsCW6Z8OMdotWD70qMH%2BSHV7jSE; Q8qA_2132_sid=KG55AA; Q8qA_2132_lip=10.175.127.135%2C1607917438; Q8qA_2132_ulastactivity=da3aK5A2Y9IFt5CiQJHo8pG7bqxRqqqyAZGXqQlAj2pbzmpAE7gX; Q8qA_2132_st_t=325969%7C1607942165%7C42fdc1d5a0704891038a133cbe893d44; Q8qA_2132_forum_lastvisit=D_553_1607237488D_555_1607237492D_165_1607513406D_72_1607672077D_106_1607942165; Q8qA_2132_visitedfid=72D561D110D217D13D548D554D549D22D568; Q8qA_2132_st_p=325969%7C1607950626%7C132d9df76f427d19c247c95290864fe4; Q8qA_2132_viewid=tid_1080830; Q8qA_2132_sendmail=1; Q8qA_2132_lastact=1607951543%09misc.php%09patch"""
headers = {"cookie":cookies}

conn = sqlite3.connect('D:\\程序资料\\python\\read-rs\\rs_record.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS time_records
    (id INTEGER PRIMARY KEY,
    online_time TEXT,
    last_visit TEXT,
    last_active TEXT,
    last_publish TEXT);""")
conn.commit()
cursor.execute("""CREATE TABLE IF NOT EXISTS commend_records
    (id INTEGER PRIMARY KEY,
    commend TEXT,
    name TEXT,
    address TEXT);""")
conn.commit()

def Send_Message(message):
    desp = """
        # 内容
        - {commend}
        - {name}
        - {address}
    """.format_map(message["desp"])
    message["desp"] = desp
    requests.post('https://sc.ftqq.com/SCU135387T61e123a7d6dc03eccd443ff45486abf35fd77aeb8e93f.send', data = message)

def save_comment(packet) -> bool:
    com = """
        INSERT INTO commend_records {}
        VALUES (?, ?, ?)
    """.format(str(tuple(packet.keys())).replace(r"'", ""))
    cursor.execute(com, tuple(packet.values()))
    conn.commit()

def save_active(activePacket):
    com = """
        INSERT INTO time_records (online_time, last_visit, last_active, last_publish)
        VALUES (?, ?, ?, ?)
    """
    cursor.execute(com, tuple(activePacket.values()))
    conn.commit()

def Get_Comment(packet) -> bool:
    com = """
        SELECT * 
        FROM commend_records
        WHERE commend=:commend AND name=:name AND address=:address
    """
    cursor.execute(com, packet)
    get = cursor.fetchall()
    if(get):
        return True
    else:
        return False 

def Get_Alive(packet) -> bool:
    com = """
        SELECT * 
        FROM time_records
        WHERE online_time=:online_time AND last_visit=:last_visit AND last_active=:last_active AND last_publish=:last_publish
    """
    print(packet)
    cursor.execute(com, packet)
    get = cursor.fetchall()
    if(get):
        return True
    else:
        return False  

def Find_Comment():
    response = requests.get(reply_url,headers = headers)
    soup = BeautifulSoup(response.text, 'lxml')
    reply = soup.find(class_='bm_c').find("tr", class_='bw0_all')
    content = soup.find(class_='bm_c').find_all("td", class_='xg1')
    comment_name = reply.find_all("a")
    #comment_name[1].text  帖名
    #comment_name[9].contents  发布的专区
    comment_packet={"commend":content[0].text,
        "name":comment_name[1].text,
        "address":comment_name[5].text}
    if( not Get_Comment(comment_packet)):
        save_comment(comment_packet)
        Send_Message({
            "text": "回复检测",
            "desp": comment_packet
        })

def Find_ActiveTime():
    response = requests.get(home_url,headers = headers)
    soup = BeautifulSoup(response.text, 'lxml')
    active_time = soup.find(id='pbbs').find_all('li')
    active_packet = {
              "online_time":active_time[0].text,
              "last_visit":active_time[2].contents[1],
              "last_active":active_time[3].contents[1],
              "last_publish":active_time[4].contents[1]}
    if(not Get_Alive(active_packet)):
        save_active(active_packet)
#active_time[0].text 在线时间
#active_time[2].text 最后访问时间
#active_time[5].text 上次活动时间
#active_time[6].text 上次发表时间

if __name__ == "__main__":
    Find_ActiveTime()
    Find_Comment()
    conn.close()
