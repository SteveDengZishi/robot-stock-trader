#!/bin/bash
git add . && git commit -m "$1"
git push heroku rohan-algo:master
heroku logs --tail
