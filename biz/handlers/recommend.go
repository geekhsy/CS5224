package handlers

import (
	"CS5224/biz/model"
	"CS5224/pkg/log"
	"github.com/gin-gonic/gin"
	"net/http"
)

type RecommendCarsRequest struct {
	CarID int64 `json:"car_id"`
}

type RecommendCarsResponse struct {
	Cars []model.Car `form:"cars" json:"cars"`
}

/*
Sample:
curl --location --request POST 'http://44.202.253.122:5000/recommend_cars' \
--form 'id="1024"'
*/

func RecommendCars(context *gin.Context) {
	log.Logger.Infof("hit RecommendCars~")
	req := RecommendCarsRequest{}
	if err := context.Bind(&req); err != nil {
		log.Logger.Errorf("Bind request error: %+v", err)
		context.JSON(http.StatusBadRequest, gin.H{
			"error": err.Error(),
		})
		return
	}
	log.Logger.Infof("req is: %+v", req)
	// todo: some logic
	resp := RecommendCarsResponse{Cars: []model.Car{{
		Model:          "testRecommendModel",
		Price:          666,
		Brand:          "testRecommendBrand",
		ProductionYear: 2020,
		URL:            "www.google.com",
	}}}
	context.JSON(http.StatusOK, resp)
	return
}
