"""
বাংলা উপভাষা অনুবাদক — মূল Flask অ্যাপ।
চালাতে: python app.py
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models_db import db, User, History
import translator

app = Flask(__name__)
app.config["SECRET_KEY"] = "dialect-secret-key-change-this"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ---------- Auth routes ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        if not username or not password:
            flash("সব ঘর পূরণ করুন", "error")
        elif User.query.filter_by(username=username).first():
            flash("এই ইউজারনেম আগে থেকেই আছে", "error")
        else:
            u = User(username=username)
            u.set_password(password)
            db.session.add(u)
            db.session.commit()
            flash("অ্যাকাউন্ট তৈরি হয়েছে! এখন লগইন করুন।", "success")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("ভুল ইউজারনেম বা পাসওয়ার্ড", "error")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ---------- Main routes ----------
@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("landing.html")


@app.route("/dashboard")
@login_required
def dashboard():
    history = History.query.filter_by(user_id=current_user.id).order_by(History.id.desc()).limit(10).all()
    total = History.query.filter_by(user_id=current_user.id).count()
    return render_template("dashboard.html", history=history, total=total)


@app.route("/translate", methods=["GET", "POST"])
@login_required
def translate_page():
    result = None
    if request.method == "POST":
        text = request.form["text"].strip()
        direction = request.form["direction"]
        dialect = request.form["dialect"]
        model_choice = request.form["model"]
        if text:
            result = translator.translate(text, direction=direction,
                                          dialect=dialect, model_choice=model_choice)
            # ইতিহাসে সেভ
            h = History(user_id=current_user.id, input_text=text,
                        output_text=result["final"], direction=direction,
                        dialect=dialect, model=model_choice)
            db.session.add(h)
            db.session.commit()
    return render_template("translate.html", result=result, dialects=translator.DIALECTS)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # database তৈরি
    print("=" * 50)
    print("মডেল লোড হচ্ছে... (১-২ মিনিট অপেক্ষা করুন)")
    print("=" * 50)
    translator.load_all()   # মডেল + RAG লোড
    print("\n🚀 সার্ভার চালু! browser এ খুলুন: http://127.0.0.1:5000\n")
    app.run(debug=False, port=5000)