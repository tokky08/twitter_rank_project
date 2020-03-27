from rq import Queue
from worker import conn
from bottle import route, run
from app import views


q = Queue(connection=conn)

@route('/index')
def index():
    result = q.enqueue(background_process, '引数１')
    return result

def background_process(request):
    # ここに時間のかかる処理を書く
    views.info_get(request)
    


run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))