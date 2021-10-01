# cetac-apis

This repository contains the APIs that work along with the CETAC 
[iOS App](https://github.com/CETAC-NetworkDefenders/cetac-nd-app). The backend is built with AWS 
using serverless technologies to ensure effectiveness and scalability. The main purpose is to 
perform CRUD operations over the organization's data. 

[CETAC](https://www.cetac.mx) is a thanatologic clinic that provides free therapy and holistic 
treatment spanning a variety of services to people who have faced a recent loss. The mobile app 
is designed for internal usage. Thanatologists can add users (patients) and sessions, in order 
to keep track of the treatment for each of them. Administrators can add thanatologists and 
visualize reports of the KPIs such as the number of patients, the month income (via recovery 
fees), and the performance of the thanatologists. 


## AWS Architecture

A few AWS services were used to provide functionality and security to the application. AWS 
Cognito was used for the user authentication. This is combined with API Gateway, which expects a 
valid token in order to authorize the HTTP request. After this, depending on the endpoint of the 
request, one of five different Lambdas is invoked. 

Each of them performs CRUD operations that 
allow the management of the organization's data. In order to access the data, they retrieve 
a secret from AWS Secrets Manager, and they use the received credentials to login to an Aurora 
Serverless DB that runs with Postgres. 

The following diagram summarizes the interaction between the different services: 

![image](https://drive.google.com/uc?export=view&id=1LH7GPSSkQe7Rxc1NiKI2udxlLSBuYWud)

The Serverless Application Model (SAM) was used for the definition of the AWS resources. All the 
Lambdas and the API Gateway is defined in the `template.yaml` file. However, there are three 
resources that should be created directly from the management console: 

- The IAM role that will be assumed by the Lambdas when they are invoked. It must include 
  sufficient policies for VPCAccess and SecretsManagerAccess, as well as the regular LambdaExecute.
    
- The DB should also be created separately. It must use Postgres in the backend. Aurora 
  Serverless is the recommended service. 
  
- The secret with the DB access credentials. A private VPC endpoint must be created for Secrets 
  Manager, and it should be added to the same Security Group and Subnets that the Lambda has 
  access permissions. 
  
The template parameters must be updated when any of these resources is replaced. 

## DB Reference

The DB is SQL and normalized for faster operations and reduced storage space. The following 
diagram can be used as a reference: 

![image](https://drive.google.com/uc?export=view&id=1VFndloMM5CZigqAHsiWsIse9BP_dfr2O)

## API Reference

This is the reference of the API. It describes the endpoints, their functionality, and the 
expected request and response structure (WIP). This is to conform to the set values and keys 
when calling the API from XCode. 


### `/thanatologist`

CRUD functionalities for the management of CETAC thanatologists. 

| Method   | Description                                    | Input Format | Output Format |
| -------- | ---------------------------------------------- | ------------ | ------------- |
| `GET`    | Obtain the information of a thanatologist.     |              |               |
| `POST`   | Create a new thanatologist.                    |              |               |
| `PATCH`  | Update the information of a new thanatologist. |              |               |
| `DELETE` | Remove a thanatologist from the system.        |              |               |

### `/user`

CRUD functionalities for the management of CETAC users. 

| Method   | Description                       | Input Format | Output Format |
| -------- | --------------------------------- | ------------ | ------------- |
| `GET`    | Obtain the information of a user. |              |               |
| `POST`   | Create a new user.                |              |               |
| `PATCH`  | Update the information of a user. |              |               |
| `DELETE` | Remove a user from the system.    |              |               |

### `/session`

Management of the users' sessions with thanatologists. A session cannot be corrected nor deleted once it is registered, so that it cannot be tampered later on. Not even an admin can perform this task.

| Method | Description                                 | Input Format | Output Format |
| :----- | ------------------------------------------- | ------------ | ------------- |
| `GET`  | Retrieve the information of a past session. |              |               |
| `POST` | Register a new session.                     |              |               |

### `/admin`

| Method   | Description                               | Input Format | Output Format |
| :------- | ----------------------------------------- | ------------ | ------------- |
| `GET`    | Get the information of an admin user.     |              |               |
| `POST`   | Create a new admin user (not for support) |              |               |
| `DELETE` | Delete an admin (not for support)         |              |               |

### `/reports`

These do not manage any CRUD functionality, but they are used to obtain reporting information. 

#### `/reports/listing/...`

Return a list of summaries instead of the complete information of the administrators. This will be used to create the table views. Instead of sending all the information related to every thanatologist or user, only the 

| Endpoint          | Method | Description                                            | Input Format | Output Format |
| :---------------- | ------ | ------------------------------------------------------ | ------------ | ------------- |
| `/thanatologists` | `GET`  | Get a list of all the thanatologists                   |              |               |
| `/admins`         | `GET`  | Get a list of all the administrators                   |              |               |
| `/sessions`       | `GET`  | Get a list of all the sessions associated with a user. |              |               |

#### `reports/dashboard/...`

| Endpoint         | Method | Description                                    | Input Format | Output Format |
| :--------------- | ------ | ---------------------------------------------- | ------------ | ------------- |
| `/thanatologist` | `GET`  | Get the information of a single thanatologist. |              |               |
| `/motives`       | `GET`  | Get a report of the attendance motives.        |              |               |
| `/users`         | `GET`  | Get a report of the number of attended users.  |              |               |
| `/income`        | `GET`  | Get a report of the income.                    |              |               |

### `/auth/...`

(**Temporary endpoint until Cognito is added**)

Authentification for a thanatologist or admin with her credentials. The request is `POST` rather than `GET` because it is safer to send the information in the body rather than in the request query. 

| Endpoint         | Method | Description | Input Format | Output Format |
| :--------------- | ------ | ----------- | ------------ | ------------- |
| `/thanatologist` | `POST` |             |              |               |
| `/admin`         | `POST` |             |              |               |






