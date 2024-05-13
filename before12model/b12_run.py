from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
import os
from flask import Blueprint
from b12_youtube_methods import recommend_yts
from b12_youtube_methods import get_recent_yts
from b12_youtube_methods import get_personalized_yt_recommendations
from b12_youtube_methods import search_yts
from b12_youtube_methods import getYt
from b12_books_methods import recommend_books
from b12_books_methods import search_books
from b12_books_methods import getBook
from b12_websites_methods import recommend_websites
from b12_websites_methods import search_websites

# Define a blueprint for searchyts model
searchyts_bp = Blueprint('searchyts', __name__)

app = Flask(__name__)

@app.route('/')
def b12_homepage():
    recent_yts = get_recent_yts()
    personalized_yt_recommendations = get_personalized_yt_recommendations("Vishwa")
    trending_books = recommend_books("English")
    recommended_websites = recommend_websites("Real Number")
    return render_template('b12_homepage.html', recent_yts_list=recent_yts, trending_books_list=trending_books,
                           personalized_yt_recommendations_list=personalized_yt_recommendations, 
                           recommended_websites_list=recommended_websites)

@app.route('/b12_ytsearchpage')
def b12_ytsearchpage():
    recent_yts = get_recent_yts()
    personalized_yt_recommendations = get_personalized_yt_recommendations("Vishwa")
    real_numbers_yts = recommend_yts("Real Numbers")
    ecology_yts = recommend_yts("Ecology")
    electricity_yts = recommend_yts("Electricity")
    return render_template('b12_ytsearchpage.html', recent_yts_list=recent_yts,
                           personalized_yt_recommendations_list=personalized_yt_recommendations,
                           real_numbers_yts_list=real_numbers_yts, ecology_yts_list=ecology_yts,
                           electricity_yts_list=electricity_yts)

@app.route('/b12_booksearchpage')
def b12_booksearchpage():
    sapna_store_books = recommend_books("Sapna Store")
    english_books = recommend_books("English")
    hindi_books = recommend_books("Hindi")
    kannada_books = recommend_books("Kannada")
    return render_template('b12_booksearchpage.html', sapna_store_books_list = sapna_store_books, english_books_list = english_books,
                           hindi_books_list = hindi_books, kannada_books_list = kannada_books)

@app.route('/b12_websearchpage')
def b12_websearchpage():
    byjus_websites = recommend_websites("byjus")
    vedantu_websites = recommend_websites("Vedantu")
    physics_wallah_websites = recommend_websites("Physics Wallah")
    gfg_websites = recommend_websites("GeeksforGeeks")
    return render_template('b12_websearchpage.html',byjus_websites_list = byjus_websites, vedantu_websites_list = vedantu_websites,
                           physics_wallah_websites_list = physics_wallah_websites, gfg_websites_list = gfg_websites)

@app.route('/b12_searchresults', methods=['GET'])
def b12_searchresults():
    if request.method == 'GET':
        pageid = request.args.get('pageid')
        keyword = request.args.get('keyword')
        if pageid == '1':
            result_yts = search_yts(keyword)
            results = result_yts
        elif pageid == '2':
            result_books = search_books(keyword)
            results = result_books
        elif pageid == '3':
            result_websites = search_websites(keyword)
            results = result_websites

        return render_template('b12_searchresults.html', pageid=pageid, keyword=keyword, results_list=results)

    return render_template('b12_searchresults.html')

@app.route('/b12_ytdetailspage/<title>', methods=['GET'])
def b12_ytdetailspage(title):
    youtube = getYt(title)
    similar_yts = recommend_yts(title)
    similar_books = recommend_books(title)
    similar_websites = recommend_websites(title)
    return render_template('b12_ytdetailspage.html', youtube=youtube, similar_yts_list=similar_yts,
                           similar_books_list=similar_books, similar_websites_list=similar_websites)

@app.route('/b12_bookdetailspage/<title>', methods=['GET'])
def b12_bookdetailspage(title):
    book = getBook(title)
    similar_books = recommend_books(title)
    similar_websites = recommend_websites(title)
    return render_template('b12_bookdetailspage.html', book=book, similar_books_list=similar_books,
                           similar_websites_list=similar_websites)

@app.route('/b12_homepagesearchresults', methods=['GET'])
def b12_homepagesearchresults():
    if request.method == 'GET':
        keyword = request.args.get('keyword')
        home_result_yts = search_yts(keyword)
        home_result_books = search_books(keyword)
        home_result_webs = search_websites(keyword)
        return render_template('b12_homepagesearchresults.html', keyword=keyword, home_result_yts_list=home_result_yts,
                            home_result_books_list=home_result_books, home_result_webs_list=home_result_webs)
    
    return render_template('b12_homepagesearchresults.html')

if __name__ == '__main__':
    app.run(debug=True)










