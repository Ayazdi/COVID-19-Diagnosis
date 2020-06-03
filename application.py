""" This module runs Flask"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from ct_scan_analyser import load_model, ct_scan_diagnosis


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = load_model('model_2')


def allowed_file(filename):
    """ check if an extension is valid """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/index')
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            prediction = ct_scan_diagnosis(file)

            return render_template('recommender.html',
                                   result_html=prediction)
    return render_template('index.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],

                               filename)

# @app.route('/')
# @app.route('/index')
# def hello_world():
#     return render_template('index.html')


@app.route('/recommender')
def recommender():
    user_input = dict(request.args)
    user_input_movies = list(user_input.values())[:-1]
    user_input_movies_fuzzed = []
    for movie in user_input_movies:
        # Search for the name of the movie in the database using tsvector
        movie_name_query = f"""SELECT title, "movieId",
                        ts_rank_cd(to_tsvector('english', movies.title), to_tsquery('''{movie}'':*'))
                        AS score
                        FROM movies
                        WHERE to_tsvector('english', movies.title) @@ to_tsquery('''{movie}'':*')
                        ORDER BY score DESC;"""
        result = PG.execute(movie_name_query).fetchall()[0][0]
        user_input_movies_fuzzed.append(result)

    user_input_ratings = [5] * len(user_input_movies_fuzzed)
    user_input = dict(zip(user_input_movies_fuzzed, user_input_ratings))

    if dict(request.args)['model'] == 'NMF':
        new_array = user_array(user_input, nmf=True)
        result_list = get_movies_nmf(new_array)

    if dict(request.args)['model'] == 'Cosim':
        new_array = user_array(user_input)
        result_list = get_movies_cosim(new_array)

    if dict(request.args)['model'] == 'Cosim Item':
        result_list = get_movies_cosim_item(user_input_movies_fuzzed)

    if dict(request.args)['model'] == 'Cosim Item Mix':
        result_list = get_movies_cosim_item_mix(user_input_movies_fuzzed)

    return render_template('recommender.html',
                           result_html=result_list,
                           user_input=user_input)
