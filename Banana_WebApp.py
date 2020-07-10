from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import Markets_Taipei_Chart as Taipei
import Markets_NTaipei_Chart as NTaipei
import Markets_Taichung_Chart as Taichung
import Markets_Kaohsiung_Chart as Kaohsiung
from get_news import fetch_db_newest

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def my_web_app():
    return render_template('banana_index.html', page=1)


@app.route('/taipei')
def taipei():
    Taipei.taipei_page()
    return render_template('taipei.html', page=2)


@app.route('/new_taipei')
def new_taipei():
    NTaipei.ntaipei_page()
    return render_template('new_taipei.html', page=3)


@app.route('/taichung')
def taichung():
    Taichung.taichung_page()
    return render_template('taichung.html', page=4)


@app.route('/kaohsiung')
def kaohsiung():
    Kaohsiung.kaohsiung_page()
    return render_template('kaohsiung.html', page=5)



@app.route('/banana_report')
def banana_report():
    return render_template('banana_report.html')



@app.route('/banana_news')
def banana_news():
    news_dict = fetch_db_newest()
    return render_template('banana_news.html', news = news_dict)


if __name__ == '__main__':
    app.run()
