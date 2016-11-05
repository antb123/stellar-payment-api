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

### Step 3

All transactions need to submit the sender information, recipeint info and some meta data regarding the actual transaction.

Users are in the code member_id*tempo.eu.com

The system needs to generate a post command with the following JSON


{
    "firstname": "Rizwan",
    "lastname": "Azwan",
    "nationality": "RU",
    "address1": "123 St",
    "address2": "",
    "city": "Paris",
    "postcode": "75306",
    "country": "FR",
    "email":"abcd@gmail.com",
    "gender": "Male",
    "dob": "1973-09-09",
	"mobile": "+339696968699",
	"callback":"http://www.test.com",
    "occupation": "worker",
    "annual_income": "10000", 
	"id_details":"BAD876G567",
	"id_type":"Passport",
	"id_expiry":"2017-09-05",
	"id1_scan":"image(base64_encoded)",
	"id2_details":"BAD876G567",
	"id2_type":"Residence permit",
	"id2_expiry":"2017-09-05",
	"id2_scan":"image(base64_encoded)",
}

# format notes
nationality/country iso alpha2:
https://en.wikipedia.org/wiki/ISO_3166-1_alpha
gender: Male/Female
mobile in E.164 fomat:
https://en.wikipedia.org/wiki/E.164
dob: iso 8601
https://en.wikipedia.org/wiki/ISO_8601


Option fields: address2, id2 is not required if id1 is a passport.




### Step 4 Routing Call


Generate KYC call

Assuming the sender and receiver are not registered on the TEMPO network you need to submit the appropriate paperwork.

As TEMPO is a registered PSD licensed with the Bank of France this is required by our regulator for all transactions.

If you have already submitted the kyc information you can just submit the memberid if you have it.







