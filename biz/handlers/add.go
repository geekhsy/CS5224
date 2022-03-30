package handlers

import (
	"CS5224/biz/model"
	"CS5224/pkg/log"
	"github.com/gin-gonic/gin"
	"net/http"
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
	// todo: some logic
	resp := AddCarResponse{}
	context.JSON(http.StatusOK, resp)
	return
}
