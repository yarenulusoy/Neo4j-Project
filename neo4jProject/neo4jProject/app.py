from flask import Flask, request, render_template, flash, url_for
from neo4j import GraphDatabase
from werkzeug.utils import redirect
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():

    return render_template("anasayfa.html")

@app.route('/admin',methods=('GET', 'POST'))
def admin():
    return render_template("admin.html")

@app.route('/login',methods=('GET', 'POST'))
def login():
    error = None;
    if request.method == 'POST':
        kullaniciadi = request.form['username']
        sifre = request.form['password']
        if kullaniciadi != '1' or sifre != '1':
            error = "Kullanıcı Adı veya Şifre Yanlış."
        else:
            return redirect(url_for('admin'))

    return render_template("login.html",error=error)

class arastirma:
    def __init__(self, ad, soyad):
        self.ad=ad
        self.soyad=soyad

@app.route('/kullanici',methods=('GET', 'POST'))
def kullanici():
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="123")
    sayi = conn.query(
        "MATCH (n:Arastirmacilar)-[r:yayinyazari]->(a:Yayinlar)-[x:yayinlanir]->(d:Türler)    RETURN collect(n.Ad),collect(n.Soyad), a.YayinAdi,a.YayinYili,d.YayinTuru,d.YayinYeri",
        db="neo4j")

    adliste=[]
    soyadliste=[]
    yayinliste=[]
    yilliste =[]
    turliste=[]
    yerliste=[]

    for i in sayi:
        adliste.append(i['collect(n.Ad)'])
        soyadliste.append(i['collect(n.Soyad)'])
        yayinliste.append(i['a.YayinAdi'])
        yilliste.append(i['a.YayinYili'])
        turliste.append(i['d.YayinTuru'])
        yerliste.append(i['d.YayinYeri'])


    return render_template('kullanici.html',info=zip(adliste,soyadliste,yayinliste,yilliste,turliste,yerliste))

@app.route('/grafik/<string:ad>',methods=('GET', 'POST'))
def grafik(ad):
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="123")
    sayi = conn.query(
        "MATCH (n:Arastirmacilar)  where  n.Soyad='%s' RETURN id(n)"%(ad),db="neo4j")
    id=sayi[0]['id(n)']
    print(id)
    return render_template("grafik.html",id=id)

@app.route('/grafik2/<int:id>',methods=('GET', 'POST'))
def grafik2(id):

    return render_template("grafik2.html",id=id)

@app.route('/grafik3/<string:ad>',methods=('GET', 'POST'))
def grafik3(ad):
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="123")
    sayi = conn.query(
        "MATCH (n:Arastirmacilar)  where  n.Soyad='%s' RETURN id(n)"%(ad),db="neo4j")
    id=sayi[0]['id(n)']
    print(id)
    return render_template("grafik3.html",id=id)

@app.route('/grafik4/<int:id>',methods=('GET', 'POST'))
def grafik4(id):

    return render_template("grafik4.html",id=id)

@app.route('/tümverigrafik',methods=('GET', 'POST'))
def tümverigrafik():

    return render_template("tümverigrafik.html")

@app.route('/arastirmaci_ekle',methods=('GET', 'POST'))
def arastirmaci():
    if request.method == 'POST':
        ad = request.form['ad']
        soyad = request.form['soyad']
        greeter = ArastirmaciEkle("bolt://localhost:7687", "neo4j", "123")
        greeter.print_greeting(ad, soyad)
        greeter.close()



    return render_template("arastirmaci_ekle.html")


class Neo4jConnection:

    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response


@app.route('/yayin_ekle',methods=('GET', 'POST'))
def yayin():

    if request.method == 'POST':
        ad = request.form.get('ad')
        print("ad",ad)
        yayinadi = request.form['yayinadi']
        yayinyili = request.form['yayinyili']
        yayinyeri = request.form['yayinyeri']
        yayinturu = request.form['yayinturu']
        greeter3 = TurEkle("bolt://localhost:7687", "neo4j", "123")
        greeter3.print_greeting(yayinturu,yayinyeri)
        greeter3.close()
        greeter2 = YayinEkle("bolt://localhost:7687", "neo4j", "123")
        greeter2.print_greeting(ad, yayinadi, yayinyili,yayinyeri,yayinturu)
        greeter2.close()

    greeter = YazarGetir("bolt://localhost:7687", "neo4j", "123")
    a=greeter.print_greeting()
    greeter.close()

    b=len(a)
    return render_template("yayin_ekle.html",yazarlar=a,uzunluk=b)

class ArastirmaciEkle:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_greeting(self, ad, soyad):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, ad, soyad)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, ad, soyad):
        result = tx.run("CREATE (a:Arastirmacilar) "
                        "SET a.Ad = $ad,a.Soyad=$soyad "
                        "RETURN a.Ad,a.Soyad + ', from node ' + id(a)",
                        ad=ad, soyad=soyad)
        return result.single()[0]




class YayinEkle:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_greeting(self,ad,yayinadi,yayinyili,yayinyeri,yayinturu):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting,ad,yayinadi,yayinyili,yayinyeri,yayinturu)
            print("deneme",greeting)

    @staticmethod
    def _create_and_return_greeting(tx,ad,yayinadi,yayinyili,yayinyeri,yayinturu):
        result = tx.run("MATCH (n:Arastirmacilar) WHERE n.Soyad=$ad RETURN id(n) ",ad=ad)
        id=result.single()[0]

        result2 = tx.run("MATCH (n:Türler) WHERE n.YayinYeri=$yayinyeri RETURN id(n) ",yayinyeri=yayinyeri)
        id2 = result2.single()[0]
        result5 = tx.run("MATCH(a: Yayinlar) where a.YayinAdi=$yayinadi RETURN count(*) ", yayinadi=yayinadi)
        count=result5.single()[0]
        if (count == 0):
            result3 = tx.run("CREATE (b:Yayinlar) "
                             "SET b.TurId=$id2,b.YayinAdi=$yayinadi,b.YayinYili=$yayinyili "
                             "RETURN id(b)",
                             id2=id2, yayinadi=yayinadi, yayinyili=yayinyili)
        # arastirmaci yazar yayini ekle
            # yayinvarsa

        result4 = tx.run(
            "match (a:Yayinlar { YayinAdi:$yayinadi }) match (b:Arastirmacilar { Soyad: $ad }) create (b)-[:yayinyazari]->(a)",
            yayinadi=yayinadi, ad=ad)
       # result4 = tx.run("match (a:Arastirmacilar),(b:Arastirmacilar  WHERE a.Soyad =$ad AND b.Ad= "Esra" create (b)-[:ortakcalisir]->(a)",yayinadi=yayinadi, ad=ad)
        result7 = tx.run("MATCH (n:Yayinlar)-[r:yayinlanir]->(a:Türler) WHERE n.YayinAdi =$yayinadi and a.YayinYeri=$yayinyeri RETURN COUNT(r) ",
                        yayinadi=yayinadi,yayinturu=yayinturu, yayinyeri=yayinyeri)
        count2 = result7.single()[0]

       #yayin yayinlanir tür
        if(count2==0):
            tx.run(
                "match (a:Yayinlar { YayinAdi:$yayinadi }) match (b:Türler { YayinYeri: $yayinyeri }) create (a)-[:yayinlanir]->(b)",
                yayinadi=yayinadi, yayinyeri=yayinyeri)




        #ortak calisir ekle

        conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="123")
        sayi = conn.query("MATCH (n:Arastirmacilar)-[r:yayinyazari]->(a:Yayinlar) WHERE a.YayinAdi='%s' RETURN n.Soyad"%(yayinadi),
            db="neo4j")


        for i in range(len(sayi)):
            soyad= sayi[i]['n.Soyad']
            result11 = tx.run(
                "MATCH (n:Arastirmacilar)-[r:ortakcalisir]->(a:Arastirmacilar) WHERE n.Soyad= $ad AND a.Soyad =$soyad  RETURN COUNT(r) ",
                ad=ad,soyad=soyad)
            count6 = result11.single()[0]
            if(count6==0):
                tx.run("MATCH(a: Arastirmacilar), (b:Arastirmacilar)  WHERE a.Soyad= $ad AND b.Soyad =$soyad  CREATE(a) - [r: ortakcalisir]->(b)  CREATE(b) - [d: ortakcalisir]->(a)",ad=ad,soyad=soyad)






"""
result3 = tx.run("CREATE (b:Yayinlar) "
                        "SET b.TurId=$id2,b.YayinAdi=$yayinadi,b.YayinYili=$yayinyili "
                        "RETURN id(b)",
                        id2=id2, yayinadi=yayinadi, yayinyili=yayinyili)
"""




class TurEkle:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_greeting(self, yayinturu, yayinyeri):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, yayinturu, yayinyeri)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx,yayinturu, yayinyeri):
        result = tx.run("MATCH(a: Türler) where a.YayinTuru=$yayinturu and a.YayinYeri=$yayinyeri RETURN count(*) ", yayinturu=yayinturu, yayinyeri=yayinyeri)
        count = result.single()[0]

        if (count == 0):

            result2 = tx.run("CREATE (c:Türler) "
                        "SET c.YayinTuru=$yayinturu,c.YayinYeri=$yayinyeri "
                        "RETURN c.YayinTuru,c.YayinYeri + ', from node ' + id(c)",
                        yayinturu=yayinturu, yayinyeri=yayinyeri)




#CREATE CONSTRAINT ON (n:Arastirmacilar) ASSERT n.id IS UNIQUE


class YazarGetir:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_greeting(self):
        with self.driver.session() as session:
            aa=list()
            greeting = session.write_transaction(self._create_and_return_greeting)
            print(greeting)

            return greeting

    @staticmethod
    def _create_and_return_greeting(tx):
        sorgu=list(tx.run('MATCH (x:Arastirmacilar) RETURN x'))
        return [serialize_genre(record['x']) for record in sorgu]



def serialize_genre(x):
    print(x)
    liste=list()
    liste.append(x['Ad'])
    liste.append(x['Soyad'])
    return liste














if __name__ == '__main__':
    app.run()


