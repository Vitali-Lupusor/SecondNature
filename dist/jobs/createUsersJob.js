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
function generateRandomPlan() {
    // Hard coded plan types
    const planTypesArray = [
        {
            _id: ObjectID(),
            planID: '1234',
            planDescription: 'CoreTechMonthly',
            planCost: 120,
            currency: 'GBP',
            planLength: 3,
            planLengthUnits: 'months',
            paymentType: 'repeat'
        },
        {
            _id: ObjectID(),
            planID: '1235',
            planDescription: 'CoreTechUpfront',
            planCost: 150,
            currency: 'GBP',
            planLength: 3,
            planLengthUnits: 'months',
            paymentType: 'upfront'
        },
        {
            _id: ObjectID(),
            planID: '2234',
            planDescription: 'CoreNoTechMonthly',
            planCost: 90,
            currency: 'GBP',
            planLength: 3,
            planLengthUnits: 'months',
            paymentType: 'repeat'
        },
        {
            _id: ObjectID(),
            planID: '2235',
            planDescription: 'CoreNoTechUpfront',
            planCost: 120,
            currency: 'GBP',
            planLength: 3,
            planLengthUnits: 'months',
            paymentType: 'upfront'
        }
    ];
    var randomPlanType = planTypesArray[Math.floor(Math.random() * planTypesArray.length)];
    return randomPlanType;
}
;
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
function generateRepeatInvoices(planObject, signUpDate, subscriptionStartDate) {
    var diff = moment(new Date()).diff(subscriptionStartDate, 'months');
    var noOfInvoices = Math.min(diff, planObject.planLength);
    let invoiceArray = [];
    for (var i = 0; i <= noOfInvoices; i++) {
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
function generateInvoices(planObject, signUpDate, subscriptionStartDate) {
    let invoiceArray = [];
    switch (planObject.paymentType) {
        case 'upfront':
            invoiceArray = generateUpfrontInvoices(planObject, signUpDate);
            break;
        case 'repeat':
            invoiceArray = generateRepeatInvoices(planObject, signUpDate, subscriptionStartDate);
            break;
        default:
            console.log(`Plan payment frequency provided ${planObject.paymentType} is invalid.`);
    }
    return invoiceArray;
}
;
function generateSubscriptionStartDate(randomSignUpDate) {
    const minSubscriptionStartDate = moment(randomSignUpDate).startOf('isoWeek').add(1, 'weeks').toDate();
    const maxSubscriptionStartDate = moment(randomSignUpDate).startOf('isoWeek').add(4, 'weeks').toDate();
    const randomSubscriptionStartDate = faker.date.between(minSubscriptionStartDate, maxSubscriptionStartDate);
    const randomSubscriptionStartDateMonday = moment(randomSubscriptionStartDate).startOf('isoWeek').toDate();
    return randomSubscriptionStartDateMonday;
}
function generateSubscription(signUpDate) {
    const subscriptionStartDate = generateSubscriptionStartDate(signUpDate);
    const randomPlan = generateRandomPlan();
    // const invoices = generateInvoices(randomPlan, signUpDate, subscriptionStartDate)
    const invoices = [];
    const subscriptions = {
        _id: ObjectID(),
        subscriptionID: ObjectID(),
        startDate: subscriptionStartDate,
        planType: randomPlan,
        invoices: invoices
    };
    return {
        subscriptions,
        subscriptionStartDate
    };
}
function createGroup(subscriptionStartDate, db) {
    return __awaiter(this, void 0, void 0, function* () {
        const groupCollection = db.collection('groups');
        let group = yield groupCollection.findOne({ startDate: subscriptionStartDate });
        let groupId = '';
        if (group) {
            console.log('Group for this start date already exists, getting group ID');
            groupId = group._id;
        }
        else {
            console.log('Group does not exist yet for this start date, creating one');
            const groupInfo = yield groupCollection.insertOne({
                startDate: subscriptionStartDate,
                healthCoach: chance.pickone(['Bob A', 'Alice C', 'Charlie D', 'Daisy E'])
            });
            groupId = groupInfo.insertedId;
        }
        return groupId;
    });
}
function createExampleUsers(numberOfUsers, dateInScaledTime, db) {
    return __awaiter(this, void 0, void 0, function* () {
        for (var i = 0; i < numberOfUsers; i++) {
            const userSignUpDate = dateInScaledTime;
            const { subscriptions, subscriptionStartDate } = generateSubscription(userSignUpDate);
            const groupId = yield createGroup(subscriptionStartDate, db);
            const randomNumMessagesPerDay = chance.integer({ min: 1, max: 10 });
            const userCollection = db.collection('users');
            const user = yield userCollection.insertOne({
                firstname: faker.name.firstName(),
                lastname: faker.name.lastName(),
                age: chance.age({ type: 'adult' }),
                gender: chance.gender(),
                country: faker.address.countryCode(),
                postCode: chance.postcode(),
                signUpDate: userSignUpDate,
                subscriptions: subscriptions,
                groupId: ObjectID(groupId),
                fakeDataHelpers: {
                    messagesPerDay: randomNumMessagesPerDay
                }
            });
            const userId = user.insertedId;
        }
    });
}
module.exports = (realTimeStartDate, fakeCoStartDate, timeScaleFactor, timer) => __awaiter(this, void 0, void 0, function* () {
    console.log(`A user is about to sign up - time since last sign up = ${(new Date().getTime() - timer.getTime()) / 1000} seconds`);
    const uri = process.env.MONGODB_URL;
    console.log(uri);
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
            return;
        }
        // Database Name
        const dbName = 'secondNature';
        const db = client.db(dbName);
        const numberOfUsersToCreate = 1;
        yield createExampleUsers(numberOfUsersToCreate, dateInScaledTime, db);
        yield client.close();
    }
    catch (e) {
        console.error(e);
    }
});
//# sourceMappingURL=createUsersJob.js.map