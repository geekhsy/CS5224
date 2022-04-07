package handlers

import (
	"CS5224/biz/model"
	"CS5224/dao"
	"CS5224/pkg/json"
	"CS5224/pkg/log"
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"os/exec"
	"strings"
)

type RecommendCarsRequest struct {
	Title           string `json:"title"`
	Make            string `json:"make"`
	Model           string `json:"model"`
	Description     string `json:"description"`
	Manufactured    string `json:"manufactured"`
	OriginalRegDate string `json:"original_reg_date"`
	RegDate         string `json:"reg_date"`
	TypeOfVehicle   string `json:"type_of_vehicle"`
	Category        string `json:"category"`
	Transmission    string `json:"transmission"`
	CurbWeight      int    `json:"curb_weight"`
	Power           int    `json:"power"`
	FuelType        string `json:"fuel_type"`
	EngineCap       int    `json:"engine_cap"`
	NoOfOwners      int    `json:"no_of_owners"`
	Depreciation    int    `json:"depreciation"`
	Coe             int    `json:"coe"`
	RoadTax         int    `json:"road_tax"`
	DeregValue      int    `json:"dereg_value"`
	Mileage         int64  `json:"mileage"`
	Omv             int    `json:"omv"`
	Arf             int    `json:"arf"`
	OpcScheme       string `json:"opc_scheme"`
	Lifespan        string `json:"lifespan"`
	EcoCategory     string `json:"eco_category"`
	Features        string `json:"features"`
	Accessories     string `json:"accessories"`
	IndicativePrice int    `json:"indicative_price"`
	Price           int64  `json:"price"`
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
	args := json.ToString(req)
	args = strings.Replace(args, "'", "", -1)
	recommendCmd := fmt.Sprintf("cd algorithm/ && python3 5224rectest.py '%s' 5", args)
	log.Logger.Infof("command is: %s", recommendCmd)
	cmd := exec.Command("bash", "-c", recommendCmd)
	var (
		result []byte
		err    error
	)
	if result, err = cmd.Output(); err != nil {
		log.Logger.Errorf("execute python error: " + err.Error())
		resp := RecommendCarsResponse{Cars: []model.Car{{
			Model:          "testRecommendModel",
			Price:          666,
			ProductionYear: "2020",
			URL:            "https://elasticbeanstalk-us-east-1-530992748314.s3.amazonaws.com/demo1.jpeg",
		}}}
		context.JSON(http.StatusOK, resp)
		return
	}
	log.Logger.Infof("execute output is: %s", string(result))
	recommendCars := make([]dao.Car, 0)
	if err = json.Unmarshal(result, recommendCars); err != nil {
		log.Logger.Errorf("json unmarshal error: %s", err.Error())
		resp := RecommendCarsResponse{Cars: []model.Car{{
			Model:          "testRecommendModel",
			Price:          666,
			ProductionYear: "2020",
			URL:            "https://elasticbeanstalk-us-east-1-530992748314.s3.amazonaws.com/demo1.jpeg",
		}}}
		context.JSON(http.StatusOK, resp)
		return
	}
	cars := make([]model.Car, 0)
	for _, car := range recommendCars {
		cars = append(cars, model.Car{
			Model:          car.Model,
			Price:          car.Price,
			ProductionYear: "2020",
			URL:            "https://elasticbeanstalk-us-east-1-530992748314.s3.amazonaws.com/demo1.jpeg",
		})
	}
	resp := RecommendCarsResponse{Cars: cars}
	context.JSON(http.StatusOK, resp)
}
