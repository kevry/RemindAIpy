# RemindAIpy (python) -- version 0.1
Python alternative to the Remind A.I. project

#### Written by Kevin M. Delgado

## Objective (updated)
Since COVID-19 many institutions and businesses have transitied their staff to a remote setting. However, as a result of this, students and workers are now required to be in front of a computer almost all the time. Unfortunately, having to sit for so long can lead to many physical health issues. Sources such as the National Health Service of UK, and PainScience, have recommended a maximum of 30 minutes of sitting at one go. However, this number is always exceeded. To solve this issue, I decided to develop a web gui that utilizes deep learning to track if users are sitting or standing. If the application detects that the user has been sitting for more than the recommended time, an alarm or notification will be activated to notify the user to stand. For reinforcement, this alert will continually be activated until the app detects the user has stood up. The overall goal of this is to prevent users from sitting for prolonged periods of time.

## Awards:
Remind A.I. is the winner of two categories at BostonHacks 2020 🎉🎊
1. BostonHacks Best FitTech 💪🏽 
2. Best Use of Google Cloud - COVID-19 Hackathon Fund 🏋️‍♂️🏃‍♀️

Devpost Link - https://devpost.com/software/remind-a-i

Google Cloud Demo Week Link - https://events.withgoogle.com/demo-week-hackathon-fund/remind-ai/#

Demo Link - https://drive.google.com/file/d/1pKkIDtWujqohYbHvuVvlgWnHKYRE7IbM/view?usp=sharing

## Instructions to use (for now ...)

1.  Clone the repository ``git clone https://github.com/kevry/RemindAIpy.git``

2.  Create a Python environment using either ``requirements.txt`` or ``requirements_win.txt`` if you are on a Windows OS

3.  Start script ``python main.py``

## Use
At the start,  you can set the limit of how long you want to be sitting for (in minutes), and how you want to be alerted if you exceed the limit (only notification available at the moment). Once a session has started, Remind A.I. will track when you are sitting and standing and the overall frequency of how ofter you are sitting and standing.

<img width="320" alt="remind_ai_intro_screen" src="https://github.com/kevry/RemindAIpy/assets/45439265/31303b94-441b-4816-950b-60f3cba6ccaa">


<img width="460" alt="remind_ai_tracking_screen" src="https://github.com/kevry/RemindAIpy/assets/45439265/86f063e1-d9a2-47ba-bf95-e8bb89911456">
