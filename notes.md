### Convention: 
As a rule of thumb, values are stored as strings and converted just at the moment when they are needed to be else 


### Method of propagation 
- each server send to all his neighbors if it is not a member of `sent_ls`
- what can go wrong? 
    - there can be multiple versions of sent_ls propagated around 
        - sol: eventually, they will all fill up
- each request contains a sent_ls, with names, seperated with commas.
    - to send a request, each server take sthe prior sent_ls and append `,{server_name}`

### Logging convention 
- log where, and only where, writer.write is used
- always log after writing, in case we can catch a failure to write that way
- timestamp when logging, there will be a bit of a discrepency for network writes, but that's ok

### Before submitting
- what other test cases can I run? talk to people
