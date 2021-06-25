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

| Path                	| Method 	| Purpose                              	| Data (Body)                                        	|
|---------------------	|--------	|--------------------------------------	|----------------------------------------------------	|
| /api/register/      	| POST   	| Register a new user                  	| email, password, first_name, last_name             	|
| /api/token/         	| POST   	| Get a pair of JWT tokens (Login)     	| username, password, client_id, client_secret, grant_type  |
| /api/convert-token    | POST      | Send google oauth2 access token to backend | token, backend: "google-oauth2", client_id, client_secret, grant_type: "convert_token"   |
| /api/token/refresh/ 	| POST   	| Get new Access token (Token Refresh) 	| refresh                                            	|
| /api/profile/       	| GET    	| Get profile data       	            | -                                                  	|
| /api/profile/       	| PUT   	| Create/Update your profile            | image, dob(yyyy-mm-dd), bio, tags[array<str>], location[array<float>] 	|
| /api/profile/\<userid\> | GET    	| Get specific user's profile           | - (\<userid\> must be replaced with an integer value) |
| /api/post/          	| POST   	| Create a new post(blog thingy)       	| image, title, desc                                 	|
| /api/event/          	| POST   	| Create a new event                   	| image, title, desc, event_date(yyyy-mm-dd), addr, location[array<float>], tags[array<str>], max_attendees | 
| /api/event/          	| GET   	| Get all available events              | -                                                     | 
| /api/event/join/\<event-id\>      | POST  | Join an event                         | -                                                     | 
| /api/event/accept/\<event-id\>    | POST  | Accept the join request                         | userid                                                     | 
| /api/getRecommendation          	| GET   	| Get events within 50kms of a particular event              | event                                                     | 
| /api/post/          	| POST   	| Create a new post(blog thingy)       	| image, title, desc                                 	|

To generate `client_id` and `client_secret` go to the admin page -> Application -> Add Application

Parameters Description: _datatypes within sqared brackets[]_
+ `email`: Email address [string]
+ `username`: Email address [string]
+ `password`: 8+ characters [string]
+ `grant_type`: "password" when sending POST request to /api/token/ and "convert_token" when POSTing to /api/convert-token
+ `refresh`: Refresh token obtained after POST /api/token/ [string]
+ `image`: Image File to be uploaded [file]
+ `dob`: Date Of Birth. (yyyy-mm-dd) [date/string]
+ `bio`: Biography [string]
+ `tags`: Array of strings. [array<string>] eg: ['ski', 'boating', 'gaming']
+ `location`: Array of floating points. (x-axis, y-axis) [array<float>] eg: [12.885151, 74.825905]
+ `title`: Title of the post [string]
+ `desc`: Post body [string]
+ `event_date`: Date with formate (yyyy-mm-dd)
+ `addr`: Address of event. [string]
+ `max_attendees`: Interger field [int]
+ `event-id`: EventID [int]
