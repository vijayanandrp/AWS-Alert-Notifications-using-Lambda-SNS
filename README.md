# PROBLEM 
Being in data engineering role, 
many times we need to monitor the daily load jobs and lambda, data flows. 
It's always challenging to monitor the status and capture the errors. 
Most of the time ended up creating more SNS and alert & error lambdas to handle it.

# DESIGN
create a single Lambda that handles all the email and notifications to the various channels
`HAVING EASY MODULAR DESIGN HELPS US TO PUT ALL IN ONE PLACE`
### design light weight
### one point configuration
### template based
### easy to manage, scale, maintain


# SOLUTION
1. Email templates can be maintained using AWS SES
2. AWS Lambda reads the app config based on uniq app_name given and send the email using configuration.

NOTE: All email address and group email address should be verified manually.





