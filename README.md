# Video Storing App (Backend)


Built with FastAPI
Runs on sqllite database 


installing the requirements and 
running: uvicorn main:app from the project root terminal should run the app.


a fake database module runs to fill the data as the app loads. The fake data lacks video type validation. However, the validation on video type is assured on the real runs. The fake script was written for testing out joins and queries on pgadmin workbench before opting to use sqlalchemy orm.


several requests on endpoint requires authentication. This was done imagning a real world scenario. A superuser is left to be made to access all endpoints with ease.









