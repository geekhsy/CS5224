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
	originalCar := dao.Car{
		ListingID:       123456,
		Title:           "test",
		Make:            "",
		Model:           "",
		Description:     "ownerconsignmentunit, viewingstrictlybyappostringmentonly. pristineconditionwithlotsof upgradesdone. viewtobelieve!optiontopurchasewithout coe. flexible loan solutions! call/whatsapp our sales consultant now to arrange for a viewing before it's gone!",
		Manufactured:    "2012",
		OriginalRegDate: "",
		RegDate:         "2012-6-27",
		TypeOfVehicle:   "suv",
		Category:        "",
		Transmission:    "",
		CurbWeight:      0,
		Power:           0,
		FuelType:        "",
		EngineCap:       0,
		NoOfOwners:      1,
		Depreciation:    0,
		Coe:             0,
		RoadTax:         0,
		DeregValue:      0,
		Mileage:         0,
		Omv:             0,
		Arf:             0,
		OpcScheme:       "",
		Lifespan:        "",
		EcoCategory:     "",
		Features:        "smooth inline 6 3.0l turbo n55 engine, high specification unit. view specs of the bmw x6",
		Accessories:     "20'' staggered m rims, carbon steering wheel, 10'' andriod headunit, hamann wide bodykit, kw coilover, bms tuned.",
		IndicativePrice: 0,
	}
	args := json.ToString(originalCar)
	args = strings.Replace(args, "'", "", -1)
	recommendCmd := fmt.Sprintf("python3 algorithm/Code/5224rectest.py '%s' 5", args)
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
