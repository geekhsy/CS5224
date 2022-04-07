package handlers

import (
	"CS5224/pkg/json"
	"CS5224/pkg/log"
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"os/exec"
	"strings"
)

type EvaluateCarRequest struct {
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
	args := json.ToString(req)
	args = strings.Replace(args, "'", "", -1)
	evaluateCmd := fmt.Sprintf("cd algorithm/ && python3 5224test.py '%s'", args)
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
