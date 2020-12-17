# Second Nature
Practical test by Vitali Lupusor

## Overview
The application will extract collections from a MongoDB database based on a partitioning criteria. Then, the extract is flattened and the output saved locally. This triggers two concurrent task:  
  - upload the initial extract to a Google Cloud Storage bucket (Data Lake)  
  - upload the flattened file to a BigQuery table.   
 
The application is set up as a batch job that is scheduled to run daily at 00:00. With the commands listed below, we will trigger the app to backfill the tables starting with 2020-06-01 (COMPANY_START_DATE) and 2020-06-10 as end date.  
The end date is chosen close to start date in order to reduce the amount of time the app will be running, but it can be increased up to current date, in which case the app will update the BigQuery tables with data that was generated between start date and current date - 1 day (if today is 2020-11-22, cut off date 2020-11-21 23:59:59).  

There is an actual Google Gloud Platofrm project set up for this application, so when the commands are executed real actions take place.  
The credentials for the account are encrypted with Fernet cryptography, the key to which is going to be sent in a separate email. No actions to decryp the credentials are required as everything is fully automated. The set credentials will expire on 2020-12-01.  

The application has a centralised configuration file `./config.py` where you can amend the current settings.

## How to Run

1. Install Docker from `https://docs.docker.com/get-docker/`
2. Run `npm install` from top level of the repository
3. Run `docker-compose up --build` from top level of the repository
4. Allow docker to run for a few minutes in order to generate enough fake data. In the meanwhile proceed with the below.
5. Run `docker-compose down` from top level of the repository to stop all services
6. Create a new environement with tools like conda or pyenv or virtualenv.
7. Actiave the environment and run `pip install -r requirement.txt`.
    - Note: not all libraries in the `./requirements.txt` file are mandatory, as didn't have time to filter out the unnecessary ones.
8. Install Spark.  
    - Run `curl --silent -O https://downloads.apache.org/spark/spark-3.0.1/spark-3.0.1-bin-hadoop3.2.tgz`
    - To unpack the archive run `tar xvf spark-3.0.1-bin-hadoop3.2.tgz`
    - Set up the environment variables `export SPARK_HOME={PATH TO WHERE YOU UNPACTED THE SPARK ARCHIVE}/spark-3.0.1-bin-hadoop3.2 && export PYSPARK_PYTHON={PYTHON 3 INTERPRETER TO RUN SPARK} && export JAVA_HOME={PATH TO JAVA 11}`
9. Install Apache Airflow `https://airflow.apache.org/docs/stable/start.html`.
10. In `~/airflow/airflow.cfg` change the value of `dags_folder` to the top level of this application.
11. Check your email for the decryption passphrase and impliment one of the below options:
    - Inside `./config.py` replace the `PASSPHRASE` value with the phrase from the email.
    - In the shell you will execute the application from run `export PASSPHRASE='REPLACE ME WITH THE PASSPHRASE FROM THE EMAIL'`
12. Run `airflow backfill data_migration -s 2020-06-01 -e 2020-06-10`.  
    - This will trigger the app.
13. In order to visualise every step of the application, head over to `localhost:8080`
    - Given than you have run `airflow webserver -p 8080`
14. (Optional) If you want to see the data from the BigQuery table that you just populated, run `python ./query_bq.py`.

## Futere improvements
1. Create a Dockerfile to easily install all the dependencies
2. Due to time restrictions I was not able to engineer all the collections (only users is working), so a natural next step is to develop the logic for the rest of them.
3. Create a dashboard to visualise insights based on the created pipelines.
4. Add logs for an easier debugging.
5. Add unit tests for a smooth CI/CD.
6. Improve the security aspect:
    - Hide sensite information in a vault (example Google Secret Manager)
    - Use a better encryption mechanism (example GnuPG)
    - Use `customer-supplie` encryption key for an elivated security
7. Set up an SMTP to send email notification on the status if the tasks.
8. Comment the code in a more explicit manner.
9. Push the ETL of the extracts to the cloud.
    - Create a docker image with a tailored code and set it up on a service like to Google Cloud App Engine or Kubernetes.
    - Make it event driven as opposed to scheduled task.
