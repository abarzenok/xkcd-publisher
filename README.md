# Comics publisher

Posts a random [xkcd](https://xkcd.com) comic to the [VK](https://vk.com) group.

### How to install

#### VK

1. Create a `.env` file to store all the sensitive data needed to run the program.
2. You need an account on [VK.com](https://vk.com). Save your account ID in `.env`:
```commandline
VK_USER_ID=<paste account id here>
```
Account ID can be obtained at [regvk](https://regvk.com/id/) (note: the site is in Russian only).

3. You will also need a group in which you want to post your comics (you must have admin rights to this group). You can see the available groups on a dedicated page: [vk.com/groups?tab=admin](https://vk.com/groups?tab=admin).
Save your group ID in the `.env`:
```commandline
VK_GROUP_ID=<paste group id here>
```
Group ID can be obtained at [regvk](https://regvk.com/id/) (note: the site is in Russian only).

4. You will need an application through which you will publish comics. You can create it here: [vk.com/apps?act=manage](https://vk.com/apps?act=manage). Select the `Standalone app` platform. In the `Settings` tab of the application, see `App ID`. You will need it in the next step.
5. Get access token via [VK implicit flow](https://vk.com/dev/implicit_flow_user).
Paste the `App ID` obtained in the previous step as `client_id`:
```commandline
https://oauth.vk.com/oauth/authorize?client_id=<your APP ID here>&scope=photos,groups,wall,offline&response_type=token
```
Paste the link above into your browser and allow the requested access.
After the redirect, you will see `access_token` in your browser's address bar:
```commandline
https://oauth.vk.com/blank.html#access_token=blatestdd369edblablabla2f63c2testb33d7ea7d80d97ed2d287d30bla943c09b2e9409fd18a20a1e[...]
```
Copy and paste it into the `.env` file:
```commandline
VK_API_ACCESS_TOKEN=<paste access_token here>
```
Great, it's done! We are now ready to install and run the project.


#### Poetry

1. Python3 should already be installed. For more detailed instructions visit [Python official site](https://www.python.org/downloads/)
2. You need Poetry to be installed.  Use pip (or pip3, if there is a conflict with Python2) to install it:
```commandline
pip install poetry
```
2. To install Poetry dependencies, run:
```commandline
poetry install
```
3. To run the project, execute:
```commandline
poetry run python main.py 
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
