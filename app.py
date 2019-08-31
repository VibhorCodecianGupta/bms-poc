from flask import Flask, request, Response, json, render_template, redirect
from master import save_user, get_steps, enqueue_job, success_q_to_res, signup, login_helper

app = Flask(__name__)

# routes
@app.route('/', methods=['GET'])
def welcome():
    try:
        return render_template('landing.html')
    except Exception as e:
        return render_template('error.html', error = str(e))


@app.route('/signup', methods=['GET','POST'])
def register():
    try:
        if request.method == 'GET':
            return render_template('signup.html', request = request)
        elif request.method == 'POST':
            r = request.form
            name, e_id, role = r['name'], r['e_id'], r['role']
            result = signup(name, e_id, role)
            if result is not 'success':
                raise Exception('Cant register user: ' + str(result))
            return render_template('login.html', request = request)
    except Exception as e:
        return render_template('error.html', error = str(e))


@app.route('/login', methods=['GET','POST'])
def login():
    try:
        if request.method == 'GET':
            return render_template('login.html', request = request)
        elif request.method == 'POST':
            r = request.form
            name, e_id, role = r['name'], r['e_id'], r['role']
            token = login_helper(name, e_id)
            if token is not 'success_token':
                raise Exception('User not registered: ' + str(token))
            return render_template('dashboard.html', user = {'name': name, 'role': role})
    except Exception as e:
        return render_template('error.html', error = str(e))


@app.route('/logout', methods=['GET'])
def logout():
    try:
        return redirect('http://localhost:5000/login', code=302)
    except Exception as e:
        return render_template('error.html', error = str(e))


@app.route('/fn/<string:uid>', methods=['POST'])
def handle_fn(uid):
    try:
        r = request.get_json()
        status = save_user(uid, r['purpose'], r['priority'])
        if status is not 'success':
            raise Exception('User not saved')
        steps = get_steps(r['purpose'])
        return Response(response=json.dumps(steps), status=200)
    except Exception as e:
        return Response('{"error":"' + str(e) + '"}', status=400)


@app.route('/done/<string:uid>', methods=['POST'])
def handle_done(uid):
    try:
        r = request.get_json()
        user = User(uid, r['purpose'], r['priority'])
        enqueue_job(user)
        result = success_q_to_res(uid)
        if not result:
            raise Exception('No response from logic')
        return Response(response=json.dumos(result), status=200)
    except Exception as e:
        return Response('{"error":"' + str(e) + '"}', status=400)


# serve app
if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)