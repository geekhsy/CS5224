# CS5224: Cloud Computing Project (CarGuru)

## Introduction
> This repo is the back-end part for our `CarGuru` project. `CarGuru` is a second-hand car trading platform based on AWS. Currently, it provides the features including uploading cars, searching cars, the evaluation of second-hand cars, and the recommendation for second-hand cars. 
>
> This file describing how to configure, setup and run the project based on AWS using the codes in this repository. The project is implemented by Go 1.17 and relies on multiple AWS services(e.g. AWS RDS, AWS ElasticCache)

## Project Structure
```shell
├── algorithm                   # the machine model based on Bert to do the evaluation & recommendation                   
├── biz                         # the business logic 
│   ├── handlers                # the handlers for HTTP requests
│       ├── add.go              # the HTTP handler for uploading car requests
│       ├── evaluate.go         # the HTTP handler for evaluating car requests
│       ├── query.go            # the HTTP handler for searching car requests
│       ├── recommand.go        # the HTTP handler for recommanding car requests
│── dao                         # data access object level: responsible for the database operation
│   ├── redis                 
│       ├── redis.go            # the operation relevant to AWS ElasticCache
│   ├── db.go                   # the operation relevant to AWS RDS
│   ├── model.go                # the tables' definiation
├── external                 
│       ├── preprocess 
│           ├── db.sql                   # the sql to create table 
│           ├── preprocess.ipynb         # the python script to extract cars' records from raw CSV 
│   ├── transaction.go          # executed the transactions required 
├── pkg                         # common tools to replace the ones in standard library
│   ├── json
│       │── json.go             # more efficient json tool
│   ├── log
│       │── log.go              # more efficient log printer            
└── application.go              # the entrance to the program
```



## Configuration
### Init Redis
Set up AWS ElasticCache in AWS console and replace the following information in `InitRedisClient()` function from dao/redis/redis.go:
```go
func InitRedisClient() {
    Client = redis.NewClient(&redis.Options{
        Addr:     "carguru.ow3jum.0001.use1.cache.amazonaws.com:6379",
        Password: "", // no password set
        DB:       0,  // use default DB
    })
}
```

### Init MySQL
Set up AWS RDS in AWS console and replace the following information in dao/db.go:
```go
const (
	username = "admin"
	password = "admin666"
	dbHost   = "database-2.ckzihnf4uip0.us-east-1.rds.amazonaws.com"
	dbPort   = 3306
	dbName   = "carguru"
)
```

## Running
Run the following command
```shell
go run application.go
```
Then the server will run and listening to the port 5000, the normal output should be:
```shell
2022-04-09T21:43:53.792+0800    info    /Users/wangxin/GolandProjects/CS5224/application.go:13  Hello World     {"serviceName": "CS5224"}
2022-04-09T21:43:53.792+0800    info    /Users/wangxin/GolandProjects/CS5224/dao/db.go:29       admin:admin666@tcp(database-2.ckzihnf4uip0.us-east-1.rds.amazonaws.com:3306)/carguru    {"serviceName": "CS5224"}
[GIN-debug] [WARNING] Creating an Engine instance with the Logger and Recovery middleware already attached.

[GIN-debug] [WARNING] Running in "debug" mode. Switch to "release" mode in production.
 - using env:   export GIN_MODE=release
 - using code:  gin.SetMode(gin.ReleaseMode)

[GIN-debug] GET    /welcome                  --> CS5224/biz.Welcome (3 handlers)
[GIN-debug] POST   /get_cars                 --> CS5224/biz/handlers.GetCars (3 handlers)
[GIN-debug] POST   /add_cars                 --> CS5224/biz/handlers.AddCars (3 handlers)
[GIN-debug] POST   /recommend_cars           --> CS5224/biz/handlers.RecommendCars (3 handlers)
[GIN-debug] POST   /evaluate_car             --> CS5224/biz/handlers.EvaluateCar (3 handlers)
[GIN-debug] [WARNING] You trusted all proxies, this is NOT safe. We recommend you to set a value.
Please check https://pkg.go.dev/github.com/gin-gonic/gin#readme-don-t-trust-all-proxies for details.
[GIN-debug] Listening and serving HTTP on :5000
```

## Reference
* https://aws.amazon.com/rds/
* https://aws.amazon.com/redis/
* https://aws.amazon.com/lambda/
* https://aws.amazon.com/s3/
* https://pkg.go.dev/github.com/gin-gonic/gin
