from flask import Flask, render_template, redirect, request, session
import csv
import os


app = Flask(__name__)


@app.route('/')
def route_index():
    with open("user_stories.csv", "r", newline='') as csvfile:
        storyreader = csv.reader(csvfile, delimiter=",")
        story_info = []
        for row in storyreader:
            story_info.append(row)

    return render_template('list.html', story_info=story_info)


@app.route('/story', methods=['GET', 'POST'])
def route_new():
    if request.method == 'POST':
        with open("user_stories.csv", "r", newline='') as csvfile:
            storyreader = csv.reader(csvfile, delimiter=",")
            story_info = []
            for row in storyreader:
                story_info.append(row)
        story_id = int(story_info[-1][0]) + 1
        story_title = request.form.get("story title")
        story = request.form.get("user story")
        criteria = request.form.get("acceptance criteria")
        business_value = request.form.get("business value")
        estimation = request.form.get("estimation")
        status = request.form.get("status")
        user_story = [story_id, story_title, story, criteria, business_value, estimation, status]
        with open("user_stories.csv", "a", newline='') as csvfile:
            storywriter = csv.writer(csvfile)
            storywriter.writerow(user_story)
 
        return redirect('/')

    return render_template('form.html')


@app.route('/story/<story_id>', methods=['GET'])
def route_edit(story_id):
    with open("user_stories.csv", "r", newline='') as csvfile:
        storyreader = csv.reader(csvfile, delimiter=",")
        edit_story = []
        for row in storyreader:
            if row[0] == story_id:
                edit_story = row
    return render_template("form.html", edit_story=edit_story)


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(
        debug=True,  # Allow verbose error reports
        # use_debugger=False,
        # use_reloader=False,  
        port=5000  # Set custom port
    )

