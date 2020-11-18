var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var ObjectID = require('mongodb').ObjectID;
const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');
var faker = require('faker/locale/en_GB');
var chance = require('chance').Chance();
const moment = require('moment');
var poissonProcess = require('poisson-process');
function generateUpfrontInvoices(planObject, signUpDate) {
    return [
        {
            _id: ObjectID(),
            amount: planObject.planCost,
            currency: planObject.currency,
            info: {
                status: 'settled',
                date: signUpDate
            }
        }
    ];
}
function generateRepeatInvoices(planObject, signUpDate, subscriptionStartDate, dateInScaledTime) {
    var monthsSinceSubStartDate = moment(dateInScaledTime).diff(subscriptionStartDate, 'months');
    var noOfInvoices = Math.min(monthsSinceSubStartDate, planObject.planLength);
    let invoiceArray = [];
    for (var i = 0; i < noOfInvoices; i++) {
        const invoiceDate = i ? moment(subscriptionStartDate).add(i, 'months').toDate() : signUpDate;
        invoiceObject =
            {
                _id: ObjectID(),
                amount: planObject.planCost / planObject.planLength,
                currency: planObject.currency,
                info: {
                    status: 'settled',
                    date: invoiceDate
                }
            };
        invoiceArray.push(invoiceObject);
    }
    return invoiceArray;
}
function createInvoicesForUser(userCollection, userDoc, dateInScaledTime) {
    return __awaiter(this, void 0, void 0, function* () {
        const userId = userDoc._id;
        const signUpDate = userDoc.signUpDate;
        const planObject = userDoc.subscriptions.planType;
        const subscriptionStartDate = userDoc.subscriptions.startDate;
        switch (planObject.paymentType) {
            case 'upfront':
                invoiceArray = generateUpfrontInvoices(planObject, signUpDate);
                break;
            case 'repeat':
                invoiceArray = generateRepeatInvoices(planObject, signUpDate, subscriptionStartDate, dateInScaledTime);
                break;
            default:
                console.log(`Plan payment frequency provided ${planObject.paymentType} is invalid.`);
        }
        yield userCollection.updateOne({
            _id: userId,
        }, {
            $set: { "subscriptions.invoices": invoiceArray }
        });
        return;
    });
}
function createInvoicesForAllUsers(dateInScaledTime, db) {
    return __awaiter(this, void 0, void 0, function* () {
        const userCollection = db.collection('users');
        const cursor = userCollection.find({});
        while (yield cursor.hasNext()) {
            const userDoc = yield cursor.next();
            yield createInvoicesForUser(userCollection, userDoc, dateInScaledTime);
        }
        return;
    });
}
;
module.exports = (realTimeStartDate, timeScaleFactor, cronTime, fakeCoStartDate) => () => __awaiter(this, void 0, void 0, function* () {
    console.log(`-----------------------------------------------`);
    console.log(`Creating invoices for users in last cron period`);
    console.log(`-----------------------------------------------`);
    const uri = process.env.MONGODB_URL;
    // console.log(uri)
    try {
        const realTimeNow = new Date();
        const secondsPassedInRealTime = moment(realTimeNow).diff(realTimeStartDate, 'seconds');
        const secondsPassedInScaledTime = secondsPassedInRealTime * timeScaleFactor;
        const dateInScaledTime = moment(fakeCoStartDate).add(secondsPassedInScaledTime, 'seconds').toDate();
        console.log(`RT start date: ${realTimeStartDate}`);
        console.log(`RT Now: ${realTimeNow}`);
        console.log(`Seconds passed in RT: ${secondsPassedInRealTime}`);
        console.log(`Seconds passed in ST: ${secondsPassedInScaledTime}`);
        console.log(`Date in ST: ${dateInScaledTime}`);
        const client = yield MongoClient.connect(uri, { useNewUrlParser: true })
            .catch(err => { console.log(err); });
        if (!client) {
            console.log('Error connect to mongodb');
            return;
        }
        // console.log('Connected to mongodb')
        // Database Name
        const dbName = 'secondNature';
        const db = client.db(dbName);
        yield createInvoicesForAllUsers(dateInScaledTime, db);
        console.log('Inovices updated/created for all users');
        yield client.close();
    }
    catch (e) {
        console.log('Error from outer loop');
        console.error(e);
    }
});
//# sourceMappingURL=createInvoicesJob.js.map