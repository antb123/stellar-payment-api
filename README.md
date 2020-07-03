# TEMPO's Stellar API documentation

# Summary
* [1. Domains](#1-domains)  
    - [1.1. Public Network](#11-public-network)  
    - [1.2. Test Network](#12-test-network)  
* [2. SEPs](#2-seps)  
* [3. Guides](#3-guides)  

## 1. Domains

### 1.1. Public Network

Domain:  
`https://k.tempocrypto.com`

Assets:
* EURT (fiat)

*fiat* assets represent currencies in the real world (EUR, USD) and can be
 deposited/withdrawn directly to bank accounts.

### 1.2. Test Network

Domain:  
`https://ktest.tempocrypto.com`

Assets:
* PURPLE

## 2. SEPs

* [SEP-1](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0001.md): fully compliant
* [SEP-2](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0002.md): not supported
* [SEP-6](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0006.md): fully compliant, requires account to be already verified, see notes below
* [SEP-10](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0010.md): fully compliant
* [SEP-24](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0024.md): fully compliant

Notes:
* SEP-6 can only be used after user document verification (KYC), either through SEP-24 or manual approval

## 3. Guides

* [SEP-10: Obtain token](./guides/sep10.md)
* [SEP-24: Basic Wallet Implementation](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0024.md#basic-wallet-implementation)
* [SEP-6: Basic Wallet Implementation](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0006.md#basic-wallet-implementation)

