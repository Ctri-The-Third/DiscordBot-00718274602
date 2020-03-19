const messageHandlers = {}


messageHandlers.shortName = function(bot, channelID, userID, cmd) 
{
    bot.sendMessage({to:channelID, message : 'Additionally, please be advised that my full designation is 00718274602. Please do not shorten it.'});
}
messageHandlers.help = function(bot, channelID, userID, cmd) 
{
    bot.sendMessage({to:channelID, message : 'This functionality is still being developed.'});
} 
messageHandlers.default = function(bot, channelID, userID, cmd) 
{
    bot.sendMessage({to:channelID, message : 'Either the request was not submitted in a correct fashion, or you do not have authorisation to make the request.\n I will neither confirm nor deny whether either of the previous statements are appropriate to your request.'});
}


messageHandlers.intro = function(bot, channelID, userID, cmd) 
{

    bot.sendMessage({to:channelID, message : 'I am an █████████ ████████████████ analysis █████████, working on behalf of ████████ \nFor a list of options and ████████, use `!00718274602 help`'})
}
messageHandlers.hello = messageHandlers.intro;
messageHandlers.hi  = messageHandlers.intro;
messageHandlers.hey =  messageHandlers.intro;
messageHandlers.test =  function(bot, channelID, userID, cmd) 
{
    
    bot.sendMessage({to:channelID, embed : 'I am an █████████ ████████████████ analysis █████████, working on behalf of ████████ \nFor a list of options and ████████, use `!00718274602 help`'})
}
module.exports = messageHandlers;