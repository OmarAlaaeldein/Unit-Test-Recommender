# Unit Test Recommendation Engine

This project provides a Python script designed to streamline the process of finding relevant unit tests for a given piece of code or a textual description. Leveraging machine learning models, the script recommends unit tests based on either textual descriptions or similar tests.

## Usage

To utilize the script, you can execute the `main.py` file. The script is designed to automate the process by accepting command-line arguments. For instance, to perform text similarity, you would run the script with a flag indicating text similarity and the text input. Similarly, for code similarity, you would use a different flag and provide the code input.

```bash
python main.py 1 "This is a test for a function that adds two numbers"
```


In this example, 1 is the flag indicating that the script should perform text similarity, and "A test for a function that adds two numbers" is the text input.

If you want to perform code similarity, you can use the following command:

```bash
python main.py 2 "def add_numbers(a, b): return a + b"
```

## How it Works

The script operates in the following steps:

1. Initializes a machine learning model.
2. Loads unit tests from a specified directory, summarizes them using the model, and encodes the summaries.
3. Accepts user input (either text or code) and performs a semantic search to find the most similar unit tests based on the input.
4. Writes the results to a file in JSON format.

## Contributing

We welcome contributions to the Unit Test Recommendation Engine! If you have any suggestions, find any issues, or want to add new features, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.