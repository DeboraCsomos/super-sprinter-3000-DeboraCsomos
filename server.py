from flask import Flask, render_template, redirect, request, session, url_for
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
    criteria = request.args.get("criteria")
    order = request.args.get("order")
    story_info = ordering(story_info, order, criteria)
    return render_template('list.html', story_info=story_info, order=order)


def ordering(story_info, order, criteria):
    if order == "descending" and criteria == "business_value":
        story_info = sorted(story_info, key=lambda x: x[4], reverse=True)
    elif order == "ascending" and criteria == "business_value":
        story_info = sorted(story_info, key=lambda x: x[4], reverse=False)
    else:
        story_info = sorted(story_info, key=lambda x: x[0], reverse=True)
    return story_info


@app.route('/story', methods=['GET', 'POST'])
def route_new():
    if request.method == 'POST':
        with open("user_stories.csv", "r", newline='') as csvfile:
            storyreader = csv.reader(csvfile, delimiter=",")
            story_info = []
            for row in storyreader:
                story_info.append(row)
        if story_info:
            story_id = int(story_info[-1][0]) + 1
        else:
            story_id = 1
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

        return redirect(url_for('route_index'))

    return render_template('form.html')


@app.route('/story/<story_id>', methods=['GET', 'POST'])
def route_edit(story_id):
    if request.method == 'POST':
        story_title = request.form.get("story title")
        story = request.form.get("user story")
        criteria = request.form.get("acceptance criteria")
        business_value = request.form.get("business value")
        estimation = request.form.get("estimation")
        status = request.form.get("status")
        edited_user_story = [story_id, story_title, story, criteria, business_value, estimation, status]
        with open("user_stories.csv", "r", newline='') as csvfile:
            storyreader = csv.reader(csvfile)
            stories = []
            for index, row in enumerate(storyreader):
                if story_id == row[0]:
                    stories.append(edited_user_story)
                else:
                    stories.append(row)
        with open("user_stories.csv", "w", newline='') as csvfile:
            storywriter = csv.writer(csvfile)
            storywriter.writerows(stories)

        return redirect(url_for('route_index'))
    if request.method == 'GET':
        with open("user_stories.csv", "r", newline='') as csvfile:
            storyreader = csv.reader(csvfile, delimiter=",")
            edit_story = []
            for row in storyreader:
                if row[0] == story_id:
                    edit_story = row
    return render_template("form.html", edit_story=edit_story, story_id=story_id)


@app.route('/story/delete/<story_id>', methods=['GET'])
def story_delete(story_id):
    with open("user_stories.csv", "r", newline='') as csvfile:
        storyreader = csv.reader(csvfile, delimiter=",")
        story_info = []
        for row in storyreader:
            if story_id == row[0]:
                continue
            else:
                story_info.append(row)
    with open("user_stories.csv", "w", newline='') as csvfile:
        storywriter = csv.writer(csvfile)
        storywriter.writerows(story_info)
    return redirect(url_for('route_index'))


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(
        debug=True,  # Allow verbose error reports
        # use_debugger=False,
        # use_reloader=False,
        port=5000  # Set custom port
    )
