# import requirements needed
import os

from flask import Flask, request, redirect, url_for, render_template, session
from utils import get_base_url
from aitextgen import aitextgen

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12360
base_url = get_base_url(port)

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')
    

ai_shakespeare = aitextgen(model_folder="model/trained_model_shakespeare", to_gpu=False)
ai_poe = aitextgen(model_folder="model/trained_model_poe", to_gpu=False)

app.secret_key = os.urandom(64)

# set up the routes and logic for the webserver
@app.route(f'{base_url}')
def home():
    return render_template('index.html')

@app.route(f'{base_url}/shakespeare')
def shakespeare():
    return render_template('shakespeare.html')

@app.route(f'{base_url}/poe')
def poe():
    return render_template('Poe.html')

@app.route(f'{base_url}/team')
def team():
    return render_template('team.html')

@app.route(f'{base_url}/results/')
def results():
    if 'data' in session:
        data = session['data']
        return render_template('shakespeare.html', generated=data)
    else:
        return render_template('shakespeare.html', generated=None)

@app.route(f'{base_url}/generate_text/', methods=["POST"])
def generate_text():
    """
    view function that will return json response for generated text. 
    """

    prompt = request.form['prompt']
    if prompt is not None:
        generated = ai_shakespeare.generate(
            n=1,
            batch_size=3,
            prompt=str(prompt),
            max_length=300,
            temperature=0.7,
            return_as_list=True
        )

    data = {'generated_ls': generated}
    session['data'] = generated[0]
    return redirect(url_for('results'))

# Define results_poe() and generate_text_poe()
@app.route(f'{base_url}/results_poe/')
def results_poe():
    if 'data' in session:
        data = session['data']
        return render_template('Poe.html', generated=data)
    else:
        return render_template('Poe.html', generated=None)

@app.route(f'{base_url}/generate_text_poe/', methods=["POST"])
def generate_text_poe():
    prompt = request.form['prompt']
    if prompt is not None:
        generated = ai_poe.generate(
            n=1,
            batch_size=3,
            prompt=str(prompt),
            max_length=300,
            temperature=0.7,
            return_as_list=True
        )

    data = {'generated_ls': generated}
    session['data'] = generated[0]
    return redirect(url_for('results_poe'))

# define additional routes here
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page

if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'cocalc8.ai-camp.dev/'
    
    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host = '0.0.0.0', port=port, debug=True)
