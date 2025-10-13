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

## 3. todos

- instead of dummy data fetch details based on username or phone number (after authentication if we do it --> recommended --> akedly otps should be easy)

- check the whole mirror data / replica if we are not gonna deal with the server itself

- is it read only or we can close positions

> depends on the **the type of disaster we will recover from** hahahahahah be more open ya shrouq not just db or backend server maybe network maybe the trading stuff itself aaaaaa**check this out go to point 0**
