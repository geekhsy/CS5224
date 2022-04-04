package handlers

import (
	"CS5224/biz/model"
	"CS5224/dao"
	"CS5224/dao/redis"
	"CS5224/pkg/log"
	"github.com/gin-gonic/gin"
	"net/http"
	"time"
)

type AddCarsRequest struct {
	Cars []model.Car `form:"cars" json:"cars"`
}

type AddCarResponse struct {
}

/*
Sample:
curl --location --request POST 'http://44.202.253.122:5000/add_cars' \
--header 'Content-Type: application/json' \
--data-raw '{
    "cars": [
        {
            "model": "test",
            "price": 1000,
            "brand": "NUS",
            "production_year": 2048,
            "URL": "www.baidu.com"
        }
    ]
}'
*/

func AddCars(context *gin.Context) {
	log.Logger.Infof("hit AddCars~")
	req := AddCarsRequest{}
	if err := context.Bind(&req); err != nil {
		log.Logger.Errorf("Bind request error: %+v", err)
		context.JSON(http.StatusBadRequest, gin.H{
			"error": err.Error(),
		})
		return
	}
	log.Logger.Infof("req is: %+v", req)
	key := redis.GenCarKey("123")
	// prevent concurrent insert
	if success, err := redis.Client.SetNX(key, 1, time.Minute*1).Result(); err != nil || !success {
		context.JSON(http.StatusOK, gin.H{
			"status": "service busy",
		})
		return
	}
	car := dao.Car{
		Title:        req.Cars[0].Title,
		Model:        req.Cars[0].Model,
		Manufactured: req.Cars[0].ProductionYear,
		Mileage:      req.Cars[0].Mileage,
		Price:        req.Cars[0].Price,
	}
	if err := dao.InsertCar(&car); err != nil {
		context.JSON(http.StatusOK, gin.H{
			"error": err.Error(),
		})
		return
	}
	resp := AddCarResponse{}
	context.JSON(http.StatusOK, resp)
	return
}
