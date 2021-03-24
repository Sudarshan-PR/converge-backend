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

##### Endpoints

| Path                	| Method 	| Purpose                              	| Params/Values                                      	|
|---------------------	|--------	|--------------------------------------	|----------------------------------------------------	|
| /api/register/      	| POST   	| Register a new user                  	| email, password, first_name, last_name             	|
| /api/token/         	| POST   	| Get a pair of JWT tokens (Login)     	| email, password                                    	|
| /api/token/refresh/ 	| POST   	| Get new Access token (Token Refresh) 	| refresh                                            	|
| /api/profile/       	| GET    	| Get profile info if available        	| -                                                  	|
| /api/profile/       	| POST   	| Create a profile                     	| dob, bio, tags[array<str>], location[array<float>] 	|
| /api/post/          	| POST   	| Create a new post(blog thingy)       	| image, title, desc                                 	|
