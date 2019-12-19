import json
from flask import render_template, request, make_response
from models import Survey, Observation, DB_url, app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from statistics import mode, median, StatisticsError

engine = create_engine(DB_url, connect_args={'check_same_thread': False}, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


@app.route("/")
def survey():
    survey_data = session.query(Survey).all()
    observation_data = session.query(Observation).all()
    return make_response(render_template('index.html', survey=survey_data, observation=observation_data))


@app.route("/survey/", methods=["POST"])
def addsurvey():
    if request.method == 'POST':
        name = request.get_json().get('name')
        session.add(Survey(name = name))
        output = "Record Added"
    session.commit()
    return make_response(output)


@app.route("/survey/<id>/", methods=["DELETE"])
def removesurvey(id):
    if request.method == 'DELETE':
        session.query(Survey).filter(Survey.id == id).delete()
        output = "Record Deleted"
    session.commit()
    return make_response(output)


@app.route("/stat/<stat_id>/", methods=["GET","PUT", "POST", "DELETE"])
def stat(stat_id):
    if request.method == "GET":
        records = session.query(Observation).filter(Observation.survey_id == stat_id)
        result = []
        for record in records:
            data = {
                "id": record.id,
                "survey_id": record.survey_id,
                "value": record.value,
                "frequency": record.frequency
            }
            result.append(data)
        return make_response(json.dumps(result))
    if request.method == 'PUT' or request.method == "POST":
        value = request.get_json().get('value')
        frequency = request.get_json().get('frequency')
        record = session.query(Observation).filter(Observation.id == stat_id)
        if record:
            record.update({Observation.value: value, Observation.frequency: frequency})
            output = "Record Updated for Observation: %s" % stat_id
        else:
            session.add(Observation(value=value, id=stat_id, frequency=frequency))
            output = "Record Added for %s" % stat_id
            session.commit()
        return make_response(output)
    elif request.method == 'DELETE':
        session.query(Observation).filter(Observation.id == stat_id).delete()
        output = "Record Deleted for Observation: %s" % stat_id
        session.commit()
        return make_response(output)


@app.route('/results', methods=['GET'])
def results():
    id = request.args.get('id')
    survey = session.query(Survey).filter(Survey.id == id).first()
    if survey:
        records = session.query(Observation).filter(Observation.survey_id == id)
        if records.count() > 0:
            lst = [record.frequency for record in records]
            mean_lst = [record.value * record.frequency for record in records]
            master_median_lst = []
            for record in records:
                median_lst = [record.value]
                count_lst = median_lst * record.frequency
                master_median_lst = master_median_lst + count_lst
            count = sum(lst)  # sum of all frequencies of a survey id
            mean_val = sum(mean_lst) / count
            try:
                median_val = median(master_median_lst)
                mode_val = mode(master_median_lst)
            except StatisticsError:
                mode_val = "No unique Mode."
            return make_response(render_template('results.html',survey=survey.name, count=count, mean=mean_val, mode=mode_val,
                                   median=median_val))
        else:
            return make_response(render_template('results.html', survey="No Observations for this survey", count='NA', mean='NA', mode='NA',
                                median='NA'))
    else:
        return make_response(render_template('results.html', survey="No survey available", count='NA', mean='NA', mode='NA',
                               median='NA'))


if __name__ == "__main__":
    app.run(debug=True)

