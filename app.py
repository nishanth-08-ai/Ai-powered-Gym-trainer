import os
import subprocess
import threading
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Initial detected object
detected_object = "None"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/exercise')
def exercise():
    return render_template('exercise.html')  # Ensure 'exercise.html' exists in templates

@app.route('/foodcomposition')
def food_composition():
    try:
        # Render the foodcalc.html page immediately
        # Start the YOLO script asynchronously after rendering the page
        threading.Thread(target=start_yolo).start()
        return render_template('foodcalc.html')
    except Exception as e:
        return jsonify({"error": str(e)})

def start_yolo():
    try:
        # Absolute path to yolo.py (use the same directory as app.py)
        yolo_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'yolo.py')

        print(f"Attempting to run YOLO script at {yolo_script_path}")  # Debug print

        # Check if the script exists before running it
        if os.path.exists(yolo_script_path):
            # Run YOLO script synchronously
            result = subprocess.run(['python', yolo_script_path], capture_output=True, text=True)

            if result.returncode == 0:
                print("YOLO script ran successfully.")
            else:
                print(f"Error running YOLO script: {result.stderr}")
        else:
            print(f"YOLO script not found at {yolo_script_path}")
    except Exception as e:
        print(f"Error running YOLO script: {str(e)}")

@app.route('/update', methods=['POST'])
def update():
    global detected_object
    detected_object = request.json.get('object_name', 'None')
    return jsonify(success=True)

@app.route('/get_object')
def get_object():
    return jsonify(object_name=detected_object)

@app.route('/run-exercise/<exercise_name>', methods=['GET'])
def run_exercise(exercise_name):
    try:
        # Define the base directory path where exercises are stored
        base_path = os.path.join(os.getcwd(), 'exercise')

        # Map exercise names to their respective script files
        exercise_scripts = {
            "squats": "squat.py",
            "alt-dumbbell-curls": "alternative2.py",
            "barbell-row": "barbell2.py",
            "shoulder-press": "Shoulder_press.py"
        }

        # Full path to the Python executable inside the virtual environment
        python_executable = r"D:\HAL\.venv\Scripts\python.exe"

        # Find the corresponding script for the selected exercise
        script = exercise_scripts.get(exercise_name)

        if script:
            # Full path to the script
            script_path = os.path.join(base_path, script)

            if os.path.exists(script_path):
                # Execute the script with the virtual environment's Python executable
                result = subprocess.run([python_executable, script_path], capture_output=True, text=True)
                output = result.stdout if result.returncode == 0 else result.stderr
                return jsonify({"output": output})
            else:
                return jsonify({"error": f"Script not found: {script_path}"})
        else:
            return jsonify({"error": "Exercise script not found!"})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
