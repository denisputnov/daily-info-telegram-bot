# Daily info Telegram bot

> Telegram interface for cheching dollar and euro course to ruble and check COVID-19 situation in Russia and all over the world.</br>

### Installation
``` cmd
git clone https://github.com/grnbows/daily-info-telegram-bot.git
```

### Usage 
In `config.py`:
```
TOKEN = '1234567890:abcdefghijklmnopqrstuwxyzABCdefghijK # bot token from @BotFather
ADMIN_ID = '123456789' # admin id to stop the bot
```

The `TOKEN` variable is responsible for connecting your program with the bot. You can get your own token from `@BotFather` in Telegram.
`ADMIN` variable allows you to select a user and give him the largest bot management rights. The value of this variable is the id of your telegram account.

Also in `config.py` you can change `PARSE_DELAY`. This variable show how often parser will update local data. 
```
PARSE_DELAY = 300 
```
A value of `300` seconds is the most optimal in my opinion.
### Code info
In `bot.py` you can see a threading module include. I use this library for `reloadData` function, that parse new info for bot from the Internet every `config.PARSE_DELAY` seconds.</br>
I started this function in own thread. It's necessary that the database update process doesn't disturb the main bot code.</br></br>In `config.py`:
```
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
```
It's the user agent, that needed for correct parser work. </br>
You can find your own user agent [HERE](https://www.google.com/search?sxsrf=ALeKk01kqrdxJf949NumVHacA5etbmoVKA%3A1585737968455&source=hp&ei=8HCEXsOgGdPlmwWm57oo&q=my+user+agent&oq=my&gs_lcp=CgZwc3ktYWIQARgAMgQIIxAnMgIIADICCAAyBQgAEIMBMgUIABCDATICCAAyAggAMgIIADICCAAyAggAOgcIIxDqAhAnUIQHWNQIYL4daAJwAHgAgAFciAG0AZIBATKYAQCgAQGqAQdnd3Mtd2l6sAEK&sclient=psy-ab).</br>
 #### Logging settings:
 You can chang basic logging config in `bot.py` at the top of file:
 ```
 logging.basicConfig(filename='botbody.log',
					level=logging.INFO,
					format='%(asctime)s///%(levelname)s///%(funcName)s/// - %(message)s')

 ``` 

---
### Find me here:
* [Вконтакте](https://vk.com/grnbows) </br>
* [Instagram](https://www.instagram.com/grnbows) </br>
* [Twitter](https://twitter.com/grnbows) </br>

### License

I want to use this code only by myself. Please, take this code for free, but only for education. 

<i>With respect and love,</i></br> by grnbows