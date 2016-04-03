### Description

Script, that gets the given user likes statistics. The input is a username,
the output is a database records.

Script creates (or updates) database with the name `instagram.db`

### Tables used

#### Table 1 - media

media_id

#### Table 2 - user

* user_id
* username
* bio
* website
* profile picture
* full_name
* stat_id

#### Table 3 - stat

* followed_by
* follows
* media

see diagram.png file from repository


### Usage

To install all requirenments

`pip install -r reqs.txt`

Run

`python main.py username`

Example `python main.py 'sample_user'`


