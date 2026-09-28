from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "clave-secreta"
DB = "drogueria.db"


def login_required(view_func):
    def wrapped(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Debes iniciar sesión para continuar", "error")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    wrapped.__name__ = view_func.__name__
    return wrapped


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0)""")
        db.execute("""CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL)""")
        if db.execute("SELECT COUNT(*) FROM producto").fetchone()[0] == 0:
            db.execute("INSERT INTO producto (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)",
                       ("Acetaminofén 500mg", "Analgésicos", 2500, 100))
        if db.execute("SELECT COUNT(*) FROM usuario").fetchone()[0] == 0:
            db.execute(
                "INSERT INTO usuario (nombre, correo, contrasena) VALUES (?, ?, ?)",
                ("Administrador", "admin@drogueria.com", generate_password_hash("admin123"))
            )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form.get("correo", "").strip().lower()
        contrasena = request.form.get("contrasena", "")

        with get_db() as db:
            usuario = db.execute("SELECT * FROM usuario WHERE correo = ?", (correo,)).fetchone()

        if usuario and check_password_hash(usuario["contrasena"], contrasena):
            session["usuario_id"] = usuario["id"]
            session["usuario_nombre"] = usuario["nombre"]
            flash("Inicio de sesión correcto", "ok")
            return redirect(url_for("listar_productos"))

        flash("Correo o contraseña incorrectos", "error")

    return render_template("login.html")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        correo = request.form.get("correo", "").strip().lower()
        contrasena = request.form.get("contrasena", "")

        if not nombre or not correo or not contrasena:
            flash("Todos los campos son obligatorios", "error")
            return render_template("registro.html")

        with get_db() as db:
            usuario_existe = db.execute("SELECT id FROM usuario WHERE correo = ?", (correo,)).fetchone()
            if usuario_existe:
                flash("Ese correo ya está registrado", "error")
                return render_template("registro.html")

            db.execute(
                "INSERT INTO usuario (nombre, correo, contrasena) VALUES (?, ?, ?)",
                (nombre, correo, generate_password_hash(contrasena))
            )

        flash("Usuario registrado correctamente", "ok")
        return redirect(url_for("login"))

    return render_template("registro.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada", "ok")
    return redirect(url_for("login"))


@app.route("/")
@login_required
def listar_productos():
    with get_db() as db:
        productos = db.execute("SELECT * FROM producto ORDER BY nombre").fetchall()
    return render_template("productos.html", productos=productos)


@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevoproducto():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        categoria = request.form.get("categoria", "").strip()
        precio = request.form.get("precio", "").strip()
        stock = request.form.get("stock", "0").strip()
        if not nombre or not categoria:
            flash("Nombre y categoría son obligatorios", "error")
            return render_template("form_producto.html")
        with get_db() as db:
            db.execute("INSERT INTO producto (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)",
                       (nombre, categoria, float(precio), int(stock)))
        flash("Producto agregado", "ok")
        return redirect(url_for("listar_productos"))
    return render_template("form_producto.html")


@app.route("/productos/Eliminar/<int:producto_id>", methods=["POST"])
@login_required
def eliminarproducto(producto_id):
    with get_db() as db:
        db.execute("DELETE FROM producto WHERE id = ?", (producto_id,))
    return redirect(url_for("listar_productos"))


@app.route("/productos/editar/<int:producto_id>", methods=["GET", "POST"])
@login_required
def editarproducto(producto_id):
    with get_db() as db:
        producto = db.execute("SELECT * FROM producto WHERE id = ?", (producto_id,)).fetchone()
    if producto is None:
        flash("Producto no encontrado", "error")
        return redirect(url_for("listar_productos"))
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        categoria = request.form.get("categoria", "").strip()
        precio = request.form.get("precio", "").strip()
        stock = request.form.get("stock", "0").strip()
        if not nombre or not categoria:
            flash("Nombre y categoría son obligatorios", "error")
            return render_template("form_producto.html", producto={
                "id": producto_id,
                "nombre": nombre,
                "categoria": categoria,
                "precio": float(precio) if precio else 0,
                "stock": int(stock) if stock else 0,
            })
        with get_db() as db:
            db.execute("UPDATE producto SET nombre=?, categoria=?, precio=?, stock=? WHERE id=?",
                       (nombre, categoria, float(precio), int(stock), producto_id))
        flash("Producto actualizado", "ok")
        return redirect(url_for("listar_productos"))
    return render_template("form_producto.html", producto=producto)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5001)
