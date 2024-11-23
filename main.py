from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('main.html')


# Logic untuk form usia
@app.route('/usia', methods=['GET','POST'])
def cek_usia():
    if request.method == "POST":
        tahun_lahir = int(request.form["usia"])
        tahun_sekarang = 2024
        usia = tahun_sekarang - tahun_lahir
        return render_template("form.html", usia =usia)
    return render_template("form.html", usia=None)