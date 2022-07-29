from flask import Flask, request
import sys

import pip
from banking.util.util import read_yaml_file, write_yaml_file
from matplotlib.style import context
from banking.logger import logging
from banking.exception import BankingException
import os, sys
import json
from banking.config.configuration import Configuartion
from banking.constant import CONFIG_DIR, get_current_time_stamp
from banking.pipeline.pipeline import Pipeline
from banking.entity.banking_predictor import BankingPredictor, BankingData
from flask import send_file, abort, render_template

ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "logs"
PIPELINE_FOLDER_NAME = "banking"
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, "model.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)


from banking.logger import get_log_dataframe

BANKING_DATA_KEY = "banking_data"
CREDIT_RISK_KEY = "credit_risk"


app = Flask(__name__)


@app.route('/artifact', defaults={'req_path': 'banking'})
@app.route('/artifact/<path:req_path>')
def render_artifact_dir(req_path):
    os.makedirs("banking", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        if ".html" in abs_path:
            with open(abs_path, "r", encoding="utf-8") as file:
                content = ''
                for line in file.readlines():
                    content = f"{content}{line}"
                return content
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file_name): file_name for file_name in os.listdir(abs_path) if
             "artifact" in os.path.join(abs_path, file_name)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('files.html', result=result)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)


@app.route('/view_experiment_hist', methods=['GET', 'POST'])
def view_experiment_history():
    experiment_df = Pipeline.get_experiments_status()
    context = {
        "experiment": experiment_df.to_html(classes='table table-striped col-12')
    }
    return render_template('experiment_history.html', context=context)


@app.route('/train', methods=['GET', 'POST'])
def train():
    message = ""
    pipeline = Pipeline(config=Configuartion(current_time_stamp=get_current_time_stamp()))
    if not Pipeline.experiment.running_status:
        message = "Training started."
        pipeline.start()
    else:
        message = "Training is already in progress."
    context = {
        "experiment": pipeline.get_experiments_status().to_html(classes='table table-striped col-12'),
        "message": message
    }
    return render_template('train.html', context=context)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    context = {
        BANKING_DATA_KEY: None,
        CREDIT_RISK_KEY: None
    }

    if request.method == 'POST':
        status = int(request.form['status'])
        duration = int(request.form['duration'])
        credit_history = int(request.form['credit_history'])
        purpose = int(request.form['purpose'])
        amount = int(request.form['amount'])
        savings = int(request.form['savings'])
        employment_duration = int(request.form['employment_duration'])
        installment_rate = int(request.form['installment_rate'])
        personal_status_sex = int(request.form['personal_status_sex'])
        other_debtors = int(request.form['other_debtors'])
        present_residence = int(request.form['present_residence'])
        property = int(request.form['property'])
        age = int(request.form['age'])
        other_installment_plans = int(request.form['other_installment_plans'])
        housing = int(request.form['housing'])
        number_credits = int(request.form['number_credits'])
        job = int(request.form['job'])
        people_liable = int(request.form['people_liable'])
        telephone = int(request.form['telephone'])
        foreign_worker = int(request.form['foreign_worker'])
        

        banking_data = BankingData(status=status,
                                   duration=duration,
                                   credit_history=credit_history,
                                   purpose=purpose,
                                   amount=amount,
                                   savings=savings,
                                   employment_duration=employment_duration,
                                   installment_rate=installment_rate,
                                   personal_status_sex=personal_status_sex,
                                   other_debtors=other_debtors,
                                   present_residence=present_residence,
                                   property=property,
                                   age=age,
                                   other_installment_plans=other_installment_plans,
                                   housing=housing,
                                   number_credits=number_credits,
                                   job=job,
                                   people_liable=people_liable,
                                   telephone=telephone,
                                   foreign_worker=foreign_worker
                                   )
        banking_df = banking_data.get_banking_input_data_frame()
        banking_predictor = BankingPredictor(model_dir=MODEL_DIR)
        credit_risk = banking_predictor.predict(X=banking_df)
        context = {
            BANKING_DATA_KEY: banking_data.get_banking_data_as_dict(),
            CREDIT_RISK_KEY: credit_risk,
        }
        return render_template('predict.html', context=context)
    return render_template("predict.html", context=context)


@app.route('/saved_models', defaults={'req_path': 'saved_models'})
@app.route('/saved_models/<path:req_path>')
def saved_models_dir(req_path):
    os.makedirs("saved_models", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('saved_models_files.html', result=result)


@app.route("/update_model_config", methods=['GET', 'POST'])
def update_model_config():
    try:
        if request.method == 'POST':
            model_config = request.form['new_model_config']
            model_config = model_config.replace("'", '"')
            print(model_config)
            model_config = json.loads(model_config)

            write_yaml_file(file_path=MODEL_CONFIG_FILE_PATH, data=model_config)

        model_config = read_yaml_file(file_path=MODEL_CONFIG_FILE_PATH)
        return render_template('update_model.html', result={"model_config": model_config})

    except  Exception as e:
        logging.exception(e)
        return str(e)


@app.route(f'/logs', defaults={'req_path': f'{LOG_FOLDER_NAME}'})
@app.route(f'/{LOG_FOLDER_NAME}/<path:req_path>')
def render_log_dir(req_path):
    os.makedirs(LOG_FOLDER_NAME, exist_ok=True)
    # Joining the base and the requested path
    logging.info(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        log_df = get_log_dataframe(abs_path)
        context = {"log": log_df.to_html(classes="table-striped", index=False)}
        return render_template('log.html', context=context)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('log_files.html', result=result)


if __name__ == "__main__":
    app.run()