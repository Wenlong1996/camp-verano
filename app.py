
from flask import Flask, render_template, request
import pandas as pd
import re

app = Flask(__name__)

# 读取 Excel 数据
df = pd.read_excel("data/夏令营资料库.xlsx")

# 预处理证件号：去除破折号并转为大写
df["规范证件号"] = df["证件号"].astype(str).str.replace("-", "").str.upper()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        id_number = request.form["id_number"].strip()
        id_number_cleaned = re.sub(r"[^A-Za-z0-9]", "", id_number).upper()

        person = df[df["规范证件号"] == id_number_cleaned]

        if not person.empty:
            user_row = person.iloc[0]
            user_name = user_row["姓名（中文）"]
            group = user_row["组别"]
            room_number = user_row["房间号"]

            # 获取本组所有人
            same_group = df[df["组别"] == group]

            # 获取辅导信息
            mentors = same_group[same_group["身份"] == "辅导"][["姓名（中文）", "联系电话"]].to_dict("records")

            # 获取组员信息（排除自己）
            members = same_group[(same_group["身份"] == "组员") & (same_group["规范证件号"] != id_number_cleaned)][["姓名（中文）", "所属堂点"]].to_dict("records")

            result = {
                "user_name": user_name,
                "group": group,
                "room_number": room_number,
                "mentors": mentors,
                "members": members
            }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
