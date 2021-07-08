# Obtaining refresh token

## Prerequisites
BeProduct implements OAuth2 [Authorization Code](https://datatracker.ietf.org/doc/html/rfc6749#section-1.3.1) authentication flow. That means you can use any library of your choice for getting [**access**](https://datatracker.ietf.org/doc/html/rfc6749#section-1.4) or [**refresh**](https://datatracker.ietf.org/doc/html/rfc6749#section-1.3.1) tokens. 

Below we will generate a refresh token manually. Once you have a refresh token you will use it with this library to call BeProduct Public API. You wont need to worry about refreshing your access token manually. This library will do it for you.

## Client Credentials 
Before accessing BeProduct you should request [BeProduct Support](mailto:support@beproduct.com) to generate **client credentials** for your application. After your request has been granted your receive:

* Client ID (Identifies your application)
* Client Secret
* Callback URL (Used to redirect a user to this URL after successful authentication. You can always ask support to add more whitelisted url's to your client id)
* Scopes (Identifies recources your app can access. It is the predefined value for every app: `openid profile email roles offline_access BeProductPublicApi`)
## Authorization flow
Authorization flow consists of 4 simple steps

1. Your application redirects a user to BeProduct authentication server providing your *client id* and *callback url* 
2. User authenticates using his/her login/password and is redirected back to your application callback URL with **authorization code** being a GET parameter
3. Your application makes a call to BeProduct authentication server providing **authorization code** from step 2, *client id* and *client secret*.
4. BeProduct authentication server responds with **refresh and access** tokens.

NOTE: While Client ID uniquely identifies your application the *refresh* and *access* token identify both your app and a signed user. All subsequent calls to the BeProduct Public API will be impersonated as a user from step 2. All permission checks will be executed against that user identity.

## Obtaining Refresh And Access tokens
In this section we will get tokens using [curl] which is present on any Unix type OS and can be easily installed on Windows. Alternatively one simple way of getting access and refresh token is [postman](https://www.postman.com/).
You may use [this](https://beproduct.atlassian.net/l/c/TAXJ87AP) tutorial for that.

We will follow 4 steps from above to get the tokens.

We will need two authentication server endpoints:

* Authorization endpoint - `https://id.winks.io/ids/token/authorize`
* Token endpoint - `https://id.winks.io/ids/connect/token`

### 1. Redirecting to authentication server
We can craft the necessary url by using next template:
`https://id.winks.io/ids/connect/authorize?client_id=<CLIENTID>&response_type=code&scope=openid+profile+email+roles+offline_access+BeProductPublicApi&redirect_uri=<CALLBACK_URL>`

Place your client id and callback url and open URL in a webbrowser.

### 2. Authentication 
Identity server asks for login and password. After that it redirects you to your callback url (which in our case is not a valid listening endpoint). You should see in your browser that you was redirected to a url which looks like this:

`<CALLBACK_URL>?code=6850c396e36e42ddcbc5af2844bd18ef&session_state=...nonimportant`

**code** GET parameter is our **authorization code**.

### 3. Exchanging authorization code for a refresh token

Put your **client id**, **client secret**, **callback url** and **authorization code** into command below

```
curl --request POST \
  --url 'https://id.winks.io/ids/connect/token' \
  --header 'content-type: application/x-www-form-urlencoded' \
  --data grant_type=authorization_code \
  --data client_id=YOUR_CLIENT_ID \
  --data client_secret=YOUR_CLIENT_SECRET \
  --data code=YOUR_AUTHORIZATION_CODE \
  --data 'redirect_uri=YOUR_CALLBACK_URL'
```

After you execute this command in the  terminal you should get a response like this:
```
{
"id_token":"....",
"access_token":"eyJ0eXAiO......your access token here...",
"expires_in":28800,
"token_type":"Bearer",
"refresh_token":"0f7c7235cc3448a000000000001"
}
```
Congratulations! You've got your refresh token.

NOTE: Access token lifetime is specified in *expires_in* value. Refresh token only expires when it's revoked and can be stored and reused.
### 4. OPTIONAL. Refreshing tokens 
You can use refresh token from the previous step to obtain as many access_token as required without user interaction to access BeProduct Public API using other means than this library (For example you can use Access Token to call API directly from [BeProduct Public API Website](https://developers.beproduct.com/documentation/)

To get new access token just do:

```
curl --request POST \
  --url 'https://id.winks.io/ids/connect/token' \
  --header 'content-type: application/x-www-form-urlencoded' \
  --data grant_type=refresh_token \
  --data client_id=YOUR_CLIENT_ID \
  --data client_secret=YOUR_CLIENT_SECRET \
  --data refresh_token=YOUR_REFRESH_TOKEN 
```

That's it. You have your access token to access BeProduct Public API.
  


