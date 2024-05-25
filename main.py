from flask import Flask, request, jsonify ,render_template
import subprocess
import os

app = Flask(__name__)



@app.route("/a")
def a ():
    return render_template("a.html")





@app.route("/")
def index(): 
    return render_template("code.html")

@app.route('/run', methods=['POST'])
def run_code():
    filename = request.form['filename']
    code = request.form['code']
    
    with open(filename, 'w') as f:
        f.write(code)
    
    extension = filename.split('.')[-1]
    if extension == 'py':
        command = ['python', filename]
    elif extension == 'cpp':
        compiled_file = filename.replace('.cpp', '')
        compile_command = ['g++', filename, '-o', compiled_file]
        subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        command = [f'./{compiled_file}']
    elif extension == 'c':
        compiled_file = filename.replace('.c', '')
        compile_command = ['gcc', filename, '-o', compiled_file]
        subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        command = [f'./{compiled_file}']
    elif extension == 'rs':
        command = ['rustc', filename]
    else:
        return 'Unsupported file type'

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    os.remove(filename)

    if result.returncode == 0:
        return result.stdout.decode('utf-8')
    else:
        return result.stderr.decode('utf-8')

@app.route('/terminal', methods=['POST'])
def terminal():
    command = request.form['command']
    password = request.form['password']
    result = subprocess.run(['sudo', '-S', command], input=password, text=True, capture_output=True)
    return jsonify({'stdout': result.stdout, 'stderr': result.stderr})

if __name__ == '__main__':
    app.run(debug=True)
