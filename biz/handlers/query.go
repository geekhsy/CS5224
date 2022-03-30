package handlers

import (
	"CS5224/biz/model"
	"CS5224/pkg/log"
	"github.com/gin-gonic/gin"
	"net/http"
)

type GetCarRequest struct {
	Model              string `form:"model" json:"model"`
	LowPrice           int64  `form:"low_price" json:"low_price"`
	HighPrice          int64  `form:"high_price" json:"high_price"`
	Brand              string `form:"brand" json:"brand"`
	LowProductionYear  int64  `form:"low_production_year" json:"low_production_year"`
	HighProductionYear int64  `form:"high_production_year" json:"high_production_year"`
}

type GetCarResponse struct {
	Cars []model.Car `form:"cars" json:"cars"`
}

/*
Sample:
curl --location --request POST 'http://44.202.253.122:5000/get_cars' \
--form 'model="wangxin"' \
--form 'low_price="30"'
*/

func GetCars(context *gin.Context) {
	log.Logger.Infof("hit GetCars~")
	req := GetCarRequest{}
	if err := context.Bind(&req); err != nil {
		log.Logger.Errorf("Bind request error: %+v", err)
		context.JSON(http.StatusBadRequest, gin.H{
			"error": err.Error(),
		})
		return
	}
	log.Logger.Infof("req is: %+v", req)
	// todo: some logic
	resp := GetCarResponse{Cars: []model.Car{{
		Model:          "testAddModel",
		Price:          666,
		Brand:          "testAddBrand",
		ProductionYear: 2020,
		URL:            "www.google.com",
	}}}
	context.JSON(http.StatusOK, resp)
	return
}
