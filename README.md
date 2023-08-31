# Summary

object detection app that classifies objects from
an input video received by HTTP request.


# Architecture

 - The main API is working as a job orchestrator or task publisher
 - The celery app is subscribed to the redis queue that fills from API
 - After the task is finnished the result is stored in the redis result backend and retrieved on need by API

# How to run

```
cp .env.example .env
```

```
docker-compose build
```
then
```
docker-copose up
```

make a request to `POST http:localhost:5010/tasks` to create first task.
