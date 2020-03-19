var Discord = require('discord.io');
var logger = require('winston');
var auth = require('./auth.json');
const messageHandlers = require('./messageHandlers')
console.log ("imported message handlers: ")
console.log(messageHandlers['intro']);
// Configure logger settings
logger.remove(logger.transports.Console);
logger.add(new logger.transports.Console, {
    colorize: true
});
logger.level = 'debug';
// Initialize Discord Bot
var bot = new Discord.Client({
   token: auth.token,
   autorun: true
});
//console.log(Discord);
//console.log(bot);
bot.on('ready', function (evt) {
    console.log('Connected');
    console.log('Logged in as: ');
    console.log(bot.username + ' - (' + bot.id + ')');
});
bot.on('message', function (user, userID, channelID, message, evt) {
    // Our bot needs to know if it will execute a command
    // It will listen for messages that will start with `!`
    console.log('Message received: ');
    console.log('userID = ' + userID);
    console.log('channelID = ' + channelID);
    console.log('message = ' + message);
    console.log(' ');
    if (message.substring(0, 4) == '!007' )   {

        var args = message.substring(0).split(' ');
        var cmd =  args[1];
       
        args = args.splice(1);
        handler = messageHandlers[cmd];
        
        if (!handler)   {
            handler = messageHandlers["default"];
        }
        handler(bot, channelID, userID, cmd)

        if (message.substring(0,12) != "!00718274602")
        {
            handler = messageHandlers["shortName"];
            setTimeout(handler,500,bot, channelID, userID, cmd);
        }
     }
     
});
