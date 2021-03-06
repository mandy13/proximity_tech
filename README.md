## Assumptions
* A Subject is parent of course. For eg a subject can be English and course
can be "Shakespeare", "Essay Writing", etc.
  
## Tech Stack Used
* Used Django version 3.1.7
* Python 3.9.1
* requirements.txt file contains version for other libraries used.

##Improvements

* video uploading could be time consuming so we can make that call async or
create another service which does video management. This service will 
also be responsible for managing the storage.
* Pagination can be used when list is returned
  
## Steps to run
* create a virtual environment.
* pip install requirements.txt
* start server by `python manage.py runserver.`
* access the below URLs using postman at localhost
* use basic auth in postman and enter the credentials below.

### Authorized users
* Student: Student/stud
* Instructor: Instructor/inst

### DB Schema
* Table Subject with foreign key as user.
* Table Course with foreign key as subject.
* Table Tags which share many to many relation with Webinar/videos
* Table Webinar which shares many to many relateion with Course, Subject and Tags.
* Table Video which shares many to many relateion with Course, Subject and Tags.


## REST API

### Subject

#### Create Subject
POST /webapp/subject/


![alt text](readme-images/subject-create.png)

#### Get Subject
GET /webapp/subject/<id>//
![alt text](readme-images/subject-get.png)

#### Delete Subject
DELETE /webapp/subject/<id>/
![alt text](readme-images/subject-delete.png)

#### Update Subject
PATCH /webapp/subject/<id>/
![alt text](readme-images/subject-patch.png)

#### Student Access
![alt text](readme-images/student-denied.png)

### Course

#### Create Course
POST /webapp/subject/<id>/course/
![alt text](readme-images/course-create.png)

#### Get Course
GET /webapp/subject/<id>/course/<course-id>
![alt text](readme-images/course-get.png)

#### Delete Course
DELETE /webapp/subject/<id>/course/<course-id>
![alt text](readme-images/course-delete.png)

#### Update Course
PATCH /webapp/subject/<id>/course/<course-id>
![alt text](readme-images/course-patch.png)

#### Student Access
![alt text](readme-images/course-stud-denied.png)

### TAGs
#### Create Tag
POST /webapp/tags/
![alt text](readme-images/tags-create.png)

#### Get Subject
GET /webapp/tags/<id>/
![alt text](readme-images/tags-get.png)

#### Delete Subject
DELETE /webapp/tags/<id>/
![alt text](readme-images/tags-delete.png)

#### Update Subject
PATCH /webapp/tags/<id>/
![alt text](readme-images/tags-patch.png)

#### Student Access
![alt text](readme-images/tags-student-denied.png)

### Webinar

#### Webinar Create
POST /webapp/webinar/
![alt text](readme-images/webinar-create.png)

DELETE, PATCH will work the same with url /webapp/webinar/<webinar-id>

### Video

#### Video Create
POST /webapp/video/

![alt text](readme-images/video-create-1.png)
![alt text](readme-images/video-create-2.png)

**NOTE that new tag Ruskin bond gets created. I have maintained
two fields one is the tags and the other is new_tags. tags is a list
of existing tag id and new_tags is a list of string tags**

DELETE, PATCH will work the same with url /webapp/video/{video-id}


### Most viewd videos/webinars/courses

When a GET request is called on video/webinar/course a count
is incremented. The increment operation is made atomic.
based on count the list is sorted.

GET /webapp/{webinar|video}/mostviewed
GET /webapp/subject/{subject-id}/course/mostviewed/
![alt text](readme-images/most-viewed.png)

### Student viewing list webinar/videos.

![alt text](readme-images/student-view-webinar.png)
![alt text](readme-images/student-view-video.png)

### Search webinar/videos by tittle.
GET /webapp/webinar?title={title}
![alt text](readme-images/title-search.png)


### Search webinar with course/subject/tag names
/webapp/webinar/?tags__name=Writing&subject__name=English

![alt text](readme-images/search.png)

### Suggestion videos
Returns current webinar and list of related webinars and videos
![alt text](readme-images/suggestions.png)


