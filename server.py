from flask import Flask, render_template, request, send_file, redirect
import bcrypt
import json
import urllib.request

current_pass = bytes(open('password.txt').read(), 'utf-8')


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/style/<filename>")
def get_style(filename):
    return send_file(f'styles/{filename}')

@app.route("/assets/<filename>")
def get_assets(filename):
    return send_file(f'assets/{filename}')


@app.route("/script/<filename>")
def get_script(filename):
    return send_file(f'scripts/{filename}')

@app.route("/projects")
def get_projects():
    return send_file('projects.json')

@app.route("/projecticons/<filename>")
def get_project_icon(filename):
    return send_file(f'projects/{filename}')


@app.route("/add/<password>", methods=['POST', 'GET'])
def add_project(password):
    if bcrypt.hashpw(bytes(password, 'utf-8'), b'$2b$12$3whq2NeGvsWq7CtNcWWhB.') == current_pass:
        if request.method == 'POST':
            print(request.files)
            print(request.form["name"])
            name = request.form['name']
            icon = request.form['icon']
            link = request.form['link']
            description = request.form['description']
            urllib.request.urlretrieve(icon, 'projects/'+name.replace(" ","_")+'.png')
            projects = open('projects.json').read()
            projects = json.loads(projects)
            projects.append({
                "Name": name,
                "Icon": "/projecticons/"+name.replace(" ","_")+".png",
                "Link": link,
                "ProjectDescription": description
            })
            projects = str(projects).replace("\\'","'").replace("\"","\\\"").replace("'", '"')
            with open('projects.json', 'w') as f:
                f.write(projects)
            return render_template('addproject.html', password=password)
        else:
            return render_template('addproject.html', password=password)
    else:
        return render_template('imateapot.html', reason="enter correct password"), 418


@app.route("/changepassword/<password>", methods=['POST', 'GET'])
def change_password(password):
    global current_pass
    if bcrypt.hashpw(bytes(password, 'utf-8'), b'$2b$12$3whq2NeGvsWq7CtNcWWhB.') == current_pass:
        if request.method == 'POST':
            new_password = request.form['newpassword']
            with open('password.txt', 'w') as f:
                f.write(str(bcrypt.hashpw(bytes(new_password, 'utf-8'), b'$2b$12$3whq2NeGvsWq7CtNcWWhB.')))
            current_pass = bcrypt.hashpw(bytes(new_password, 'utf-8'), b'$2b$12$3whq2NeGvsWq7CtNcWWhB.')
            return redirect("/")
        else:
            return render_template('changepassword.html', password=password)
    else:
        return render_template('imateapot.html', reason="enter correct password"), 418

@app.route("/deleteproject/<password>", methods=['POST', 'GET'])
def delete_project(password):
    if bcrypt.hashpw(bytes(password, 'utf-8'), b'$2b$12$3whq2NeGvsWq7CtNcWWhB.') == current_pass:
        if request.method == 'POST':
            name = request.form['name']
            projects = open('projects.json').read()
            projects = json.loads(projects)
            projects = [project for project in projects if project['Name'] != name]
            projects = str(projects).replace("\\'","'").replace("\"","\\\"").replace("'", '"')
            with open('projects.json', 'w') as f:
                f.write(projects)
            return redirect("/")
        else:
            return render_template('deleteproject.html', password=password , data = "\n".join([project['Name'] for project in json.loads(open('projects.json').read())]))
    else:
        return render_template('imateapot.html', reason="enter correct password"), 418

@app.route("/api")
def api():
    return render_template('api.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('imateapot.html', reason="no u"), 418