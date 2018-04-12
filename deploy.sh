#!/bin/bash
git push heroku rohan:master && heroku logs --tail
