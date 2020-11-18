import './utils/env';
import jobs from './jobs';
// import cronLoader from './cron/loader';
import createCronJobs from './cron/createCronJobs';


var poissonProcess = require('poisson-process');


if (!process.env.MONGODB_URL) {
  throw new Error('No MONGODB_URL set');
}

let timer = new Date();

const cronTime:number = Number(process.env.TIME_BETWEEN_CRON_JOBS!) // Seconds between cron job
const msInASecond = 1000
const secondsInADay = 24*60*60
const realTimeStartDate = new Date()
const fakeCoStartDate = new Date(process.env.COMPANY_START_DATE!)
const realTimeSecsInADay:number = Number(process.env.REAL_TIME_SECONDS_IN_A_DAY!) // Number of seconds in real time that represent a day - i.e. 10 => 10 seconds in real time = 24 hours
const timeScaleFactor = secondsInADay / realTimeSecsInADay
const usersPerDay:number = Number(process.env.USER_SIGN_UPS_PER_SCALED_DAY!)
const msBetweenSignUpsInScaledTime = msInASecond * secondsInADay / usersPerDay
const msBetweenSignUpsInRealTime = msBetweenSignUpsInScaledTime / timeScaleFactor

console.log(`Scale factor = ${timeScaleFactor}`)
console.log(`ms between sign ups in scaled time = ${msBetweenSignUpsInScaledTime}`)
console.log(`ms between sign ups in real time = ${msBetweenSignUpsInRealTime}`)

// Poisson process that creates sign-ups randomly
var signUpPoissionProcess = poissonProcess.create(msBetweenSignUpsInRealTime, async function call() {
  jobs.createUsersJob(realTimeStartDate, fakeCoStartDate, timeScaleFactor, timer)
  timer = new Date();
}
)

signUpPoissionProcess.start()

// Create cron jobs that add messages and invoices
createCronJobs(cronTime, realTimeStartDate, timeScaleFactor, fakeCoStartDate);
