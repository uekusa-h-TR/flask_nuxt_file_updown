"""Simple Flask server for File Download server

flaskを使った単純なファイルアップロードとダウンロードのためのサーバ
"""
from flask import Flask, make_response, request
from flask_cors import cross_origin
from werkzeug import Response
app = Flask(__name__)


@app.after_request
def after_request(response: Response):
    response.headers.add('Access-Control-Expose-Headers',
                         'Content-Disposition')
    return response


@app.route("/rtnfile", methods=["POST"])
@cross_origin()
def rtnfile():
    """POSTでアップロードされた画像ファイルをそのままダウンロードさせる

    Returns:
        Response(): ダウンロードさせる写真の情報が入ったレスポンスオブジェクト
    """
    res: Response = make_response()
    res.data = request.files["file"].stream.read()
    res.headers["Content-Disposition"] = "attachment; filename=\"{}\"".format(
        request.files["file"].filename)
    res.mimetype = request.files["file"].mimetype
    return res


@app.route("/rtnfile64", methods=["POST"])
@cross_origin()
def rtnfile64():
    """POSTでアップロードされた画像ファイルをそのままダウンロードするAPIでアップロードをbase64エンコードで持ってくるバージョン
    ここはどんな感じで表示されるのだろう
    Return:
        Response(): ダウンロードしてさせる写真の情報が入ったレスポンスオブジェクト
    """
    downloadData: dict[str, str] = {
        "contentData": request.json["contentData"],
    }
    res: Response = make_response(downloadData)
    res.headers["Content-Disposition"] = "attachment; filename=\"{}\"".format(
        request.json["fileName"])
    return res


if __name__ == "__main__":
    app.run(host="localhost", port=3001, debug=True)
