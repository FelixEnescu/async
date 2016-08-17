

# async
Asynchronous Python Application

You need a linux box to run this example. Make sure you have docker installed. For help installing docker see here: https://docs.docker.com/v1.11/engine/installation/linux/ubuntulinux/

Checkout the source code:

```
$ git clone git@github.com:blueCat1301/async.git
$ cd async
```

Start the application with

```
$ docker-compose up --build
```

This will start the application containers in foreground so you can see the logs. On another terminal test the API:


```
$ curl  -D -  http://localhost:5000/mount/qwe
$ curl  -D -  http://localhost:5000/mount/process
$ curl  -D -  http://localhost:5000/mount/process-status
```

Notes:
 - Application uses Flask with Celery and Redis as queue
 - It is minimal, no checks are performed if for example one tries to launch two processes at same time
 - This is a demo for Sam Hazar

