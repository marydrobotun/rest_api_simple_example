# rest_api_simple_example
This is a very simple implementation of Rest API. This project implements a todo-list backend app.
1. [API Description](#api)
2. [Technical details](#tech)
3. [How to run](#run)
# API Description <a name="api"></a> 
HTTP method | URI | action <a name="table"></a>
------ | ------|----------
GET|/api/tasks| Get the list of all tasks
GET|/api/tasks/[task_id]| Get the task with [task_id]
POST|/api/tasks|Create new task
PUT|/api/tasks/[task_id]| Update the existing task with [task_id]
DELETE|/api/tasks/[task_id]| Delete the existing task with [task_id].

Our task will have these fields:
* **title**: the title of a task, string
* **description**: the description of a task, string
* **id**: the unique identificator of a task, numeric
* **done**:  whether the task is done or not, bool

To get the list of all tasks, we should, according to the [table](#table), send to our server an http-request with method GET

The example using curl:
```sh
curl -i http://hostname/api/tasks
```
To get the one task, for example with id=2, run this:
```
curl -i http://hostname/api/tasks/2
```

To add a new task:
```
curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book", "done": false, "description":"Harry Potter and the Chamber of Secrets, page 122"}' http://hostname/api/tasks
```
To update an existing task:
```
curl -i -H "Content-Type: application/json" -X PUT  -d '{"done": true}' http://hostname/api/tasks/11
```
To delete a task:
```
curl -i -H "Content-Type: application/json" -X DELETE http://hostname/api/tasks/11
```

# Technical details <a name="tech"></a>
The app uses [MongoDB](https://www.mongodb.com/) to store information about tasks. The database's name used by app is 'tasks'. It has only one collection 'tasks', where documents like this:
```
{
      "description": "Wash dishes and do the laundry",
      "done": false,
      "id": 1,
      "title": "Do the cleaning"
}
```
are stored.

The app uses [Docker](https://www.docker.com/). It contains three docker containers. One for the server app, the other for MongoDB and the third for restoring the MongoDB from dump. Database is restored automatically when the containers start.  

The server part of the app is made on [Flask framework](https://flask.palletsprojects.com/en/2.2.x/).
# How to run <a name="run"></a>
Firstly, downlodad the source code with git clone.

Then you should create a .env file:
```
mongo_login=admin
mongo_password=admin
```
to specify mongo login and mongo password. You can choose it as you like.

You can also create a docker-network for your containers.
```
 docker network create --driver bridge --subnet 192.168.100.0/24 --ip-range 192.168.100.0/24 my-bridge-network
```
But you can also use a default docker-net. If you choose to use the default one, you should delete these lines from [docker-compose.yml](https://github.com/marydrobotun/rest_api_simple_example/blob/main/docker-compose.yml):
```
        external:
          name: my-bridge-network
```
After that, you should build the images:
```
docker-compose build
```
and after they're builded, run the containers:
```
docker-compose up
```
The server uses 80 port.
