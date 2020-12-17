# The challenge

Thank you for your interest in joining Second Nature! Before inviting you to a technical interview we would like to ask you to complete the challenge below:

> _Up until now company focus has been on making our app world class and therefore the technologies on the backend that go into making that happen, OLTPs etc. But now, as we start to grow rapidly, data and analytics is becoming an increasingly important way for us to distinguish ourselves from competitors. With that in mind, we have started to migrate data from our operational systems (MongoDB) to analytics ones, however this process is not complete._
>
> _We are currently looking at how to move data between operational and analytics environments and what those environments should look like, and this is where we'd like your help! We have a MongoDB database that contains three basic collections:_
>
> 1. _Users (which includes)_
>    1. _Subscriptions_
>    2. _Invoices_
>    3. _Plans_
> 2. _Groups_
> 3. _Messages_
>
> _and we want to get this data out of Mongo DB and into a SQL-like environment with a dashboarding tool on top of it. We want to transform the data into flat tables to allow our wider team to use basic SQL queries to analyse the data. Users are signing up and added to groups all the time plus sending messages in the group chat._

## What we would like from you:

- Create an pipeline that takes data from the Mongo DB instance and exports it to a SQL database of your choice in an environment of your choice
- Your ETL code should be tested in some form
- You should provide a way to test data robustness of the ETL pipeline
- **Bonus1**: Add a UI dashboard on top of this that allows you to answer the following questions:
  - How many users signed up today/this week/this month/ broken down across region, age and gender
  - What proportion of our total userbase is on subscription A vs B.
  - How many messages on average are sent per user and per group per week
- **Bonus2**: you can visualise the success/failure rate of your pipelines

You may use whatever langauage and technologies you like as long as you can explain easily how to run them.

Please fork the repository [here](https://github.com/boz-sn/secondnature-data-challenge) to your own GitHub account. The updated code should then be submitted to your GitHub account and sent through to us for review (add @boz-sn and @danieloj to your repo). We would suggest allocating 3-4 hours to complete the challenge and writing code that you'd be happy to send for code review at your current company. We would expect this to be completed within 1 week of receiving the challenge, if you require longer, please let us know.

We understand that the entire task may not be completeable in 3-4 hours, so please get as far as possible and then summarise in your readme what you'd still like to be completed, and any thoughts you had about challenges or next steps.

Let me know if you have any questions, I'd be happy to help.

Good luck!

Boz

# How to Run

1. Install Docker from `https://docs.docker.com/get-docker/`
2. Run `npm install` from top level of the repository
3. Run `docker-compose up --build` from top level of the repository
4. Run `docker-compose down` from top level of the repository to stop all services

## Notes

The docker compose file spins up 3 services, only 2 of which are critical, the third more for support if needed.

1. `mongo` - this is the container running the mongoDB instance
2. `fake-data` - this is the service that creates fake users, messages and groups
3. `mongo-express` - a UI for inspecting the data in the mongoDB database (you can access this at `localhost:8081`

All 3 services are on the same docker network and expose ports as defined in the `docker-compose.yml` file

The mongoDB instance running within the `mongo` container is exposed via port `27107` which means you can connect to the DB from your **host machine** as you would to a mongoDB instance running on your host machine. In other words using the below at the command line (authentication details provided)

`mongo -u root -p example --authenticationDatabase admin secondNature`

If you add more services via docker-compose, you can connect to the DB from other containers within the network using the container alias `mongo` as the host - i.e. using the details below

```
host: mongo
port: 27017
user: root
password: example
authenticationDatabase: admin
database: secondNature
```

### A note on the fake data creation

The `fake-data` service automatically 'signs up' new users, adds subscriptions to the user, creates groups and adds messages to users. The addition of this data is done in 'sped-up' time, i.e. 10 seconds in the real world will represents several days in the sped-up time. The exact speed is defined by the environment variables below

### Environment variables

Several environment variables are defined for the `fake-data` service within the `docker-compose.yml` file, that you may want to adjust, although the defautls should be acceptable. (Predominantly they only change how realistic numbers are for analysis)

| Variable Name                | Type                       | Description                                                              | Default      |
| ---------------------------- | -------------------------- | ------------------------------------------------------------------------ | ------------ |
| USER_SIGN_UPS_PER_SCALED_DAY | int                        | Number of users who sign up per day in sped-up time                      | 10           |
| REAL_TIME_SECONDS_IN_A_DAY   | int                        | Number of seconds in real time that corresponds to a day in sped-up time | 20           |
| TIME_BETWEEN_CRON_JOBS       | int                        | Time between jobs to add messages and invoices                           | 20           |
| COMPANY_START_DATE           | date string - 'YYYY-MM-DD' | The date you want users to start signing up from                         | '2020-06-01' |
