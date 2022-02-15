# Comics publisher

Posts a random [xkcd](https://xkcd.com) comic to a [VK](https://vk.com) group.

### How to install

#### VK

1. Create a `.env` file to store all sensitive data, needed to launch the program.
2. You need an account on [VK.com](https://vk.com). Save your account ID to the `.env`:
```commandline
VK_USER_ID=<paste account id here>
```
The account ID may be retrieved on [regvk](https://regvk.com/id/) (NB the site is russian language only).
3. Also you need a group where you want to post your comics (you must have admin rights to this group). You can see available groups on the dedicated page: [vk.com/groups?tab=admin](https://vk.com/groups?tab=admin)
Save your group ID in the `.env`:
```commandline
VK_GROUP_ID=<paste group id here>
```
The group ID may be retrieved on [regvk](https://regvk.com/id/) (NB the site is russian language only).
4. You'll need to have an app through which you'll post the comics. You can create it here: [vk.com/apps?act=manage](https://vk.com/apps?act=manage). Choose `Standalone app` platform. In the app `Settings` tab see the `App ID`. It'll be needed in the next step
5. Get an access token via the [VK implicit flow](https://vk.com/dev/implicit_flow_user)
Paste you `App ID` retrieved on the previous step as `client_id`:
```commandline
https://oauth.vk.com/oauth/authorize?client_id=<your APP ID here>&scope=photos,groups,wall,offline&response_type=token
```
Paste the link above to your browser and allow the requested access.
After the redirect, you'll see the `access_token` in you browser's address line:
```commandline
https://oauth.vk.com/blank.html#access_token=blatestdd369edblablabla2f63c2testb33d7ea7d80d97ed2d287d30bla943c09b2e9409fd18a20a1e[...]
```
Copy and paste it to the `.env` file:
```commandline
VK_API_ACCESS_TOKEN=<paste access_token here>
```
Great, all's done! Now we are ready for the project installation and run.


#### Poetry

1. Python3 should already be installed. For more detailed instruction please visit the [Python official site](https://www.python.org/downloads/)
2. You need Poetry to be installed.  Use pip (or pip3, if there is a conflict with Python2) to install it:
```commandline
pip install poetry
```
2. To install Poetry dependencies, execute:
```commandline
poetry install
```
3. To run the project, execute:
```commandline
poetry run python main.py 
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).