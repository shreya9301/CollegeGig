# CollegeGig
<br />
<p>
  An online job portal for university students wherein they can apply to the jobs provided by campus faculties. 
  The members who are a part of college's database are only allowed to register/login to the portal.
  Students can filter jobs according to campus location, job type, etc. to access relevant jobs. 
  Faculty members can post jobs and once they are verified by the moderator, the jobs are published to the portal. 
  The applicants and their profiles are accessible to the respective faculty member who posted the job.<br>
  The profile of the students primarily comprise of their college's transcript. 
  To be eligible candidate for the job, the students must have prerequisite grades mentioned in the job details. 
  There's also bookmark feature to save job so that the student doesn't have to search for that job repeatedly.
  For this project, I have used dummy data in the form of json format for the transcript details.
</p>

# Demo Video
[Demo](https://user-images.githubusercontent.com/65105127/186474966-50732560-83ef-4ed0-9799-abdec8c9083e.webm)



# Installation Process
### Install System Dependencies
* git
* pip

### Get the code
* Clone the repository in your terminal <code>git clone https://github.com/shreya9301/CollegeGig.git</code>

### Setup Virtual environment
* Create a virtual environtment - <code>virtualenv env</code>
* Activate VirtualENV - ubuntu : <code>source env/bin/activate</code> || windows : <code>\env\Scripts\activate</code>
* <code>cd collegegig</code>

### Install the project dependencies
```python
pip install -r requirements.txt
```
### Run the command to generate the database
```python
python manage.py makemigrations
python manage.py migrate
```

### Generate super user
```python
python manage.py createsuperuser
```

### Run the local server
<code>python manage.py runserver</code> - the application will be running on port 8000 http://127.0.0.1:8000/

