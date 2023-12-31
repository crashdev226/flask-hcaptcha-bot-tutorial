import subprocess
import uuid
import os
import json

from flask import Flask, jsonify, send_from_directory, render_template, request

app = Flask(__name__)
app.debug = True


@app.route("/create-session", methods=["POST", "GET"])
def create_session():
    cpf = request.args.get("cpf", "06780432627")
    data_nascimento = request.args.get("data_nascimento", "20/05/1983")
    token = str(uuid.uuid4())

    process = subprocess.Popen(
        ["python3", "hcaptcha.py", token, cpf, data_nascimento],
        stdout=subprocess.PIPE,
    )
    return render_template(
        "page.html", token=token, cpf=cpf, data_nascimento=data_nascimento
    )
    return jsonify({"token": token})

@app.route("/create-session-monster", methods=["POST", "GET"])
def create_session_monster():
    cpf = request.args.get("cpf", "06780432627")
    data_nascimento = request.args.get("data_nascimento", "20/05/1983")
    token = str(uuid.uuid4())

    process = subprocess.Popen(
        ["python3", "hcaptcha_v1_s1_monster.py", token, cpf, data_nascimento],
        stdout=subprocess.PIPE,
    )
    return render_template(
        "page.html", token=token, cpf=cpf, data_nascimento=data_nascimento
    )
    return jsonify({"token": token})
@app.route("/create-session-2captcha", methods=["POST", "GET"])
def create_session_2captcha():
    cpf = request.args.get("cpf", "06780432627")
    data_nascimento = request.args.get("data_nascimento", "20/05/1983")
    token = str(uuid.uuid4())

    process = subprocess.Popen(
        ["python3", "hcaptcha_v1_s2_twocaptcha.py", token, cpf, data_nascimento],
        stdout=subprocess.PIPE,
    )
    return render_template(
        "page.html", token=token, cpf=cpf, data_nascimento=data_nascimento
    )
    return jsonify({"token": token})


@app.route("/create-session-v2", methods=["POST", "GET"])
def create_session_v2():
    cnpj = request.args.get("cnpj", "10753249000121")
    token = str(uuid.uuid4())

    process = subprocess.Popen(
        ["python3", "hcaptcha_v2.py", token, cnpj],
        stdout=subprocess.PIPE,
    )
    return render_template("page_v2.html", token=token, cnpj=cnpj)
    return jsonify({"token": token})


@app.route("/download/<upload_id>")
def download(upload_id):
    file_path = f"data/{upload_id}.json"
    content = {
        "type": "error",
        "data": "Scraping not finished. Please try again later.",
    }
    try:
        with open(file_path, "r") as f:
            content = json.load(f)
        # with open(file_path, "rb") as file:
        #     content = file.read().decode("utf-8")
    except:
        pass
    print(content)

    return render_template(
        "data.html",
        content=content["data"].replace("\n", " "),
    )
    

@app.route("/download-v2/<upload_id>")
def download_v2(upload_id):
    file_path = f"data/{upload_id}.json"
    content = {
        "type": "error",
        "data": {
            "cnpjContent": "Scraping not finished. Please try again later.",
            "qsaData": "",
        },
    }
    try:
        with open(file_path, "r") as f:
            content = json.load(f)
        # with open(file_path, "rb") as file:
        #     content = file.read().decode("utf-8")
    except:
        pass
    print(content)

    return render_template(
        "data_v2.html",
        cnpjContent=content["data"]["cnpjContent"].replace("\n", " "),
        qsaData=content["data"]["qsaData"].replace("\n", " "),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)


# with open("./users/" + name + ".json", "r", encoding="utf-8-sig") as f:
#     profile = json.load(f)
