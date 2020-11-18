var ObjectID = require('mongodb').ObjectID;
const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');
var faker = require('faker/locale/en_GB');
var chance = require('chance').Chance();
const moment = require('moment');
var poissonProcess = require('poisson-process');

function getMessageDate(signUpDate, latestMessageDate, thisTimeBetweenMessages) {
   if (!latestMessageDate) {
      return moment(signUpDate).add(thisTimeBetweenMessages, 'ms').toDate()
   }
   else {
      return moment(latestMessageDate).add(thisTimeBetweenMessages, 'ms').toDate()
   }
}

async function createMessages(realTimeStartDate, timeScaleFactor, cronTime, fakeCoStartDate, db) {   

   const userCollection = db.collection('users')
   console.log(`Real time start date: ${realTimeStartDate}`)

   const cursor = userCollection.find({});
   while(await cursor.hasNext()) {
      const userDoc = await cursor.next();
      const userId = userDoc._id
      const signUpDate = userDoc.signUpDate
      const groupId = userDoc.groupId
      const messagesPerDay = userDoc.fakeDataHelpers.messagesPerDay
      
      // console.log(`-----------------------------------------------`)
      // console.log(`Creating messages for next user, ID: ${userId}`)
      // console.log(`-----------------------------------------------`)
      // console.log(`User sign up date: ${signUpDate}`)
      // console.log(`User group ID: ${groupId}`)
      // console.log(`User messages per day: ${messagesPerDay}`)
      
      const scaledMsSinceLastCronJob = cronTime * timeScaleFactor * 1000
      // console.log(`Scaled time since last cron in seconds: ${scaledMsSinceLastCronJob}`)
      const scaledMsBetweenMessages = 24*60*60*1000/messagesPerDay // TODO: change to constants
      let totalMsFromMessages = 0
      while (totalMsFromMessages<scaledMsSinceLastCronJob) {
         // console.log(`Scaled time since last cron in seconds: ${scaledMsSinceLastCronJob}`)
         const thisTimeBetweenMessages = poissonProcess.sample(scaledMsBetweenMessages)
         // console.log(`Time between messages from poisson: ${thisTimeBetweenMessages}`)
         totalMsFromMessages += thisTimeBetweenMessages
         // console.log(`Total time between messages: ${totalMsFromMessages}`)
         // console.log(totalMsFromMessages<scaledMsSinceLastCronJob)
                  
         const messageCollection = db.collection('messages')
         const userMessages = await messageCollection.findOne({userId: userId, groupId: groupId})
         const latestMessageDate = userMessages ? userMessages.latestMessageDate: 0
         const messageDate = getMessageDate(signUpDate, latestMessageDate, thisTimeBetweenMessages)

         await messageCollection.updateOne(
            {
               userId: userId,
               groupId: groupId
            },
            {
               $set: {
                  latestMessageDate: messageDate,                  
               },
               $push: {
                  messages: {
                     messageDate: messageDate,
                     message: chance.string({ length: chance.integer({ min: 0, max: 40 })}),
                  }
               }
            },
            {
               upsert: true
            }
         )
      }      

   }   
   return
}

module.exports = (realTimeStartDate, timeScaleFactor, cronTime, fakeCoStartDate) => async () => {

   console.log(`-----------------------------------------------`)
   console.log(`Adding messages for users in last cron period`)
   console.log(`-----------------------------------------------`)
   const uri = process.env.MONGODB_URL
   // console.log(uri)
   
   try {      
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
   
      await createMessages(realTimeStartDate, timeScaleFactor, cronTime, fakeCoStartDate, db)

      console.log('Messages updated/created for all users')

      await client.close()
   }
   catch (e) {
      console.log('Error from outer loop')
      console.error(e);
   }
}
