import subprocess
import numpy as np

def run_experiment(n, experiments):
    total = []
    init = []
    load = []
    user = []
    t_similarity = []
    c_similarity = []
    gpu_utilization = []

    for experiment in experiments:
        for i in range(n):
            if experiment["flag"] == 1:
                cmd = f"python main.py {experiment['flag']} {experiment['input']}"
            elif experiment["flag"] == 2:
                cmd = f"python main.py {experiment['flag']} {experiment['input']}"
            
            try:
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate()

                if process.returncode != 0:
                    print(f"Command '{cmd}' failed with return code {process.returncode}")
                    print(f"stderr:\n{stderr}")
                    continue

                print(f"Command output:\n{stdout}")  # Debugging output
                
                lines = stdout.splitlines()
                print(f"Lines: {lines}")  # Debugging output

                if len(lines) < 6:
                    print("Unexpected output format. Skipping iteration.")
                    continue
                
                model_init_time = float(lines[0].split(': ')[1].strip(' seconds'))
                load_unit_tests_time = float(lines[1].split(': ')[1].strip(' seconds'))
                get_user_input_time = float(lines[2].split(': ')[1].strip(' seconds'))
                similarity_time = float(lines[3].split(': ')[1].strip(' seconds'))
                if experiment["flag"] == 1:
                    t_similarity.append(similarity_time)
                elif experiment["flag"] == 2:
                    c_similarity.append(similarity_time)
                total_execution_time = float(lines[4].split(': ')[1].strip(' seconds'))
                total.append(total_execution_time)
                init.append(model_init_time)
                load.append(load_unit_tests_time)
                user.append(get_user_input_time)
            except Exception as e:
                print(f"An error occurred: {e}")

    return total, init, load, user, c_similarity, t_similarity

# Define the experiments
experiments = [
    {"flag": 1,"input":"const { isValidFilename } = require('./filenameValidator'); describe('Filename Validator', () => { test('valid filename', () => { expect(isValidFilename('example_file-123.txt')).toBe(true); expect(isValidFilename('another_file.jpg')).toBe(true); expect(isValidFilename('my_document.pdf')).toBe(true);});test('invalid filename', () => {expect(isValidFilename('file with space.txt')).toBe(false);expect(isValidFilename('file#with#hash.txt')).toBe(false);expect(isValidFilename('file$with$dollar.docx')).toBe(false);expect(isValidFilename('.hiddenfile')).toBe(false);expect(isValidFilename('invalid_extension.tar.gz')).toBe(false);});});"}
]

n = 1
total, init, load, user, c_similarity, t_similarity= run_experiment(n, experiments)

print(f"Mean total time: {sum(total) / (n * len(experiments)):.2f} seconds")
print(f"Standard deviation total time: {np.std(total):.2f} seconds")
print(f"Mean init time: {sum(init) / (n * len(experiments)):.2f} seconds")
print(f"Standard deviation init time: {np.std(init):.2f} seconds")
print(f"Mean load time: {sum(load) / (n * len(experiments)):.2f} seconds")
print(f"Standard deviation load time: {np.std(load):.2f} seconds")
print(f"Mean user time: {sum(user) / (n * len(experiments)):.2f} seconds")
print(f"Standard deviation user time: {np.std(user):.2f} seconds")
print(f"Mean code similarity time: {sum(c_similarity) / (len(c_similarity)):.2f} seconds")
print(f"Standard deviation code similarity time: {np.std(c_similarity):.2f} seconds")
print(f"Mean text similarity time: {sum(t_similarity) / (len(t_similarity)):.2f} seconds")
print(f"Standard deviation text similarity time: {np.std(t_similarity):.2f} seconds")
