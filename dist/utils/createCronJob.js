"use strict";
/**
 * This function registers a cron job.
 *
 * The reason we use a function rather than calling the CronJob constructor directly in cron.js
 * is to extract the onlyRunInProduction logic from the jobs themselves so that we can write test
 * for jobs without having to set NODE_ENV=production in our test environment.
 */
Object.defineProperty(exports, "__esModule", { value: true });
const cron_1 = require("cron");
const createCronJob = (cronTime, job) => {
    try {
        const timezone = 'Europe/London';
        new cron_1.CronJob(cronTime, job, null, true, timezone);
    }
    catch (err) {
        console.log(`Error creating cron job: ${err}`);
    }
};
exports.default = createCronJob;
//# sourceMappingURL=createCronJob.js.map