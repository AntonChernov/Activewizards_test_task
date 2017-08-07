import tornado.ioloop
import os
import tornado.web
import motor.motor_tornado
import json
from bson import json_util
client = motor.motor_tornado.MotorClient()
db = client.testdb


class DataHandler(tornado.web.RequestHandler):

    async def sum_all_cost_to_country_and_projects(self, data_list=None, key_list=None):
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

    async def country_get(self):
        db = self.settings['db']
        data = db.world.find()
        data_list = []
        fillKeys = []
        [data_list.append(
            {
                'project_name': val['project_name'],
                'countryname': val['countryname'],
                'lendprojectcost': val['lendprojectcost'],
            }
        ) for val in await data.to_list(length=await data.count())]
        [fillKeys.append(i['countryname']) for i in data_list if i['countryname'] not in fillKeys]
        sorted_list = sorted(data_list, key=lambda k: k['countryname'])
        sorted_fillKeys = sorted(fillKeys)
        seri, dril = await self.sum_all_cost_to_country_and_projects(data_list=data_list, key_list=sorted_fillKeys)
        args = {'series_data': seri, 'dril_data': dril}
        self.write(json.dumps(args, default=json_util.default))

    async def get(self):
        await self.country_get()
        self.finish()


class MainHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.render('main_tornado.html')


settings = {
            "debug": True,
            "template_path": os.path.join(os.path.dirname(__file__), "templates"),
            "static_path": os.path.join(os.path.dirname(__file__), "static")
        }


application = tornado.web.Application([
        (r"/get_data", DataHandler),
        (r"/", MainHandler),
    ], db=db, **settings)
application.listen(8881)
tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    application()
