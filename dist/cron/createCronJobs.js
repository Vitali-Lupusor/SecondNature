"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const createCronJob_1 = __importDefault(require("../utils/createCronJob"));
const jobs_1 = __importDefault(require("../jobs"));
function createCronJobs(cronTime, realTimeStartDate, timeScaleFactor, fakeCoStartDate) {
    console.log('Creating cron jobs');
    createCronJob_1.default(`*/${cronTime} * * * * *`, jobs_1.default.createMessagesJob(realTimeStartDate, timeScaleFactor, cronTime, fakeCoStartDate));
    createCronJob_1.default(`*/${cronTime} * * * * *`, jobs_1.default.createInvoicesJob(realTimeStartDate, timeScaleFactor, cronTime, fakeCoStartDate));
}
exports.default = createCronJobs;
//# sourceMappingURL=createCronJobs.js.map