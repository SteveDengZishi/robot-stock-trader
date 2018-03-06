# Robot Stock Trader
* Smart investing for everyone.
* Created by Robot Stock Trading Group LLC.
* Steve, Rohan, Anmol

## Holding your money gets you nowhere but inflation

#### How do individuals make smarter investment decisions by avoiding the volatility in the market and compete with institutional investors

It is difficult for ordinary users to make money off of the stock market because it is hard to commit enough time to constantly watch it and analyze trends. In addition, it is typically not worth creating a real high-frequency trading robot because HFT firms have vastly better hardware and systems design to capitalize on miniscule intervals of time. A trading robot that holds positions for seconds or minutes is therefore a much better idea.

## Who

Students, citizens, or anyone else interested in making higher returns off of their investments without needing to constantly monitor and trade on the stock market. Those with a higher risk profile than what is offered by index funds, but do not want to pay fees associated with mutual or other funds.

## How

* The user creates an account on the web client and links it to their investment account (containing capital).
* The user inputs factors such as risk profile, initial capital investment, and others (to be decided) that will affect how the robot behaves.
* At the start of a trading day, the robot pulls this information from the database and starts trading using the money in the account.
* At the end of a trading day, the robot loads its performance metrics to the database so they can be viewed in the web client.


## Scope

There are a few major components I anticipate needing to be completed for this project:
* Machine Learning: pre-train a neural net based on available historical stock values and trading data that will define the main behavior of the robot. Optional: use some algorithm to also optimize which stocks are selected based on the user's risk profile. This will likely need to be done with some cloud computing service like AWS.
* Web Application: Interface in which users can create accounts, login, view performance statistics, and modify their preferences and settings/
*  API: Handles communication between the robot, database, and web application.
* Database: Stores user data, the robot's data (once training is complete), etc.

I anticipate that the machine learning task will definitely be the hardest part, since this is what is at the core of the trading robot. This task will likely need input from multiple people, or 1 - 2 fully dedicated group members. The web application, API, and database will probably be of similar difficulty to each other to set up, and could be handled by 2 - 3 group members. With good planning, I definitely think this project is achievable within the semester. Here is a link to a blog by an experienced software engineer describing his experience of setting up a trading bot in a couple of months


## Links
* https://www.indiehackers.com/businesses/stock-trading-bot
* http://cs229.stanford.edu/proj2014/David%20Montague,%20Algorithmic%20Trading%20of%20Futures%20via%20Machine%20Learning.pdf

