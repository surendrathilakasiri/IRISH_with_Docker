import numpy as np 
from flask import Flask, request
from predict import make_prediction
from flask import jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return """
    <html>
      <head>
        <title>Iris Classification Model with Logistic Regression</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            background: #f7f9fc;
            margin: 0;
            padding: 0;
          }
          .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 40px;
            gap: 40px;
          }
          .left {
            width: 40%;
          }
          .right {
            width: 55%;
            text-align: center;
          }
          .card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
          }
          h2 {
            margin-top: 0;
          }
          label {
            display: block;
            margin-top: 12px;
            font-weight: bold;
          }
          input {
            width: 100%;
            padding: 8px;
            margin-top: 4px;
            border-radius: 6px;
            border: 1px solid #ccc;
          }
          button {
            margin-top: 18px;
            width: 100%;
            padding: 12px;
            background: #2ecc71;
            color: white;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
          }
          button:hover {
            background: #27ae60;
          }
          pre {
            background: #eef3f8;
            padding: 12px;
            border-radius: 8px;
            margin-top: 15px;
          }
          img {
            max-width: 100%;
            border-radius: 14px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
          }
        </style>
      </head>

      <body>
        <div class="container">
          
          <!-- LEFT SIDE: FORM -->
          <div class="left">
            <div class="card">
              <h2>Iris Flower Prediction with Logistic Regression </h2>

              <form id="predictForm">
                <label>Sepal Length (cm)</label>
                <input type="number" step="any" name="sepal_length_cm" value="5.1" required>

                <label>Sepal Width (cm)</label>
                <input type="number" step="any" name="sepal_width_cm" value="3.5" required>

                <label>Petal Length (cm)</label>
                <input type="number" step="any" name="petal_length_cm" value="1.4" required>

                <label>Petal Width (cm)</label>
                <input type="number" step="any" name="petal_width_cm" value="0.2" required>

                <button type="submit">Predict</button>
              </form>

              <pre id="result">Waiting for prediction...</pre>
            </div>
          </div>

          <!-- RIGHT SIDE: IMAGE -->
          <div class="right">
            <img src="/static/iris_model.png" alt="Iris ML Model">
          </div>

        </div>

        <script>
          const form = document.getElementById("predictForm");
          const resultEl = document.getElementById("result");

          form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const payload = Object.fromEntries(formData.entries());
            for (const k in payload) payload[k] = Number(payload[k]);

            resultEl.textContent = "Predicting...";

            const res = await fetch("/predict", {
              method: "POST",
              headers: {"Content-Type": "application/json"},
              body: JSON.stringify(payload)
            });

            const text = await res.text();
            resultEl.textContent = text;
          });
        </script>
        <footer style="
        text-align: center;
        padding: 18px;
        background: #f0f2f5;
        border-top: 1px solid #ddd;
        font-size: 13px;
        color: #555;
        ">
        <label>
            © <span id="year"></span> Surendra Koththigoda · Iris Classification ML Model
            &nbsp;|&nbsp;
            <a href="https://www.linkedin.com/in/surendrakoththigoda/" target="_blank" style="color:#2c7be5; text-decoration:none;">LinkedIn</a>
            &nbsp;|&nbsp;
            <a href="https://github.com/surendrathilakasiri/IRISH_with_Docker/" target="_blank" style="color:#2c7be5; text-decoration:none;">GitHub</a>
        </label>
        </footer>
        <script>
        document.getElementById("year").textContent = new Date().getFullYear();
        </script>
      </body>
    </html>
    """


@app.route("/predict", methods=["POST"])
def predict():
    data_json = request.get_json(silent=True)
    if data_json is None:
        data_json = request.form.to_dict()

    sepal_length_cm = float(data_json["sepal_length_cm"])
    sepal_width_cm = float(data_json["sepal_width_cm"])
    petal_length_cm = float(data_json["petal_length_cm"])
    petal_width_cm = float(data_json["petal_width_cm"])

    data = np.array([[sepal_length_cm, sepal_width_cm, petal_length_cm, petal_width_cm]])
    predictions = make_prediction(data)

    return str(predictions)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
