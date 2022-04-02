package main

import (
	"CS5224/biz"
	"CS5224/dto"
	"CS5224/pkg/log"

	"github.com/gin-gonic/gin"
)

func main() {

	log.Logger.Info("Hello World")

	dto.ConnectDB()

	router := gin.Default()
	biz.RegisterRouters(router)
	router.Run(":5000")
}
