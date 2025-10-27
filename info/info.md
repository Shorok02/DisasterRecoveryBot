# Disaster Recovery bot stuff

fallback plan so during critical downtime you ensure service continuity and transparency

> what is the disaster we are recovering from? attacks, server downtime, network this is so important I need more **context** look it up and ask

## 0. What disaster ?

### 1. App Downtime / Outage

- Backend servers for the app are down

- Mobile or web app crashes

- Deployment error or system upgrade

### 2. Partial API Failure

Main trading APIs are down, but portfolio data is still retrievable from caches or backups ---> Users can’t trade, but they should view holdings I think users can see their stuff still from the app Idk if the bot might be used here but yeah.
**TODO: CHECK Different database options replicas, snapshots, different provider**

## 1. Examples of such bots - real ones:

some bots are read only bots --> ensure availability of info BUT no actions (e.g. you can not close a position)

Other bots actions are available --> This should be controlled in a sense maybe rate limited, logged (if the server is down I am not sure how actions proceed I was thinking the whole bot works with a lightweight replica or smth **needs further research I do not know**)

> might need a layer of authentication / verification (OTP maybe like kite backup)

- Zerodha “Kite Backup: WhatsApp-based emergency mode” you can have transactions here AND verification https://zerodha.com/z-connect/kite/introducing-kite-backup-a-whatsapp-based-emergency-mode?utm_source=chatgpt.com

- Based bot
  https://t.me/based_one_bot
  **you can link the wallet** I think this is what hana was talking about but not sure. If they have their own wallets in the backend I think we can not integrate this wallet we will need APIs (?) to integrate with our own backend wallets if the based bot is using telegram TON wallet thing in the first place **check the whole thing**

![alt text](image.avif)

> there are different UI/UX options: commands or menus or buttons Zerodha is so so similar so far

## 2. What I actually used

- @BotFather in telegram to create the token of the bot
- simple python script with _python-telegram-bot library_



## 3. linking the phone number to the database :
 - first commit was all dummy data, we want when the user opens the bot, it fetches his details from the database based on his phone number or username (if we have usernames in our db)

 - telegram does not directly catch phonenumber, you need to prompt the user to share contact and then check if this phone number is a verified user in our db 

 - also usually they do **not** do that, instead you can : 
    - ask the user to enter his username and verify it with an otp (if we do otp stuff) 
    **very general you can literally use the bot from any device as long as you can verify with the otp.**

    - or from the main app itself, users link their telegram account with their profile and then you can work with telegram ids instead of phone numbers (e.g. binance)
    **if a user did not link his telegram account with his profile, he will not be able to use the bot**
    

## 4. Database: 
- first version dummy data inside the script itself
- now try to connect to a database (I chose sqlite for simplicity) and fetch user details based on phone number 
 - check how you can design it for such usecase initially one table with user info and another table for transactions (since we are doing actions)
 - later might be a replica or smth since disaster recovery or on the cloud.

## TODOs

- instead of dummy data fetch details based on username or phone number (after authentication if we do it --> recommended --> akedly otps should be easy)

- check the whole mirror data / replica if we are not gonna deal with the server itself

- is it read only or we can close positions

> depends on the **the type of disaster we will recover from** hahahahahah be more open ya shrouq not just db or backend server maybe network maybe the trading stuff itself aaaaaa**check this out go to point 0**
