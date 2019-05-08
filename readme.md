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

## Implementation
This section will detail how the code base works and provide a general overview of all the components. Starting with scraping/crawling the web for data and ending at giving the user a recommendation on what dependencies they should install/look at
### Crawling the web
Our project's recommendation algorithm requires that we have examples of packag.json files to compare against. In order to do this at sufficient scale, we crawl reddit for github links and convert those github links to package.json files. The steps of the process are as follows:
1. Using [praw](https://praw.readthedocs.io/en/latest/), we find all subreddits related to the term github
2. Then we search those subreddits for links to github repos.
3. Then we check to see if those github repos contain package.json files and download them.
4. We make sure that this package.json file is properly formatted and extract the information that we need from it and store it in a list of these packages.
5. We define the list of packages we download as our user packages and save them to disc.
6. For each of our user packages we then scrape their dependencies information from https://www.npmjs.com/
7. These packages we scraped from npmjs.com are the object packages and are saved to disc.
### The website
This project is written in python3 using the flask framework. It hosts two main end points, **/index.html** and **/job/**. The first will be the main portal that users will start at when they want to recieve a recommendation. The users can also opt out of a data collection service where we keep their package.json files which could be useful for further refining of the collaborative filtering algorith.The second will display the results of whatever recommendation they requested. The user might have to wait a short time on this page but the results will automatically be displayed when the backend server has finished processing. The general workflow is that a user uploads their package.json file and then are transfered to some webpage **/job/XXXXX** and then wait for their results to be published. This waiting is simulated by occasionally refreshing the page until the results of the job have been saved.
### The algorithm and processing
When a request is recieved, it is processed using the same package information extracting code the crawler uses and a unique id is generated. This extracted package object is then placed in a job queue to be processed by a pool of some number of workers. When a worker recieves the package, it will run collaboritive filtering using the user and object packages crawled from before. Similarities between the retrieved package and all the user packages are precomputed, and then the [memory based collaborative filtering](https://en.wikipedia.org/wiki/Collaborative_filtering) algorithm is parallized over some number of processors. When the worker is finished, it finds the top X, usually 10, best recommendations of objects, which for this project are dependencies. The worker than places these results in a queue which is then picked up by another worker to save these results to disk.

## Contributions
* Curtis
	* Collabortive Filtering parrallization
	* Job queue system
	* Set up flask
	* Installization and Implementation documentation
	* NPM package crawler and extractor