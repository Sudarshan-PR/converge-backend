## Converge

Backend for the Converge Mobile App [College Project]

- - - 
Uses Django 3.1 and DRF 3.12 along with PostGIS for PostgreSQL

**NOTE** : Set environment variables `SECRET_KEY` `DEBUG` `DATABASE_NAME` `DATABASE_USER` `DATABASE_PASSWORD` `DATABASE_HOST` `DATABASE_PORT` `AWS_ACCESS_KEY` `AWS_SECRET_KEY` `S3_BUCKET_NAME` `AWS_REGION_NAME` 
Install PostGIS extension in PostgreSQL for Geo Objects support.

- - - 
##### Start Server
`gunicorn Converge.wsgi`

- - - 

