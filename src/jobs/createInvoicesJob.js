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
   ]
}

function generateRepeatInvoices(planObject, signUpDate, subscriptionStartDate, dateInScaledTime) {
   var monthsSinceSubStartDate = moment(dateInScaledTime).diff(subscriptionStartDate,'months')
   var noOfInvoices = Math.min(monthsSinceSubStartDate, planObject.planLength)
   let invoiceArray = []
   for ( var i = 0; i < noOfInvoices; i++ ) {
      const invoiceDate = i ? moment(subscriptionStartDate).add(i, 'months').toDate() : signUpDate
      invoiceObject =
         {
            _id: ObjectID(),          
            amount: planObject.planCost / planObject.planLength,
            currency: planObject.currency,
            info: {
               status: 'settled',
               date: invoiceDate
            }         
         }
      invoiceArray.push(invoiceObject)  
   }

   return invoiceArray
}

async function createInvoicesForUser(userCollection, userDoc, dateInScaledTime) {   
   const userId = userDoc._id
   const signUpDate = userDoc.signUpDate
   const planObject = userDoc.subscriptions.planType
   const subscriptionStartDate = userDoc.subscriptions.startDate
   
   switch (planObject.paymentType) {
      case 'upfront':
         invoiceArray = generateUpfrontInvoices(planObject, signUpDate)
      break;
      case 'repeat':
         invoiceArray = generateRepeatInvoices(planObject, signUpDate, subscriptionStartDate, dateInScaledTime)
      break;
      default:
      console.log(`Plan payment frequency provided ${planObject.paymentType} is invalid.`);
   }
   
   await userCollection.updateOne(
      {
         _id: userId,         
      },
      {
         $set: { "subscriptions.invoices": invoiceArray }      
      },
   )

   return
}

async function createInvoicesForAllUsers(dateInScaledTime, db) {
   
   const userCollection = db.collection('users')      
   const cursor = userCollection.find({});   
   while(await cursor.hasNext()) {
      const userDoc = await cursor.next();
      
      await createInvoicesForUser(userCollection, userDoc, dateInScaledTime)
   }
   
   return 
};

module.exports = (realTimeStartDate, timeScaleFactor, cronTime, fakeCoStartDate) => async () => {

   console.log(`-----------------------------------------------`)
   console.log(`Creating invoices for users in last cron period`)
   console.log(`-----------------------------------------------`)
   const uri = process.env.MONGODB_URL
   // console.log(uri)
   
   try {      
      const realTimeNow = new Date()
      const secondsPassedInRealTime = moment(realTimeNow).diff(realTimeStartDate,'seconds')
      const secondsPassedInScaledTime = secondsPassedInRealTime * timeScaleFactor
      const dateInScaledTime = moment(fakeCoStartDate).add(secondsPassedInScaledTime,'seconds').toDate()

      console.log(`RT start date: ${realTimeStartDate}`)
      console.log(`RT Now: ${realTimeNow}`)
      console.log(`Seconds passed in RT: ${secondsPassedInRealTime}`)
      console.log(`Seconds passed in ST: ${secondsPassedInScaledTime}`)
      console.log(`Date in ST: ${dateInScaledTime}`)
      
      const client = await MongoClient.connect(uri, { useNewUrlParser: true })
      .catch(err => { console.log(err); });

      if (!client) {
         console.log('Error connect to mongodb')
         return;
      }

      // console.log('Connected to mongodb')

      // Database Name
      const dbName = 'secondNature'; 
      const db = client.db(dbName);   
   
      
      await createInvoicesForAllUsers(dateInScaledTime, db)

      console.log('Inovices updated/created for all users')

      await client.close()
   }
   catch (e) {
      console.log('Error from outer loop')
      console.error(e);
   }
}
