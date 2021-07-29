# UFV exam schedule watcher
Don't ever want to miss an exam? This tool notifies your phone when one of your exam times was updated, added, or created.

## Setup
### IFTTT (part 1)
1. Setup [IFTT by creating an account (or using a google account)](https://ifttt.com/login)
2. [Create your applet](https://ifttt.com/create).
3. Click on **Add**, type **webhooks** and click **recieve a web request**. Enter **ufv_exam_change** as the event name and **create trigger**
4. Click **Add** and type **Notifications**, click **Send a notification from the IFTTT app**.
5. Enter `[{{EventName}}]: {{Value1}}` as the message and **create action**, continue and finish!
### Python (part 2)
1. Open the project and in the terminal run `python setup.py install`
2. Follow the instructions in the terminal, enter in your CRN (course) numbers. Enter **done** when done.
3. For the IFTTT event name put `ufv_exam_change`
4. Enter your secret key which is the text after **https://maker.ifttt.com/use/** on the page.

Finally run it `python runner.py`
This will auto check every hour and notify you accordingly!