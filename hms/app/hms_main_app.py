import crud_operations
import client_cli
import db_services


# uncomment the below to run the api server
crud_operations.crud_operations()

# uncomment the below to run the CLI client 
# client_cli.menus()



# Api links to run and test the api's
# GET - http://localhost:5000/patients             // to get all the patients
# GET - http://localhost:5000/patients/<id>        // to get a particular account based on id
# POST - http://localhost:5000/patients            // to add a new account (name, )
# PUT - http://localhost:5000/patients/<id>        // to update the existed book
# DELETE - http://localhost:5000/patients/<id>     // to delete the book by using its id
# GET - http://localhost:5000/patients/average-age // to get the average age
# GET - http://localhost:5000/patients/scraped     // scrape the books how many pages need to 