# cetac-apis

This repository contains the APIs that work along with the CETAC 
[iOS App (checkout the repo)](https://github.com/CETAC-NetworkDefenders/cetac-nd-app). The backend is built with AWS 
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

![image](https://drive.google.com/uc?export=view&id=1EKWjHDulDn1Yv5j1lzqcyBS3wDuq6OVL)

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

**Note:** Due to time limitations, it was not possible to use AWS Cognito to authenticate the API calls
nor for the user login. However, the *AuthLambda* allows to securely login an identify the access level 
for a user. First, given an email (username), the corresponsing SALT is looked up in the DB and it is
returned to the app, along with the user id that has that specific SALT. Then the App appends the received
value to the password, computes the hash using SHA256, and sends that value over another HTTP request to the
API. If the password for that user is correct, her access level is returned, otherwise an error message is
generated and the login fails. 

## DB Reference

The DB is SQL and normalized for faster operations and reduced storage space. The following 
diagram can be used as a reference: 

![image](https://drive.google.com/uc?export=view&id=1VFndloMM5CZigqAHsiWsIse9BP_dfr2O)






