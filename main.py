from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy,session
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///TeamPlayer.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app.config['DEBUG']=True
db = SQLAlchemy(app)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    players = db.Column(db.String(250), nullable=False)
    rank= db.Column(db.String(250), nullable=False)
    season= db.Column(db.String(200), nullable=False)
    points=db.Column(db.String(200),nullable=False)
stats=[]
s=[]

stat={}
app.app_context().push()
db.create_all()

@app.route('/add',methods=['GET','POST'])
def add():
    x=''
    stats=[]
    chrome_driver_path = r"C:\Users\louay\Downloads\chromedriver_win32\chromedriver.exe"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)  # Keeps the browser open when the script finishes
    service = ChromeService(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.nba.com/stats/players/traditional?SeasonType=Regular+Season&PerMode=Totals")
    sleep(2)

    close=driver.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]')
    close.click()
    sleep(1)
    flag=False
    for j in range(10):
        if flag:
            x=""
            selet=driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div[2]/div[3]/section[1]/div/div/div[1]/label/div/select')
            selet.click()
            sleep(1)
            selet.send_keys(Keys.ARROW_DOWN)
            sleep(1)
            selet.send_keys(Keys.ENTER)
        flag=True
        for i in range(10):
            sleep(1)
            players=driver.find_element(By.CSS_SELECTOR,'.Crom_body__UYOcU tr'+x+' td+td a')
            rank=driver.find_element(By.CSS_SELECTOR,'.Crom_body__UYOcU tr'+x+' td')
            points=driver.find_element(By.CSS_SELECTOR,'.Crom_body__UYOcU tr'+x+' td+td+td+td+td+td+td+td+td')
            season=driver.find_element(By.CSS_SELECTOR,'.SplitsPills_sp__GHtfm div span+span')
            sleep(1)
            stat = {"players": players.text, 'rank': rank.text, "points": points.text, "season": season.text}
            stats.append(stat)
            x+="+tr"
    for k in stats:
        sleep(1)
        new_player=Player(

            players=k['players'],
            rank=k['rank'],
            season=k['season'],
            points=k['points']
        )
        sleep(1)
        db.session.add(new_player)
        db.session.commit()

    return render_template('playerselect.html')

@app.route('/')
def home():
    posts = Player.query.all()

    return render_template("index.html", stap=posts)
@app.route('/player')
def player():
    d={}
    b=Player.query.all()
    for i in b:
        if i.players not in d:
            d[i.players]=[i.points,i.rank,i.season]
        else:
            d[i.players]+=[i.points,i.rank,i.season]
    return d
@app.route('/addteam')
# def addteam():
#     y=''
#     g=[]
#     chrome_driver_path = r"C:\Users\louay\Downloads\chromedriver_win32\chromedriver.exe"
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_experimental_option("detach", True)  # Keeps the browser open when the script finishes
#     service = ChromeService(executable_path=chrome_driver_path)
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#     driver.get("https://www.nba.com/stats/teams/traditional")
#     sleep(1)
#
#     sleep(1)
#     fla = False
#     for j in range(10):
#         if fla:
#             y = ""
#             selet = driver.find_element(By.XPATH,
#                                         '//*[@id="__next"]/div[2]/div[2]/div[3]/section[1]/div/div/div[1]/label/div/select')
#             selet.click()
#             sleep(1)
#             selet.send_keys(Keys.ARROW_DOWN)
#             sleep(1)
#             selet.send_keys(Keys.ENTER)
#         fla = True
#         for i in range(10):
#             sleep(1)
#             team = driver.find_element(By.CSS_SELECTOR, '.Crom_body__UYOcU tr' + y + ' td+td a div div+span')
#             # rank = driver.find_element(By.CSS_SELECTOR, '.Crom_body__UYOcU tr' + x + ' td')
#             # points = driver.find_element(By.CSS_SELECTOR, '.Crom_body__UYOcU tr' + x + ' td+td+td+td+td+td+td+td+td')
#             # season = driver.find_element(By.CSS_SELECTOR, '.SplitsPills_sp__GHtfm div span+span')
#             sleep(1)
#             t={"team":team}
#             g.append(t)
#             y += "+tr"
#     for e in g:
#         sleep(1)
#         new_team=Team(
#
#             team=e['team'],
#             # rank=k['rank'],
#             # season=k['season'],
#             # points=k['points']
#         )
#         sleep(1)
#         db.session.add(new_team)
#         db.session.commit()
#
#     return render_template('team.html')

@app.route('/team')
def team():
    aw=Team.query.all()
    return render_template('team.html',aw=aw)


if __name__=='__main__':
    app.run(debug=True,port=8888)