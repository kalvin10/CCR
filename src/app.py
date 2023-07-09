from flask import Flask, request, jsonify, render_template
import tensorflow as tf
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def record_to_input_data(passed_record):
    record = passed_record
    input_data = []
    if record[1] == 'Germany':
        temp_list = [1, 0, 0]
        input_data.extend(temp_list)
    elif record[1] == 'Austria':
        temp_list = [0, 1, 0]
        input_data.extend(temp_list)
    elif record[1] == 'Switzerland':
        temp_list = [0, 0, 1]
        input_data.extend(temp_list)

    if record[5] == 'Visa':
        temp_list = [1, 0, 0]
        input_data.extend(temp_list)
    elif record[5] == 'Diners':
        temp_list = [0, 1, 0]
        input_data.extend(temp_list)
    elif record[5] == 'Master':
        temp_list = [0, 0, 1]
        input_data.extend(temp_list)
    if record[2] < 100:
        temp_list = [1, 0, 0]
        input_data.extend(temp_list)
    elif 100 <= record[2] <= 300:
        temp_list = [0, 1, 0]
        input_data.extend(temp_list)
    elif record[2] > 300:
        temp_list = [0, 0, 1]
        input_data.extend(temp_list)

    datetime_object = datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S')
    weekday = datetime.weekday(datetime_object)
    if weekday == 0:
        temp_list = [1, 0, 0, 0, 0, 0, 0]
        input_data.extend(temp_list)
    elif weekday == 1:
        temp_list = [0, 1, 0, 0, 0, 0, 0]
        input_data.extend(temp_list)
    elif weekday == 2:
        temp_list = [0, 0, 1, 0, 0, 0, 0]
        input_data.extend(temp_list)
    elif weekday == 3:
        temp_list = [0, 0, 0, 1, 0, 0, 0]
        input_data.extend(temp_list)
    elif weekday == 4:
        temp_list = [0, 0, 0, 0, 1, 0, 0]
        input_data.extend(temp_list)
    elif weekday == 5:
        temp_list = [0, 0, 0, 0, 0, 1, 0]
        input_data.extend(temp_list)
    elif weekday == 6:
        temp_list = [0, 0, 0, 0, 0, 0, 1]
        input_data.extend(temp_list)

    hour = datetime_object.hour
    for j in range(24):
        if j == hour:
            input_data.append(1)
        else:
            input_data.append(0)

    input_data.append(record[4])
    return input_data

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        input_record = request.json['input_record']
        model = tf.keras.models.load_model("tensor_flow_model.h5")
        test_record = record_to_input_data(input_record)
        sample = {
            "Is_Germany": test_record[0],
            "Is_Austria": test_record[1],
            "Is_Switzerland": test_record[2],
            "Is_Visa": test_record[3],
            "Is_Diners": test_record[4],
            "Is_Master": test_record[5],
            "amount0": test_record[6],
            "amount1": test_record[7],
            "amount2": test_record[8],
            "Monday": test_record[9],
            "Tuesday": test_record[10],
            "Wednesday": test_record[11],
            "Thursday": test_record[12],
            "Friday": test_record[13],
            "Saturday": test_record[14],
            "Sunday": test_record[15],
            "hour0": test_record[16],
            "hour1": test_record[17],
            "hour2": test_record[18],
            "hour3": test_record[19],
            "hour4": test_record[20],
            "hour5": test_record[21],
            "hour6": test_record[22],
            "hour7": test_record[23],
            "hour8": test_record[24],
            "hour9": test_record[25],
            "hour10": test_record[26],
            "hour11": test_record[27],
            "hour12": test_record[28],
            "hour13": test_record[29],
            "hour14": test_record[30],
            "hour15": test_record[31],
            "hour16": test_record[32],
            "hour17": test_record[33],
            "hour18": test_record[34],
            "hour19": test_record[35],
            "hour20": test_record[36],
            "hour21": test_record[37],
            "hour22": test_record[38],
            "hour23": test_record[39],
            "secured": test_record[40],

        }
        input_dict = {name: tf.convert_to_tensor([value]) for name, value in sample.items()}

        predictions = model.predict(input_dict)

        json_data = {
            "UK_card_PSP": round(100 * predictions[0][0], 1),
            "Simplecard_PSP": round(100 * predictions[0][1], 1),
            "Moneycard_PSP": round(100 * predictions[0][2], 1),
            "Goldcard_PSP": round(100 * predictions[0][3], 1),
            "Transaction_Failed": round(100 * predictions[0][4], 1)
        }
        del json_data["Transaction_Failed"]

        highest_key = max(json_data, key=json_data.get)

        result = f"{highest_key}: {json_data[highest_key]}"

        output_data = {
            "Out of all PSP, the best possible PSP is": result,
            "overall PSP values": json_data
        }

        return jsonify(output_data)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
