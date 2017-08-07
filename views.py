from flask import Flask, jsonify, render_template, url_for
from pymongo import MongoClient
app = Flask(__name__)
client = MongoClient()
db = client.testdb


@app.route('/get_data', methods=['GET'])
def get_collection():
    data = db.world.find()
    data_list = []
    fillKeys = []
    [data_list.append(
        {
            'project_name': val['project_name'],
            'countryname': val['countryname'],
            'lendprojectcost': val['lendprojectcost'],
        }
    ) for val in data]
    [fillKeys.append(i['countryname']) for i in data_list if i['countryname'] not in fillKeys]
    sorted_list = sorted(data_list, key=lambda k: k['countryname'])
    sorted_fillKeys = sorted(fillKeys)
    # ads = list(filter(lambda k: k['countryname'] == sorted_fillKeys[0], data_list))
    seri, dril = sum_all_cost_to_country_and_projects(data_list=data_list, key_list=sorted_fillKeys)
    # args = {'data_list': sorted_list, 'fillKeys': sorted_fillKeys}
    args = {'series_data': seri, 'dril_data': dril}
    return jsonify(args)


@app.route('/', methods=['GET'])
def get_main_page():
    args = {}
    args['jquery'] = url_for('static', filename='jquery-3.2.1.min.js')
    args['hc'] = url_for('static', filename='highcharts.js')
    args['dd'] = url_for('static', filename='drilldown.js')
    args['main'] = url_for('static', filename='main.js')
    return render_template('main.html', data=args)


def sum_all_cost_to_country_and_projects(data_list=None, key_list=None):
    series_final_data = []
    drilldown_series_obj = []
    for i in key_list:
        list_of_cost = []
        series_data = []
        for j in list(filter(lambda k: k['countryname'] == i, data_list)):
            list_of_cost.append(int(j['lendprojectcost']))
            series_data.append([str(j['project_name']), int(j['lendprojectcost'])])
        drilldown_series_obj.append({'name': str(i), 'id': str(i), 'data': series_data})
        series_final_data.append({'name': i, 'y': sum(list_of_cost), 'drilldown': i})
    return series_final_data, drilldown_series_obj


if __name__ == '__main__':
    app.run()