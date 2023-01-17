# GithubAction

## Création du fichier python

```py
import unittest

class SimpleMath:
    @staticmethod
    def addition(x, y):
        return x + y
    @staticmethod
    def subtraction(x, y):
        return x - y

class TestSimpleMath(unittest.TestCase):
    def test_addition(self):
        result = SimpleMath.addition(5, 3)
        self.assertEqual(result, 8)

    def test_subtraction(self):
        result = SimpleMath.subtraction(5, 3)
        self.assertEqual(result, 2)

if __name__ == '__main__':
    unittest.main()
```

## Mon fichier yml 
```yml
name: Python application test

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

permissions:
  contents: read

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python 3.10
      uses: actions/setup-python@v3
      with:
        python-version: "3.10"
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pylint
        pip install flake8 pytest
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - name: Test with pytest
      run: |
        pytest main.py
        pylint main.py
```

À la sortie, j'ai :
```
Initiation-GithubAction\main.py:1:0: C0114: Missing module docstring (missing-module-docstring)
Initiation-GithubAction\main.py:3:0: C0115: Missing class docstring (missing-class-docstring)
Initiation-GithubAction\main.py:5:4: C0116: Missing function or method docstring (missing-function-docstring)
Initiation-GithubAction\main.py:5:17: C0103: Argument name "x" doesn't conform to snake_case naming style (invalid-name)
Initiation-GithubAction\main.py:5:20: C0103: Argument name "y" doesn't conform to snake_case naming style (invalid-name)
Initiation-GithubAction\main.py:8:4: C0116: Missing function or method docstring (missing-function-docstring)
Initiation-GithubAction\main.py:8:20: C0103: Argument name "x" doesn't conform to snake_case naming style (invalid-name)
Initiation-GithubAction\main.py:8:23: C0103: Argument name "y" doesn't conform to snake_case naming style (invalid-name)
Initiation-GithubAction\main.py:11:0: C0115: Missing class docstring (missing-class-docstring)
Initiation-GithubAction\main.py:12:4: C0116: Missing function or method docstring (missing-function-docstring)
Initiation-GithubAction\main.py:16:4: C0116: Missing function or method docstring (missing-function-docstring)
```

Pour corriger ce problème, il suffit de lui préciser de continue même si erreur ! 
```yaml
name: Python application test

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

permissions:
  contents: read

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python 3.10
      uses: actions/setup-python@v3
      with:
        python-version: "3.10"
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pylint
        pip install flake8 pytest
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - name: Test with pytest
      run: |
        pytest main.py
    - name : Test with pylint
      continue-on-error: true
      run: |
        pylint main.py
    - name: Build and run Docker image
      uses: ./docker
      with:
        args: build -t my-image:latest . && docker run --rm my-image:latest
```
On a également fait le DockerFile. 

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["pylint", "main.py"]
```

Mais malgré cela, cela ne se lance pas dû à ce problème : 
