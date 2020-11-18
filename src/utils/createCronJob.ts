/**
 * This function registers a cron job.
 *
 * The reason we use a function rather than calling the CronJob constructor directly in cron.js
 * is to extract the onlyRunInProduction logic from the jobs themselves so that we can write test
 * for jobs without having to set NODE_ENV=production in our test environment.
 */

import { CronJob } from 'cron';

const createCronJob = (
  cronTime: string,
  job: () => void,
): void => {
  try {
    const timezone = 'Europe/London'

    new CronJob(cronTime, job, null, true, timezone);
  } catch (err) {
    console.log(`Error creating cron job: ${err}`);
  }
};

export default createCronJob;
