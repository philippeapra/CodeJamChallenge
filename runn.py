from flask import Flask, render_template, jsonify, request, redirect, url_for
from connection import get_truckers
app = Flask(__name__)

# Hypothetical function to get trucker info. Replace with your actual implementation.
def get_trucker(truck_id):
    # Example logic: return None if truck_id is invalid
    #if truck_id not in get_truckers():  # Replace with your validation logic
     #   return None
    return {"id": truck_id}  # Replace with actual trucker data

@app.route('/')
def index():
    return render_template('page.html') 

@app.route('/submit_truck_id', methods=['POST'])
def submit_truck_id():
    truck_id = request.form.get('truckId')
    trucker_info = get_trucker(truck_id)

    if trucker_info is None:
        # Truck ID is invalid
        return render_template('page.html', error="Invalid Truck ID")
    else:
        # Truck ID is valid, redirect to dashboard
        return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
