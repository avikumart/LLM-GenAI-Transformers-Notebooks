Deploy on AWS:
1. Login to AWS account (add card/free tier credits for one year on account setup)
2. Search for AWS EC2
3. Click "Launch Instances"
4. Add a name and select necessary details like OS, disk size etc..
5. Create a .ppk key and save it
6. Once instance is created, connect to it via the connect button after clicking the instance id
7. Update commands to run to ensure everything is up to date
    a. `sudo apt-get update`
    b. `sudo apt-get upgrade`
8. Use WinScp to connect to EC2 and add files there
9. Check for python and install pip and venv
    a. `sudo apt-get install python3-pip`
    b. `sudo apt-get install python3-venv`
10. Create a new environment `python3 -m venv env`
11. To activate the environment `source env/bin/activate`
12. Install all the requirements `pip3 install -r requirements.txt`
13. Run the app `uvicorn <file_name>:app --host 0.0.0.0`
14. Make sure to add the port number to the security inbound rules
15. Use `nohup` to keep the app running even after closing the terminal `nohup uvicorn <file_name>:app --host 0.0.0.0`
16. To stop nohup process `ps -ef|grep uvicorn` and `kill -9 <PID>`
17. To run multiple apps together use `tmux`
18. Tmux commands:
    a. `tmux` -> to launch a tmux terminal
    b. `tmux new -s <session_name>` -> to launch a tmux terminal with name
    c. `ctrl b + d` -> back to main terminal
    d. `tmux list-session` -> to get a list of tmux sessions
    e. `tmux attach -t <session_name>` -> attach back to the tmux terminal
    f. `tmux kill-session -t <session_name>` -> kill a running session
19. Terminate the EC2 instance