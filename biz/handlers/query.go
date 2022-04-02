package handlers

import (
	"CS5224/biz/model"
	"CS5224/dao"
	"CS5224/pkg/log"
	"github.com/gin-gonic/gin"
	"net/http"
)

type GetCarRequest struct {
	Title           string `json:"title,omitempty" form:"title"`
	ManufacturedMax int    `json:"manufactured_max,omitempty" form:"manufactured_max"`
	ManufacturedMin int    `json:"manufactured_min,omitempty" form:"manufactured_min"`
	TypeOfVehicle   string `json:"type_of_vehicle,omitempty" form:"type_of_vehicle"`
	Transmission    string `json:"transmission,omitempty" form:"transmission"`
	PriceMax        int    `json:"price_max,omitempty" form:"price_max"`
	PriceMin        int    `json:"price_min,omitempty" form:"price_min"`
}

type GetCarResponse struct {
	Cars []model.Car `form:"cars" json:"cars"`
}

/*
Sample:
curl --location --request POST 'http://localhost:5000/get_cars' \
--form 'title="volvo"' \
--form 'price_min="30"'
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
	carParams := dao.CarParams{
		Title:           req.Title,
		ManufacturedMax: req.ManufacturedMax,
		ManufacturedMin: req.ManufacturedMin,
		TypeOfVehicle:   req.TypeOfVehicle,
		Transmission:    dao.TransmissionTypeEnum(req.Transmission),
		PriceMax:        req.PriceMax,
		PriceMin:        req.PriceMin,
		OrderBy:         "price",
	}
	cars := make([]model.Car, 0)
	if results, err := dao.SearchCar(&carParams); err != nil {
		cars = append(cars, model.Car{
			Title:          "dks",
			Model:          "dks",
			Price:          66666,
			Mileage:        100,
			ProductionYear: "2022",
			URL:            "https://elasticbeanstalk-us-east-1-530992748314.s3.amazonaws.com/demo1.jpeg",
		})
	} else {
		for _, result := range results {
			cars = append(cars, model.Car{
				Title:          result.Title,
				Model:          result.Model,
				Price:          result.Price,
				Mileage:        result.Mileage,
				ProductionYear: result.Manufactured,
				URL:            "https://elasticbeanstalk-us-east-1-530992748314.s3.amazonaws.com/demo1.jpeg",
			})
		}
	}
	resp := GetCarResponse{Cars: cars}
	context.JSON(http.StatusOK, resp)
	return
}
