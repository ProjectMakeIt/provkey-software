import web
import json
import libs.config

urls = (
        '/config/(.*)', 'get_config',
        '/config','list_config',
        )

app = web.application(urls, globals())

class list_config:
    def GET(self):
        output = json.dumps(['config1','config2'])
        return output

class get_config:
    def GET(self,config):
        output = json.dumps({'test':config})
        return output

if __name__ == "__main__":
    app.run()
