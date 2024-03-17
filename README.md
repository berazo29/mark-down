# Marker
A program to convert a text file following markdown syntax to html. 

## Usage

**Run the program:**
```python
python src/marker.py <filename> --tokens --html --out <outputfile>
```

**For help:**
```python
python src/marker.py -h
```

**Arguments and Options:**
```
positional arguments:
  filename         the markdown filename to be converted to html

options:
  -h, --help       show this help message and exit
  --tokens         print the tokens
  --html           print the html
  --output OUTPUT  output file
```
## Features
1. Headers h1 to h6.
2. Handle unformated text.
3. Links parser.
4. Ignores blank lines.
5. Print tokens list from input file in console.  
6. Print html covertion in cosole. 
7. Write html file.

## Local Install
1. Create a local virtual enviroment. 
```bash
python -m venv venv
```
2. Activate the enviroment (MACOS)
```bash
source ./venv/bin/activate
```
3. Install the libraries
```
pip install requirements.txt
```


## Development
Run a single file test
```python
pytest tests/test_marker.py
```

Run a single class test suite
```python
pytest tests/test_marker.py::TestTokinize
```

Run coverage
```python
coverage run -m pytest;coverage report
```
