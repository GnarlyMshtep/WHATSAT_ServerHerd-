### Convention: 
As a rule of thumb, values are stored as strings and converted just at the moment when they are needed to be else 


### Method of propagation 
- each server send to all his neighbors if it is not a member of `sent_ls`
- what can go wrong? 
    - there can be multiple versions of sent_ls propagated around 
        - sol: eventually, they will all fill up


### Before submitting
- add another test case and run
- all test cases are passing
- read through specs, make sure you answer EVERY question on report 
- test cases with floating point numbers (expect all the chease for WHATSAT)
- check that if right length, we need not worry about wrong arguments
- does the difference have to say "+" if it is positive?
- *still checking about assuming all input on one line*
- check if logger loads correctly when we are not in the same repo as logs