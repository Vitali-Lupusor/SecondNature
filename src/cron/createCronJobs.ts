import createCronJob from '../utils/createCronJob';
import jobs from '../jobs';
import { Int32 } from 'mongodb';

export default function createCronJobs(cronTime: Int32, realTimeStartDate: Date, timeScaleFactor: Number, fakeCoStartDate: Date): void {
  console.log('Creating cron jobs');

  createCronJob(`*/${cronTime} * * * * *`, jobs.createMessagesJob(realTimeStartDate, timeScaleFactor, cronTime, fakeCoStartDate));

  createCronJob(`*/${cronTime} * * * * *`, jobs.createInvoicesJob(realTimeStartDate, timeScaleFactor, cronTime, fakeCoStartDate));  
}
