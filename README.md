open-platform
=============

software allowing member to quickly host and publish their website with help from different organizations


[know more] (http://hackfoldr.org/code4hk/1HBq3TDTE4B_nxtRQGhiZrfawLYxjh6AEBcIvFqdxvE0)


###You have an app to host
1. Fill in the form in 1min, give us project name, e.g. demo
http://bit.ly/open-platform-add
2. we will follow up
3. work on your app & ssh git clone etc
4. share the app url demo.dev.code4.hk to your friends
5. there is no step 5
behind the hood:

###Behind the hood
1. we the dev ops will use a quick python script that will spawn a docker container (~VM) in ubuntu
`./bootstrap.sh <<project_code>>`
2. nginx config is generated with virtual host
3. a simple python HTTP server is there listening to 80
4. so <<project_code>>.dev.code4.hk will point here & up and running
5. give the dev generated key & port to ssh it
