# rest_api_simple_example
This is a very simple implementation of Rest API. This project implements a todo-list backend app.
1. [API Description](#api)
2. [Technical details](#tech)
3. [How to run](#run)
# API Description <a name="api"></a> 
HTTP method | URI | action
------ | ------|----------
GET|/api/tasks| Get the list of all tasks
GET|/api/tasks/[task_id]| Get the task with [task_id]
POST|/api/tasks|Create new task
PUT|/api/tasks/[task_id]| Update the existing task with [task_id]
DELETE|/api/tasks/[task_id]| Delete the existing task with [task_id]
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
