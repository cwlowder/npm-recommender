# Description of project
This project allows for a user to upload their npm [package.json file](https://docs.npmjs.com/files/package.json) and receive a recomendation of what dependencies they should install/look at using [memory based collaborative filtering](https://en.wikipedia.org/wiki/Collaborative_filtering).

## Installation
First make sure you have python3 and pip3 installed
```bash
sudo apt-get install python3
sudo apt-get install python3-pip
```
Next, git clone this repo somewhere locally and change directory into it
```bash
git clone git@github.com:cwlowder/npm-recommender.git
cd npm-recommender
```
Create a [virtual environment](https://www.geeksforgeeks.org/python-virtual-environment/) with some name and activate it
```bash
virtualenv env_name
source env_name/bin_activate
```
Install dependencies
```bash
pip3 install -r requirements.txt
```

## Running Server
To run the server, all you need to do is execute the following bash command from the root of the directory
```bash
python3 server.py
```
If you need to set the port of the server to be some value X, run this instead
```bash
PORT=X python3 server.py
```

## Running crawler
Run the following command to crawl from scratch:
```bash
python3 crawler.py
```
Please note that the crawler:
* first looks on reddit for github links
* then scrapes those github urls for package.json files
* and lastly builds out the object and user files
The First two steps can be skipped over if you already have those files by setting for the crawl call in crawler.py the optional arguments github_links and package_json. Note that if you set package_json, github_links will be ignored. This is an example of how to load those two files into memory to be passed as arguments:
```python
github_links = loadFile("data/reddit_all_github.txt")
package_json = loadFile("data/reddit_all_packages.txt")
```