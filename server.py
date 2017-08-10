from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)


@app.route('/')
def route_index():
    note_text = None
    if 'note' in session:
        note_text = session['note']
    return render_template('list.html', note=note_text)


@app.route('/story', methods=['POST'])
def route_edit():
    note_text = None
    if 'note' in session:
        note_text = session['note']
    return render_template('form.html', note=note_text)


@app.route('/story/<story_id>', methods=['POST'])
def route_save():
    print('POST request received!')
    session['note'] = request.form['note']
    return redirect('/')

if __name__ == "__main__":
    app.secret_key = 'some_secret_key_here'
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
