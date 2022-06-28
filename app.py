import csv
from datetime import datetime
from flask import render_template, url_for, request, redirect
from models import db, Project, app


@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)


@app.route('/project/new', methods=['GET', 'POST'])
def add_project():
    projects = Project.query.all()
    if request.form:
        # TODO: Clean Data (if necessary)
        print(request.form['date'])
        title = request.form['title']
        date = convert_picker_to_date(request.form['date'])
        description = request.form['desc']
        skills_practiced = request.form['skills']
        github_url = request.form['github']
        new_project = Project(title=title, date=date, description=description,
                              skills_practiced=skills_practiced, github_url=github_url)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('addproject.html', projects=projects)


@app.route('/project/<project_id>')
def project(project_id):
    projects = Project.query.all()
    project_in_db = Project.query.get_or_404(project_id)
    skills = project_in_db.skills_practiced.split(',')
    date = display_date(project_in_db.date)
    return render_template('detail.html', project=project_in_db, projects=projects, skills=skills, date=date)


@app.route('/project/<project_id>/edit', methods=['GET', 'POST'])
def edit_project(project_id):
    projects = Project.query.all()
    project_in_db = Project.query.get_or_404(project_id)
    date = convert_date_to_picker(project_in_db.date)
    if request.form:
        project_in_db.title = request.form['title']
        project_in_db.date = convert_picker_to_date(request.form['date'])
        project_in_db.description = request.form['desc']
        project_in_db.skills_practiced = request.form['skills']
        project_in_db.github_url = request.form['github']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editproject.html', project=project_in_db, projects=projects, date=date)


@app.route('/project/<project_id>/delete')
def delete_project(project_id):
    project_in_db = Project.query.get_or_404(project_id)
    db.session.delete(project_in_db)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/about')
def about():
    projects = Project.query.all()
    return render_template('about.html', projects=projects)


@app.errorhandler(404)
def not_found(error):
    projects = Project.query.all()
    return render_template('404.html', msg=error, projects=projects), 404


def convert_picker_to_date(date_str):
    date_split = date_str.split('-')
    year = int(date_split[0])
    month = int(date_split[1])
    date = datetime(year, month, 1)
    return date


def convert_date_to_picker(date):
    converted_date = date.strftime("%Y-%m")
    return converted_date


def display_date(date):
    converted_date = date.strftime("%B %Y")
    return converted_date


def add_csv():
    """
        Add projects from csv to database
        if they aren't in the DB already
        """
    with open('treehouse-projects.csv') as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            title = row['title']
            date = datetime.strptime(row['date'], '%m/%d/%Y').date()
            description = row['description']
            skills_practiced = row['skills_practiced']
            github_url = row['github_url']
            project_in_db = db.session.query(Project).filter(Project.title == row['title']).one_or_none()
            if project_in_db == None:
                new_project = Project(title=title, date=date, description=description,
                                      skills_practiced=skills_practiced, github_url=github_url)
                db.session.add(new_project)
    db.session.commit()


if __name__ == '__main__':
    db.create_all()
    add_csv()
    app.run(debug=True, port=8000, host='127.0.0.1')
