![home](./readme/home.png)

![logo](./readme/logo.png)

Kograph is an intelligent file gallery that harnesses AI tools to enhance user experience. This application is crafted to simplify file management and viewing, offering a wide array of intuitive AI-Powered features.
<br/>
<br/>
## Features

**⚡️AI Tools**
- Image Analysis
- Advanced Search
- Advanced User Activity
- Intelligent Organization
- Map with Image's location

**👩‍💻 Normal Tools**
- User Control
- Voice Control
  
*More features coming soon...*
<br/>
<br/>
## Deployment

**Client side run**

```bash
cd frontend
npm run serve
```

**Server side run**

```bash
cd backend
.\venv\Scripts\activate
python manage.py runserver 0.0.0.0:8000
```
<br/>

## Usage

You'll need to configure the environment variables for the application to work correctly. If you don't have access to AWS, don't worry, you just won't have access to the features that use artificial intelligence.

**/frontend/.env**

```bash
# SERVER URL
VUE_APP_SERVER_URL=

# FRONTEND URL
VUE_APP_BASE_URL=
```

**/backend/.env**

```bash
# YOUR APP NAME
APP_NAME=

# FRONTEND URL
FRONTEND_BASE_URL=

# EMAIL
EMAIL_APP_KEY='xxxx xxxx xxxx xxxx'

# AWS CREDENTIALS
aws_access_key_id=
aws_secret_access_key=
aws_session_token=
aws_region=
bucket=
```
<br/>

## Color Palette

| Color             | Hex                                                                |
| ----------------- | ------------------------------------------------------------------ |
| Primary Color | ![#00d1a0](https://via.placeholder.com/10/318ba7?text=+) #318ba7 |
| Primary Dark Mode | ![#0a192f](https://via.placeholder.com/10/242424?text=+) #242424 |
| Primary Light Mode | ![#00b48a](https://via.placeholder.com/10/ececec?text=+) #ececec |
| Secondary Dark Mode | ![#f8f8f8](https://via.placeholder.com/10/373737?text=+) #373737 |
| Secondary Light Mode | ![#00d1a0](https://via.placeholder.com/10/e2e2e2?text=+) #e2e2e2 |
<br/>

## Used libraries

[<img src="https://seeklogo.com/images/V/vuejs-logo-17D586B587-seeklogo.com.png" width="50" alt="vuejs" title="VueJS">](https://vuejs.org/)&nbsp;&nbsp;
[<img src="https://static-00.iconduck.com/assets.00/django-icon-1606x2048-lwmw1z73.png" width="40" alt="django" title="Django">](https://www.djangoproject.com/)&nbsp;&nbsp;
[<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Font_Awesome_logomark_blue.svg/1200px-Font_Awesome_logomark_blue.svg.png" width="50" alt="fontawesome" title="Fontawesome">](https://fontawesome.com/)&nbsp;&nbsp;
[<img src="https://companieslogo.com/img/orig/axios-51d6caae.png?t=1701353255" width="50" alt="axios" title="Axios">](https://axios-http.com/)&nbsp;&nbsp;
[<img src="https://banner2.cleanpng.com/20180328/ige/kisspng-leaflet-javascript-library-web-browser-plug-in-sof-leaflet-5abbab56a7bfc0.9378939815222485346871.jpg" width="50" alt="" title="">]()&nbsp;&nbsp;
[<img src="" width="50" alt="" title="">]()&nbsp;&nbsp;
[<img src="" width="50" alt="" title="">]()&nbsp;&nbsp;
[<img src="" width="50" alt="" title="">]()&nbsp;&nbsp;
[<img src="" width="50" alt="" title="">]()&nbsp;&nbsp;
[<img src="" width="50" alt="" title="">]()&nbsp;&nbsp;
[<img src="" width="50" alt="" title="">]()
<br/>

## 3rd Party Help

[<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/1024px-ChatGPT_logo.svg.png" width="50" alt="chatgpt" title="ChatGPT">](https://chat.openai.com/)&nbsp;&nbsp;
[<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Microsoft_365_Copilot_Icon.svg/2048px-Microsoft_365_Copilot_Icon.svg.png" width="50" alt="copilot" title="Microsoft Copilot">](https://copilot.microsoft.com/)
