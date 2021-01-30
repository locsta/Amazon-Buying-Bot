# Amazon-Buying-Bot
This bot aims to help the user buy a product with low availability and high demand (eg PS5)  

## Mandatory
In order to run the bot you will need to download my [Scraper module](https://github.com/locsta/Scraper)  
The other librairies are all available for installation using pip  

## What the bot does
* The bot opens one or more Firefox browser  
* Login on amazon using the email and password your entered through the CLI  
* Refreshes amazon page(s) every fews seconds until the item appears available  
* When the item is avaible clicks on "buy-now" button (fast check-out) (Need to set the manually the location of the confirmation button)  

### Work in progress
This project is a work in progress  
Further improvements will be done later, such as:  
* better CLI  
* [integrated captcha solver](https://github.com/locsta/Amazon-Captcha-Solver) (if that's doable)  
* remove autogui library completely (and the problems that comes with it)  
* possibility of saving your email/password locally and safely  
* ini file to save sets of parameters  