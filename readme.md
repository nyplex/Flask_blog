
<h1 align="center">Flask Blog</h1>

*This is the README file for FLASK BLOG web application. You will find here a bunch of information regarding the Design, the technologies used and some information regarding the code.*

FlaskBlog is a web application that allow user to create, edit & upate posts. They have the possibility to add an image on their post, add a category and add up to 5 tags. Users can also like, dislike and love any posts (included their own). Finally, users can comment any posts and they can edit or delete their comment. As a post's owner you can delete any comments on your post. User must create an account and be logged in to use the application. 
Last be not least, the user has the possiblity to reset their password, update their profile account, and finally the user can choose between light & dark mode.
 
 
The main goal of this application is to share posts, communicate with the community. 
 
There is an Admin account on the app. As an admin you can delete any posts, delete any comment and finally add, update or remove any category. To log in as Admin use the following credentials:

email: admin@admin.com
password: Password1234@
 
[Check out the website here.](https://nyplex-flask-blog.herokuapp.com/)

![alt text](responsiveSimon.png)



<h1 align="center">UX</h1>
 
## User's needs

My main focus regarding the user's needs was the application layout design and responsivity. My second focus was to add some friendly and usefull feature (comments images, tags etc.)
 
Finally I wanted to make sure the application was easy to use and for that I've decided to use a minimalistic design with short and direct text.
 

## Website requirements
       
- Signin/Signup page
- Home page with all the post
- Single post page
- Create new post page
- Edit post
- category page
- Profile page
- Account setting feature
- Dark & light mode
- comments, tags, category and like buttons



## Usage Scenario
       
- First-time Users
 
    When the user lands on the website for the first time, they will arrive the login page where they can create an account. Once the user have created an account, he will be redirected to the home page. As a new user, the application will generate a default profile picture and default username (first name + last name). User is able to update his personal information and change the default profile pciture and username. The user can also change his password but can NOT change his email address.
 
- Returning Users
 
    When the user return to the website they will either arrive directly on the home page ( if they are still logged in) or they will have to login (if they use a different device for exemple). The goal for the returning uses is to have more interction within the application (like & comment posts). They will also have the possibility to edit their posts, search for specific post on the application.
 
- User's Journey


    If the user is not logged in, he will be welcomed by the loggin page where he can either log in or create an account. Once they have logged in or created an account, the user will be redirected to the home page. On the home page, the user can see a list with all the posts. From there, he can open a single post, create a post, search for a post, go to his profile and configure his settings. 

    To open a single post, the user will click on the title of the post from the home page. He will then be redirected to the signle post page where he will find the post's title, post's body, post's image if any. From the single post page, the user can like, dislike or love the post and he can also comment the post. If the user open one of his own post, he will have the possibility to edit or delete his post. 

    To create a new post, the user will click on 'Add New Topic' button, he will be redirected to the new post page. From there the user will have to fill up a form in order to  create a new post. He will have to enter a title for his post, a text body , an optional image, a category and some optionals tags. Once the new post is created, he will be redirected to the single post page to see his new post. 

    When editing a post, the same page of create a new post will open, but the form will be pre-populated and the user will be able to change anything and repost the topic. 

    At any time and anywhere on the app, the user can open his profile settings to update his personnal information and profile picture. 
 


<h1 align="center">Design</h1>
 
## Wireframes
 
I used Figma to make the wireframe.
  - Color palette
  - Setup page
  - Main page

You can find the figma in the root project. The file's name is 'Material Design.fig'
 
## Colors
 
The main colours used on the website are dark blue, light blue and gray. The text is dark gray.
These are the main colours used on the website:
 
  - light: "#F1FAEE",
  - secondary: "#A8DADC",
  - primary: "#1D3557",
  - text: "#323232",
  - Second variant: "#457B9D",
 
## Typography
 
I have used 1 font on this application, the main one is "IBM Plex Sans".


<h1 align="center">Technologies</h1>

- HTML5
- CSS3
- TailwindCSS
- JavaScript ES6
- jQeury
- PostCSS
- Webpack
- GIT
- Flask
- MongoDB
- Heroku
- AWS


<h1 align="center">Features</h1>

- FRONT-END
    
    On the front-end I have used javascript ES6 & jQuery combined with webpack. Webpack give me the possibility to split my JS code into multiples files and bundle them into 1 main JS file. Webpack will also get rid of unused code, minify my main file and remove any comment which will improve efficieny. 

    On the top of jQuery, I have used 2 others librairies. The first one is ckEditor.js , whick allows me very easily to insert into my project a text editor. I implatement this feature for the user to create a new a post and have much more freedom on the post's design. 

    The second library is validator.js which give the user real time feedback when he fillup a form. If the user make a mistake in a form, he will receive a form error immediatly without the need to submit the form. 

    Finally, I have used mulitlple Ajax trhough the application (posts live search, like and dislike button, comments section).

    Regarding CSS, I have used TailwindCSS combine with Webpack and PostCSS. TailwindCSS is a great css framework which really helped me to code less espiclly to implement thr dark/light mode. Webpack allows the bundle all my CSS files into 1 and minify it. PostCSS allows to automatically add the prefixer. 


- BACK-END & DATABASE

  On the back-end I have used the python micro framework Flask. I splited my code into 3 mains apps. The first one is MAIN, which is responsible for the home page, category page atc. The second one is Posts, which take care of all the logic for the posts like creating new posts, editing posts, deleting posts, seeing a single posts etc. Finallt the third app is User which take care of the user's logic like login and logout, editing profile account etc. 

  Regarding the database, I have used MongoDB. Finally I have deployed my project on heroku and AWS. I only deploy static files on AWS and link my app to AWS. When you visit the website, heroku will call AWS and load all the static files(CSS, JS and all the images).


<h1 align="center">Testing</h1>

Testing has been a very important part of this project. I was constantly testing all the new features I was adding to the application. As a result, since I have deployed this project, I haven't found any bugs or issues.

My testing method was very simple but very efficient. Every new function or feature implemented in the app was tested. 

I also used Lighthouse from the google chrome dev. tool. 
 

<h1 align="center">Deployment</h1>

Flask BLog has been deployed on Heroku and AWS, click [here.](http://nyplex-flask-blog.herokuapp.com/) to check the live application.

This project use different technologies (webpack, tailwindCSS, jQuery etc..), in order to have a working version of the project on your local machine, please follow these steps using your terminal:

- Install python in your machine and node.js
- clone the git repo on your local machine (git clone https://github.com/nyplex/Flask_blog.git)
- cd into the project folder
- run "npm intall" , in order to install all the dependencies. 
- run "npm run build" in order to bundle all the files.
- run "pip3 install -r requirements.txt"
- run "python run.py"

You must have node.js & git install on your machine.
    
