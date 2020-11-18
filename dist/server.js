"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
require("./utils/env");
const jobs_1 = __importDefault(require("./jobs"));
// import cronLoader from './cron/loader';
const createCronJobs_1 = __importDefault(require("./cron/createCronJobs"));
var poissonProcess = require('poisson-process');
if (!process.env.MONGODB_URL) {
    throw new Error('No MONGODB_URL set');
}
let timer = new Date();
const cronTime = Number(process.env.TIME_BETWEEN_CRON_JOBS); // Seconds between cron job
const msInASecond = 1000;
const secondsInADay = 24 * 60 * 60;
const realTimeStartDate = new Date();
const fakeCoStartDate = new Date(process.env.COMPANY_START_DATE);
const realTimeSecsInADay = Number(process.env.REAL_TIME_SECONDS_IN_A_DAY); // Number of seconds in real time that represent a day - i.e. 10 => 10 seconds in real time = 24 hours
const timeScaleFactor = secondsInADay / realTimeSecsInADay;
const usersPerDay = Number(process.env.USER_SIGN_UPS_PER_SCALED_DAY);
const msBetweenSignUpsInScaledTime = msInASecond * secondsInADay / usersPerDay;
const msBetweenSignUpsInRealTime = msBetweenSignUpsInScaledTime / timeScaleFactor;
console.log(`Scale factor = ${timeScaleFactor}`);
console.log(`ms between sign ups in scaled time = ${msBetweenSignUpsInScaledTime}`);
console.log(`ms between sign ups in real time = ${msBetweenSignUpsInRealTime}`);
// Poisson process that creates sign-ups randomly
var signUpPoissionProcess = poissonProcess.create(msBetweenSignUpsInRealTime, function call() {
    return __awaiter(this, void 0, void 0, function* () {
        jobs_1.default.createUsersJob(realTimeStartDate, fakeCoStartDate, timeScaleFactor, timer);
        timer = new Date();
    });
});
signUpPoissionProcess.start();
// Create cron jobs that add messages and invoices
createCronJobs_1.default(cronTime, realTimeStartDate, timeScaleFactor, fakeCoStartDate);
//# sourceMappingURL=server.js.map