from flask import Flask, render_template, request, redirect,url_for
from db import init_db

app = Flask(__name__)
mysql = init_db(app)

@app.route("/")
def hello_world():
    return render_template('main.html')


# Route untuk form usia
@app.route('/usia', methods=['POST'])
def cek_usia():
    if request.method == "POST":
        tahun_lahir = int(request.form["usia"])
        tahun_sekarang = 2024
        usia = tahun_sekarang - tahun_lahir
        return render_template("form.html", usia =usia)
    return render_template("form.html", usia=None)

# Route untuk get data
@app.route("/get")
def get_data():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM tbl_barang")
    items = cursor.fetchall()
    cursor.close()
    return render_template("show_data.html", items=items)

# Route untuk update data
@app.route("/update/<id>", methods=['GET','POST'])
def update_user(id):
    cursor = mysql.connection.cursor()
    if request.method == "POST":
        nama_barang = request.form['nama_barang']
        harga_barang = request.form['harga_barang']
        stok_barang = request.form['stok_barang']
        sql = "update tbl_barang set nama_barang= %s, harga_barang= %s, stok_barang=%s where id = %s"
        cursor.execute(sql, (nama_barang,harga_barang,stok_barang, id))
        mysql.connection.commit()
        return redirect(url_for("get_data"))
    else:
        cursor.execute("select * from tbl_barang where id = %s", [id])
        data = cursor.fetchone()
        return render_template("edit.html", user=data)

# Route untuk delete data berdasarkan id
@app.route("/delete/<id>", methods=['POST'])
def delete_data(id):
    cursor = mysql.connection.cursor()
    try:
        sql = "delete from tbl_barang where id = %s"
        cursor.execute(sql, [id])
        print("Data berhasil dihapus")
        mysql.connection.commit()
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    return redirect(url_for('get_data'))

# Route untuk menambahkan item
@app.route("/add", methods=['GET','POST'])
def tambah_item():
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        kode_barang = request.form['kode_barang']
        nama_barang = request.form['nama_barang']
        harga_barang = request.form['harga_barang']
        stok_barang = request.form['stok_barang']
        
        sql = "insert into tbl_barang (kode_barang, nama_barang, harga_barang, stok_barang) values (%s, %s,%s,%s)"
        cursor.execute(sql,(kode_barang,nama_barang,harga_barang,stok_barang))
        mysql.connection.commit()
        print("item berhasil ditambah")
        return redirect(url_for("get_data"))
    else:
        return render_template("add.html")

if __name__ == '__main__' :
    app.run(debug=True)