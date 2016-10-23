# TEMPO Stellar Connectivity


## Background

All incoming transactions that occur on the TEMPO stellar network require KYC information that is similar to that required by ISO 20022.

Senders will have two options. The first one is to submit transactions using the Stellar Compliance Protocol which is described on the [stellar.org website](https://www.stellar.org/developers/guides/compliance-protocol.html)





### STEP 1 Read the STELLAR TOML FILE

You will need to read the file from our server

[https://tempo.eu.com/.well-known/stellar.toml](https://tempo.eu.com/.well-known/stellar.toml)

```
curl https://tempo.eu.com/.well-known/stellar.toml
```


### STEP 2 Read the Stellar AUTH_SERVER parameter

Read the AUTH_SERVER parameter

AUTH_SERVER="https://api.tempo.eu.com/auth"

```
curl https://tempo.eu.com/.well-known/stellar.toml | grep AUTH_SERVER
```

### Step 3 Routing Call

This step is optional if the 



### Step 4 Routing Call


Generate KYC call

Assuming the sender and receiver are not registered on the TEMPO network you need to submit the appropriate paperwork.

As TEMPO is a registered PSD licensed with the Bank of France this is required by our regulator for all transactions.

If you have already submitted the kyc information you can just submit the memberid if you have it.







