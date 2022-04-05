package main

import (
	"CS5224/biz"
	"CS5224/dao"
	"CS5224/dao/redis"
	"CS5224/pkg/log"
	"github.com/gin-gonic/gin"
)

func main() {

	log.Logger.Info("Hello World")
	dao.InitDB()
	redis.InitRedisClient()

	router := gin.Default()
	biz.RegisterRouters(router)
	router.Run(":5000")
}
