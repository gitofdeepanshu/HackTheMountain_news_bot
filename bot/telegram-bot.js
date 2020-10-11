var TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');

const options = {
  webHook: {
    // Port to which you should bind is assigned to $PORT variable
    // See: https://devcenter.heroku.com/articles/dynos#local-environment-variables
    port: process.env.PORT || 5000
    // you do NOT need to set up certificates since Heroku provides
    // the SSL certs already (https://<app-name>.herokuapp.com)
    // Also no need to pass IP because on Heroku you need to bind to 0.0.0.0
  }
};

const TOKEN = process.env.TOKEN || 'YOUR_TELEGRAM_BOT_TOKEN';
const bot = new TelegramBot(token, options);


bot.on('message' , (msg) =>{
    var text = msg.text.toString();
    axios
    .post('https://glacial-depths-57528.herokuapp.com/find_news' , {
        data : text
    })
    .then(res =>{
        console.log(`statusCode: ${res.statusCode}`);
        console.log(res);
        const response = res.data.url;
        if(response === null ){
            bot.sendMessage(msg.chat.id, "Creditable News Source not found ❌"); 
        }
        else {
            bot.sendMessage(msg.chat.id, 'News Verified ✅ \n Source: Times of India');
            bot.sendMessage(msg.chat.id, response); 

        }
        
    })
    .catch(error => {
            console.error(error)
     })

})
