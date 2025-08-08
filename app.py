from flask import Flask, render_template, redirect, url_for
import subprocess
import pyautogui  # We'll use this to simulate key press

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/workout/<workout>')
def video_page(workout):
    return render_template('video.html', workout=workout)

@app.route('/start/<workout>')
def start_workout(workout):
    try:
        script_path = f'workouts/{workout}.py'
        subprocess.Popen(['python', script_path])
        return f"{workout.capitalize()} workout started!"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/toggle_2d/<workout>')
def toggle_2d(workout):
    try:
        # Simulate pressing 'm' key to toggle 2D mapping
        pyautogui.press('m')
        return "Toggled 2D mapping"
    except Exception as e:
        return f"Error toggling 2D mapping: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
