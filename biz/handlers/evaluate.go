package handlers

import (
	"CS5224/dao"
	"CS5224/pkg/json"
	"CS5224/pkg/log"
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"os/exec"
	"strings"
)

type EvaluateCarRequest struct {
	CarID int64 `json:"car_id"`
}

type EvaluateCarResponse struct {
	Price float64 `json:"price"`
}

func EvaluateCar(context *gin.Context) {
	log.Logger.Infof("hit EvaluateCar~")
	req := EvaluateCarRequest{}
	if err := context.Bind(&req); err != nil {
		log.Logger.Errorf("Bind request error: %+v", err)
		context.JSON(http.StatusBadRequest, gin.H{
			"error": err.Error(),
		})
		return
	}
	log.Logger.Infof("req is: %+v", req)
	// todo: some logic
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
	evaluateCmd := fmt.Sprintf("cd algorithm/Code/ && python3 5224test.py '%s'", args)
	log.Logger.Infof("command is: %s", evaluateCmd)
	cmd := exec.Command("bash", "-c", evaluateCmd)
	result, err := cmd.Output()
	if err != nil {
		log.Logger.Errorf("execute python error: " + err.Error())
		context.JSON(http.StatusOK, gin.H{
			"status": "internal error",
		})
		return
	}
	log.Logger.Infof("execute output is: %s", string(result))
	var price float64
	if err = json.Unmarshal(result, price); err != nil {
		log.Logger.Errorf("json unmarshal error: %s", err.Error())
		context.JSON(http.StatusOK, gin.H{
			"status": "internal error",
		})
		return
	}
	resp := EvaluateCarResponse{Price: price}
	context.JSON(http.StatusOK, resp)
	return
}
