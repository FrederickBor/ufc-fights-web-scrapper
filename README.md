# UFC Data Web Scrapper

This web scrapper is used to get all the figths on Sherdog's website

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

| Requirement Name | Version |
| ---------------- | ------- |
|beautifulsoup4|4.8.1|
|certifi|2019.11.28|
|chardet|3.0.4|
|idna|2.8|
|requests|2.22.0|
|soupsieve|1.9.5|
|urllib3|1.25.7|

### Installing

* Clone the repository:
```bash 
$ git clone git@github.com:FrederickBor/ufc-fights-web-scrapper.git
```

*Optional: create a virtualenv*
```bash
$ pip3 install virtualenv
$ virtualenv [env-name] --python=python3
$ source [env-name]/bin/activate
```

Install the requirements:
```bash
$ pip install -r requirements.txt
```

Execute the code:
```bash
$ python3 webScrapping.py
```


## Authors

* **Frederick Borges** - *Initial work* - [FrederickBor](https://github.com/FrederickBor)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
