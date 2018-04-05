#!/bin/bash
git add . && git commit -m "$1" && git push heroku rohan:master && heroku logs --tail
