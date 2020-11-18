
function makeName(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
       result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
 }

function getRandomInt(min, max) {
   min = Math.ceil(min);
   max = Math.floor(max);
   return Math.floor(Math.random() * (max - min + 1)) + min;
}

function getRandomGender() {
   const genderSwitch = getRandomInt(0,1)
   return genderSwitch ? 'm' : 'f'
}

function getRandomGender() {
   const genderSwitch = getRandomInt(0,1)
   return genderSwitch ? 'm' : 'f'
}

function createExampleUsers(numberOfUsers) {
   for ( var i = 0; i < numberOfUsers; i++ ) 
   {
      db.user.save({ 
         firstname: makeName(5),
         lastname: makeName(6),
         age: getRandomInt(18,87),
         gender: getRandomGender(),
         country: 'ToBeReplaced',
         postCode: 'ToBeReplaced',
         subscriptions: [
            {
               _id: 'tbd', 
               subscriptionID: 'tbd',
               startDate: 'tbd',
               planType: {
                  _id: 'tbd',
                  planID: 'tbd',
                  planType: 'tbd',
                  planCost: 'tbd'
               },
               invoices: [
                  {
                     _id: 'tbd',
                     amount: 'tbd',
                     currency: 'tbd',
                     status: 'settled'
                  }
               ]
            }
         ],
         groups: [
            {
               _id: 'tbd',
               groupID: 'tbd',
               messages: [
                  {
                     _id: 'tbd',
                     dateSent: 'tbd',
                     messageText: 'string'
                  }
               ],
               healthCoach: 'tbd'
            }
         ]
      })
   }
}

 createExampleUsers(10000)