var TelegramBot = require('node-telegram-bot-api');
var token = process.env.TOKEN;
const bot = new TelegramBot(token, {polling: true});
const axios = require('axios');


bot.on('message' , (msg) =>{
    var text = msg.text.toString();
    axios
    .post('http://728eb4fa62ae.ngrok.io/find_news' , {
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
