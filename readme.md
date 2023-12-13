## Using the API
You can use the API from a browser from here https://ml6karel-uzv3utyvga-uc.a.run.app . The API uses OAuth 2.0 as a way to keep it secure. You need to use on email from the domain ml6.eu in order to gain access. There are 2 API calls implemented, 1 called analyze which takes in a string and returns a json construct containing the sentiment of the string and the confidence about this classification. The other one is called get_all_analyzes, which returns all the analyzes the application has done so far. It can take in a limit to limit the amount the number of analyzes you get it. The application saves and retrieves the analyzes in a firestore database.

## Running locally
First replace account_key_file in "database_functions.py" and client_secrets_file in "app.py" with the name of your own files. Secondly replace all the variables set to "fill me in" with the proper values.
You can run the application using 'python3 app.py' or you can use docker. In order to use docker you first build using 'docker built -t ml6sentiment'. Then you run the container with 'docker run -p 8080:8080 --name ml6sentiment ml6sentiment'. To get an overview of the supported API calls visit localhost:8080 in your browser.

## Improvements I could still make
If I spend more time on it I would make the following improvements. 
1) Using Terraform to manage the gcloud environment. I prefer this over doing stuff manually, because it is easier to keep track over how the infrastucture evolves over time.
2) Clean up the way I keep HTML content