# Second Nature
Practical test by Vitali Lupusor

## Overview
The application will extract collections from a MongoDB database based on a partitioning criteria. Then, the extract is flattened and the output saved locally. This triggers two concurrent task:  
  - upload the initial extract to a Google Cloud Storage bucket (Data Lake)  
  - upload the flattened file to a BigQuery table.   
 
The application is set up as a batch job that is scheduled to run daily at 00:00. With the commands listed below, we will trigger the app to backfill the tables starting with 2020-06-01 (COMPANY_START_DATE) and 2020-06-10 as end date.  
The end date is chosen close to start date in order to reduce the amount of time the app will be running, but it can be increased up to current date, in which case the app will update the BigQuery tables with data that was generated between start date and current date - 1 day (if today is 2020-11-22, cut off date 2020-11-21 23:59:59).

## How to Run

1. Install Docker from `https://docs.docker.com/get-docker/`
2. Run `npm install` from top level of the repository
3. Run `docker-compose up --build` from top level of the repository
4. Run `docker-compose down` from top level of the repository to stop all services
5. Allow docker to run for a few minutes in order to generate enough fake data. In the meanwhile proceed with the below. 
6. Create a new environement with tools like conda or pyenv or virtualenv.
7. Actiave the environment and run `pip install -r requirement.txt`.
    - Note: not all libraries in the `./requirements.txt` file are mandatory, as didn't have time to filter out the unnecessary ones.
8. Install Apache Airflow `https://airflow.apache.org/docs/stable/start.html`.
9. In `~/airflow/airflow.cfg` change the value of `dags_folder` to the top level of this application.
10. Check your email for the decryption passphrase and impliment one of the below options:
    - Inside `./config.py` replace the `PASSPHRASE` value with the phrase from the email.
    - In the shell you will execute the application from run `export PASSPHRASE='REPLACE ME WITH THE PASSPHRASE FROM THE EMAIL'`
11. Run `airflow backfill data_migration -s 2020-06-01 -e 2020-06-10`.  
    - This will trigger the app.
12. In order to visualise every step of the application, head over to `localhost:8080`
    - Given than you have run `airflow webserver -p 8080`

## Futere improvements
1. Due to time restrictions I was not able to engineer all the collections (only users is working), so a natural next step is to develop the logic for the rest of them.
2. Add logs for an easier debugging.
3. Add more unit tests for the same purpose as above.
4. Improve the security aspect:
    - Hide sensite information in a vault (example Google Secret Manager)
    - Use a better encryption mechanism (example GnuPG)
    - Use `customer-supplie` encryption key for an elivated security
5. Set up an SMTP to send email notification on the status if the tasks.
6. Comment the code in a more explicit manner.
7. Push the ETL of the extracts to the cloud.
    - Create a docker image with a tailored code and set it up on a service like to Google Cloud App Engine or Kubernetes.
    - Make it event driven as opposed to scheduled task.
