__author__ = 'harshit'

import tornado.ioloop
import tornado.web
import tornado.database

db = tornado.database.Connection(
    host="localhost", database="dms",
    user="root", password="root")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        files_uploaded = db.query("select name from file_handler")
        self.render('home_page.html',files_uploaded=files_uploaded)


class UploadHandler(tornado.web.RequestHandler):

    def post(self):
        file1 = self.request.files['file1'][0]
        original_fname = file1['filename']
        output_file = open("uploads/" + original_fname, 'w')
        output_file.write(file1['body'])
        db.execute_lastrowid("INSERT INTO file_handler(name) VALUES(%s)",original_fname)
        self.finish("file" + original_fname + " is uploaded")

settings = {
    "static_path": "/home/harshit/workspace/test_assignment/uploads/",
    }

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/upload",UploadHandler),
],**settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
