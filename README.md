# RecipeBox

a blog for posting online recipes with Django 4.2 and redis / postgres

## authentication 🔐
a custom user model has been used 

users can login with google or github

when a new user signup a wellcome email is sent using signals

user email verifucation is optional

users can reset-password, change email and etc.

2 step verification is optional

## how does it work 🤔

Users can post recipes and do **CRUD** on them

users can follow and unfollow each other 

User can see rcipes from your followning accuonts

Home feed will show recipes posted from your following accounts 

recipe list will show newest recipes

users can **Like and Comment** on a recipe

Users can **Bookmark** recipe for later 

bookmarked recipes are avalible in profile

some pages are cached with **Redis**



### user Profile
user can see the contact info in profile

 Bookmarked recipes are visible in profile

 all the posted recipes are showen in profile 

users can follow or un follow each other in profile page

if a user is owner of a profile extra info will be showen like bookarked / liked recipes

 ### Recipes

 filter and search for recipes are available

 recipe have images

 in recipe list you can see title and image then you have to click on it to see details

 in recipe detail you see instructions and other informaitions

 you can bookmark recipe in the detail view
 

## How to use
1) create a psql DB and a local_cnf.py file
2) add your data base info to local_cnf.py
3) then run migrations

        python manage.py migrate

4) create a super user and login 





 
