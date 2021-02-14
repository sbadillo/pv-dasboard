# Data Dashboard - Seasonal Solar Production

## Motivation

The PV observer webapp plots estimated solar production for a Photovolotaic (PV) System.

The application relies on the user input of location. The backend makes use of the PVGIS webservice to obtain Solar PV estimated yield.
Finally, the plotly.js library is used to display results to the user.

other tools used in this project:

- heroku
- plotly.js
- flask
- bootstrap.js

# To-do list

- [x] set basic project structure
- [x] build simple user input form,
- [x] get form data, see : https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask
- [x] write an API call function that pulls data fromt the PVGIS service
- [ ] clean and prepare the data set
- [ ] put the data into a csv file or json
- [ ] write a Python script to read in the data set and set up the Plotly visualizations
- [ ] set up a virtual environment and install the necessary libraries to run your app
- [ ] run web app locally to make sure that everything works
- [ ] deploy the app to Heroku or some other back-end service
