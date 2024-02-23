# Example recruitment task
## Docker

Setup is really easy as there is just Dockerfile.

By default, the Docker will expose port 8000, so change this within the
Dockerfile if necessary. When ready, simply use the Dockerfile to
build the image.

If you're in directory with Dockerfile root then execute these:
```sh
docker build -t example_name .
```

This will create the app image and pull in the necessary dependencies.


Once done, run the Docker image.

```sh
docker run -p 8000:8000 example_name
```


> Note: App will automatically fill database with mock-up data frrom `fixtures` directory.

Verify the deployment by navigating to your server address in
your preferred browser.

```sh
127.0.0.1:8000
```


## Api endpoints

### Authentication
> Note: App will automatically create superuser from  data in .env.example file which is **username: admin, password: admin**. If you want to change password you can od it in .env file.

In order to obatin authorization access to create/update/delete objects you need to create (or use automatically created superuser one) an account by POST method api call at `/api/auth/register/`

You can visit the endpoint and fill content with 
```json
{
    "username": "new_user",
    "password": "password123"
}
```
or use curl in terminal.
```sh
curl -X POST http://localhost:8000/api/auth/register/ -H "Content-Type: application/json" -d "{\"username\": \"new_user\", \"password\": \"password123\"}"

```

After this you can continue using application within your browser by firstly logging in on `/api/auth/login` endpoint and then visiting `/api/`, or you can get access token used for authorization when using raw api calls, for e.g. with curl by making POST api call at `api/auth/api-token-auth/`
```sh
curl -X POST http://localhost:8000/api/auth/api-token-auth/ -H "Content-Type: application/json" -d "{\"username\": \"your_username\", \"password\": \"your_password\"}"
```
### Browsing data
After logging in, or acquiring token you have access to all CRUD opeartions on data.
> Quick reminder that app automatically loads example data to database during creation of docker container.

You can browse either categories (`/api/categories/`) or tasks (`/api/tasks/`).

There is also posibility of filtering tasks by specific category by adding query parameter for e.g. `/api/tasks/?category=1/`

For detail view about given task visit `/api/tasks/<pk>/` where pk is id of task object.


## Tests
There is set of tests available for each viewset.
These can easily be access by going into docker container shell and executing:
```sh
python manage.py test
```

## License
MIT
