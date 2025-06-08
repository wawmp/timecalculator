from flask import Flask, render_template, request, jsonify
import re

class TimeCalculator:
    @staticmethod
    def parse_time(time_str):
        """時:分形式の文字列を分に変換"""
        try:
            hours, minutes = map(int, time_str.split(':'))
            if hours < 0 or minutes < 0 or minutes >= 60:
                raise ValueError
            return hours * 60 + minutes
        except (ValueError, TypeError):
            return None

    @staticmethod
    def format_time(minutes):
        """分を時:分形式に変換"""
        hours = minutes // 60
        minutes = minutes % 60
        return f"{hours:02d}:{minutes:02d}"

    def add(self, time1, time2):
        """時間の加算"""
        minutes1 = self.parse_time(time1)
        minutes2 = self.parse_time(time2)
        if minutes1 is None or minutes2 is None:
            return None
        return self.format_time(minutes1 + minutes2)

    def subtract(self, time1, time2):
        """時間の減算"""
        minutes1 = self.parse_time(time1)
        minutes2 = self.parse_time(time2)
        if minutes1 is None or minutes2 is None or minutes1 < minutes2:
            return None
        return self.format_time(minutes1 - minutes2)

    def multiply(self, time, multiplier):
        """時間 × 数値"""
        try:
            minutes = self.parse_time(time)
            multiplier = float(multiplier)
            if minutes is None or multiplier <= 0:
                return None
            return self.format_time(int(minutes * multiplier))
        except (ValueError, TypeError):
            return None

    def divide(self, time, divisor):
        """時間 ÷ 数値"""
        try:
            minutes = self.parse_time(time)
            divisor = float(divisor)
            if minutes is None or divisor <= 0:
                return None
            return self.format_time(int(minutes / divisor))
        except (ValueError, TypeError):
            return None

app = Flask(__name__)
calculator = TimeCalculator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    operation = data.get('operation')
    time1 = data.get('time1')
    time2 = data.get('time2')
    
    if not all([operation, time1]):
        return jsonify({'error': '必要なパラメータが不足しています'}), 400
    
    if operation == '+':
        result = calculator.add(time1, time2)
    elif operation == '-':
        result = calculator.subtract(time1, time2)
    elif operation == '*':
        result = calculator.multiply(time1, time2)
    elif operation == '/':
        result = calculator.divide(time1, time2)
    else:
        return jsonify({'error': '無効な演算子です'}), 400
    
    if result is None:
        return jsonify({'error': '無効な時間形式または計算エラー'}), 400
    
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
