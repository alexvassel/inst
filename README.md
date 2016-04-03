### H3 Description

Script, that gets the given user likes statistics. The input is a username,
the output is a database records.

### H3s Tables used

### H4 Table 1 - media

media_id

### H4 Table 2 - user

user_id
username
bio
website
profile picture
full_name
stat_id

### H4 Table 3 - stat

followed_by
follows
media

see diagram.png file from repository


### H3 Usage

To install all requirenments

`pip install -r reqs.txt`

Run

`python main.py username`

Example python main.py 'sample_user'


