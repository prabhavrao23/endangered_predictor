import pandas as pd
from flask import render_template, Blueprint

info_blueprint = Blueprint('info', __name__)


def getMappedName(name):
    mappedName = {'africanelephant': 'Elephant(African)',
                  'asianelephant': 'Elephant(Asian)',
                  'panda': 'Panda',
                  'arcticfox': 'Arctic Fox',
                  'chimpanzee': 'Chimpanzee',
                  'jaguars': 'Jaguars',
                  'lion': 'Lion',
                  'panther': 'Panther',
                  'blackrhino': 'Rhino(Black)',
                  'whiterhino': 'Rhino(White)',
                  'rhino': 'Rhino(Greater One-Horned Rhino)',
                  'javanrhino': 'Rhino(Javan)',
                  'sumatranrhino': 'Rhino(Sumatran)'
                  }
    return mappedName.get(name)


def map_from(baseObj, obj):
    for k, v in obj.items():
        baseObj[k] = v if k == 'Animal_Name' else v.lower()


def map_to_dict(basic_info, fact, rem_steps):
    base = list(basic_info.values())[0]
    fact = list(fact.values())[0]
    steps = list(rem_steps.values())[0]
    map_from(base, fact)
    map_from(base, steps)
    animal_info = {}
    for k, v in base.items():
        animal_info[k.replace("_", " ")] = v
    return animal_info


def get_all_details_for(animal_name):
    df = basic_details()
    basic_info = df[df['Animal_Name'] == animal_name].T.to_dict()

    af = affecting_factors()
    factors = af[af['Animal_Name'] == animal_name].T.to_dict()

    rm = remediation()
    steps = rm[rm['Animal_Name'] == animal_name].T.to_dict()
    return map_to_dict(basic_info, factors, steps)


def basic_details():
    return pd.read_csv('../../data/Animal.csv')


def affecting_factors():
    return pd.read_csv('../../data/Effecting_Factor.csv').drop(columns=['Country'])


def endangered_status():
    return pd.read_csv('../../data/Endangered_Species.csv').drop(columns=['Year', 'Extinction_Rate', 'Continent'])


def remediation():
    return pd.read_csv('../../data/Remediation_measures.csv').drop(columns=['Country', 'Effect_of_Measures'])


@info_blueprint.route("/info/")
def info():
    title = "Details of Mammals under threat..."
    df = basic_details()
    return render_template("base.html", title=title, tables=[df.to_html(classes='data', header="true")],
                           titles=df.columns.values)


@info_blueprint.route("/factors")
def factors():
    title = "Factors affecting of existence of Mammals..."
    df = affecting_factors()
    return render_template("base.html", title=title, tables=[df.to_html(classes='data', header="true")],
                           titles=df.columns.values, )


@info_blueprint.route("/status")
def status():
    title = "Endangered Status of Mammals..."
    df = endangered_status()
    return render_template("base.html", title=title, tables=[df.to_html(classes='data', header="true")],
                           titles=df.columns.values)


@info_blueprint.route("/remediation")
def remediation_steps():
    title = "Remediation steps taken to protect these mammals..."
    df = remediation()
    return render_template("base.html", title=title, tables=[df.to_html(classes='data', header='true')],
                           titles=df.columns.values)