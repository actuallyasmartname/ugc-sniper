# ugc-sniper

the best one out there (yet again)

credits to xolo he's like cool i guess for making this? idk

### tutorial
since the og server for this is down you have to enjoy the beauty of having a multitude of extra steps
1. find a suitable place to host a webserver. either host it yourself or with a platform like replit or heroku. this tutorial will focus on using replit, but if you're gonna host it yourself you should know better by now
2. download this repo
3. create a new repl and add the file `webserver.py` from this repo and rename it to `main.py` then create a new file called `items.json`
4. in the shell run `pip install eventlet`
5. create two secrets, call em whatever you want but i would name them `cookie` and `webhook`
6. in the `webhook` secret add the URL for a discord webhook
7. in the `cookie` secret add a .ROBLOSECURITY cookie; i would suggest making a new roblox account from <a href="https://replit.com/@cooleddie001/Firefox-Legacy">here</a>, transfer the cookie via <a href="https://snippet.host">snippet.host</a> (make sure it is set to delete after read), and setting your cookie
8. on line 8, change "WEBHOOKHERE" to `os.environ['webhook']` or whatever your webhook secret is called (remove the quote marks!). if you are hosting by yourself obviously set it to your webhook url
9. on line 9, change "COOKIEHERE" to `os.environ['cookie']` or whatever your cookie secret is called (remove the quote marks!). if you are hosting by yourself obviously set it to your .ROBLOSECURITY cookie
10. optionally you can set line 112's number to something higher if the webhook's going too fast
11. click 'Run' and it should install all required modules. if it doesn't work make sure you followed the instructions carefully
12. now for the sniper. open `main.py` and it should install all required modules then crash.
13. open `config.json`, in line 4 where it says "https://eee" replace it with your webhook url
14. in line 18 where it says the .ROBLOSECURITY warning put in your .ROBLOSECURITY for the account you wanna snipe for
15. open `main.py`, go to line 731 and replace the url with your url with `:8080` at the end
16. go to line 736 and replace the url with your url with `/items` at the end (do not put :8080)
17. save it and run and it should work. congrats ur done
### important
- fastes ugc sniper 
- has autosearcher

<a rel="license" href="http://creativecommons.org/licenses/by-nd/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nd/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nd/4.0/">Creative Commons Attribution-NoDerivatives 4.0 International License</a>.
