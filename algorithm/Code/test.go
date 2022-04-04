package main

import (
	"encoding/json"
	"fmt"
	"os/exec"
	"strings"
)

type xtest struct {
	Listing_id        int64   `json:"listing_id"`
	Title             string  `json:"title"`
	Make              string  `json:"make"`
	Model             string  `json:"model"`
	Description       string  `json:"description"`
	Manufactured      float64 `json:"manufactured"`
	Original_reg_date string  `json:"original_reg_date"`
	Reg_date          float64 `json:"reg_date"`
	Type_of_vehicle   string  `json:"type_of_vehicle"`
	Category          string  `json:"category"`
	Transmission      string  `json:"transmission"`
	Curb_weight       float64 `json:"curb_weight"`
	Power             float64 `json:"power"`
	Fuel_type         string  `json:"fuel_type"`
	Engine_cap        float64 `json:"engine_cap"`
	No_of_owners      float64 `json:"no_of_owners"`
	Depreciation      float64 `json:"depreciation"`
	Coe               float64 `json:"coe"`
	Road_tax          float64 `json:"road_tax"`
	Dereg_value       float64 `json:"dereg_value"`
	Mileage           float64 `json:"mileage"`
	Omv               float64 `json:"omv"`
	Arf               float64 `json:"arf"`
	Opc_scheme        string  `json:"opc_scheme"`
	Lifespan          string  `json:"lifespan"`
	Eco_category      string  `json:"eco_category"`
	Features          string  `json:"features"`
	Accessories       string  `json:"accessories"`
	Indicative_price  float32 `json:"indicative_price"`
}

func StructToJson(data xtest) string {
	jsons, errs := json.Marshal(data)
	if errs != nil {
		fmt.Println(errs.Error())
	}
	sdata := string(jsons)
	// fmt.Prstringln(string(jsons))
	return sdata
}

func main() {
	x := xtest{
		Listing_id:        123456,
		Title:             "test",
		Make:              "",
		Model:             "",
		Description:       "ownerconsignmentunit, viewingstrictlybyappostringmentonly. pristineconditionwithlotsof upgradesdone. viewtobelieve!optiontopurchasewithout coe. flexible loan solutions! call/whatsapp our sales consultant now to arrange for a viewing before it's gone!",
		Manufactured:      2012,
		Original_reg_date: "",
		Reg_date:          2012 / 6 / 27,
		Type_of_vehicle:   "suv",
		Category:          "",
		Transmission:      "",
		Curb_weight:       0,
		Power:             0,
		Fuel_type:         "",
		Engine_cap:        0,
		No_of_owners:      1,
		Depreciation:      0,
		Coe:               0,
		Road_tax:          0,
		Dereg_value:       0,
		Mileage:           0,
		Omv:               0,
		Arf:               0,
		Opc_scheme:        "",
		Lifespan:          "",
		Eco_category:      "",
		Features:          "smooth inline 6 3.0l turbo n55 engine, high specification unit. view specs of the bmw x6",
		Accessories:       "20'' staggered m rims, carbon steering wheel, 10'' andriod headunit, hamann wide bodykit, kw coilover, bms tuned.",
		Indicative_price:  0,
	}
	xdata := StructToJson(x)
	// xdata := json.ToString(x)
	// fmt.Printf("TYPE: %T VALUE: %v\n", xdata, xdata)
	xdata = strings.Replace(xdata, "'", "", -1)

	var price []byte
	var result []byte
	var err error
	var cmd *exec.Cmd

	// predict
	predict_cmd := fmt.Sprintf("python 5224test.py '%s'", xdata)
	fmt.Println("str = " + predict_cmd)
	// fmt.Println("xdata" + xdata)
	// cmd = exec.Command("powershell", str)
	cmd = exec.Command("cmd", "-c", predict_cmd)
	if price, err = cmd.Output(); err != nil {
		fmt.Println("err: " + err.Error())
	}
	fmt.Println("The price is", string(price))

	//recommend
	recommend_cmd := fmt.Sprintf("python 5224rectest.py '%s'", xdata)
	fmt.Println("str = " + recommend_cmd)
	// fmt.Println("xdata" + xdata)
	// cmd = exec.Command("powershell", str)
	cmd = exec.Command("cmd", "-c", recommend_cmd)
	if result, err = cmd.Output(); err != nil {
		fmt.Println("err: " + err.Error())
	}
	fmt.Println("The result is", result)

}

// '{\"listing_id\":123456,\"title\":\"test\",\"make\":\"\",\"model\":\"\",\"description\":\"ownerconsignmentunit,viewingstrictlybyappostringmentonly.pristineconditionwithlotsofupgradesdone.viewtobelieve!optiontopurchasewithoutcoe.flexibleloansolutions!call/whatsappoursalesconsultantnowtoarrangeforaviewingbeforeitsgone!\",\"manufactured\":2012,\"original_reg_date\":\"\",\"reg_date\":12,\"type_of_vehicle\":\"suv\",\"category\":\"\",\"transmission\":\"\",\"curb_weight\":0,\"power\":0,\"fuel_type\":\"\",\"engine_cap\":0,\"no_of_owners\":1,\"depreciation\":0,\"coe\":0,\"road_tax\":0,\"dereg_value\":0,\"mileage\":0,\"omv\":0,\"arf\":0,\"opc_scheme\":\"\",\"lifespan\":\"\",\"eco_category\":\"\",\"features\":\"smoothinline63.0lturbon55engine,highspecificationunit.viewspecsofthebmwx6\",\"accessories\":\"20''staggeredmrims,carbonsteeringwheel,10''andriodheadunit,hamannwidebodykit,kwcoilover,bmstuned.\",\"indicative_price\":0}'
// string VALUE: {"listing_id":123456,"title":"test","make":"","model":"","description":"ownerconsignmentunit, viewingstrictlybyappostringmentonly. pristineconditionwithlotsof upgradesdone. viewtobelieve!optiontopurchasewithout coe. flexible loan solutions! call/whatsapp our sales consultant now to arrange for a viewing before it's gone!","manufactured":2012,"original_reg_date":"","reg_date":12,"type_of_vehicle":"suv","category":"","transmission":"","curb_weight":0,"power":0,"fuel_type":"","engine_cap":0,"no_of_owners":1,"depreciation":0,"coe":0,"road_tax":0,"dereg_value":0,"mileage":0,"omv":0,"arf":0,"opc_scheme":"","lifespan":"","eco_category":"","features":"smooth inline 6 3.0l turbo n55 engine, high specification unit. view specs of the bmw x6","accessories":"20'' staggered m rims, carbon steering wheel, 10'' andriod headunit, hamann wide bodykit, kw coilover, bms tuned.","indicative_price":0}
// str = python 5224test.py '"$s"'%!(EXTRA string={"listing_id":123456,"title":"test","make":"","model":"","description":"ownerconsignmentunit, viewingstrictlybyappostringmentonly. pristineconditionwithlotsof upgradesdone. viewtobelieve!optiontopurchasewithout coe. flexible loan solutions! call/whatsapp our sales consultant now to arrange for a viewing before it's gone!","manufactured":2012,"original_reg_date":"","reg_date":12,"type_of_vehicle":"suv","category":"","transmission":"","curb_weight":0,"power":0,"fuel_type":"","engine_cap":0,"no_of_owners":1,"depreciation":0,"coe":0,"road_tax":0,"dereg_value":0,"mileage":0,"omv":0,"arf":0,"opc_scheme":"","lifespan":"","eco_category":"","features":"smooth inline 6 3.0l turbo n55 engine, high specification unit. view specs of the bmw x6","accessories":"20'' staggered m rims, carbon steering wheel, 10'' andriod headunit, hamann wide bodykit, kw coilover, bms tuned.","indicative_price":0})
// exec: "python 5224test.py '\"$s\"'%!(EXTRA string='{\"listing_id\":123456,\"title\":\"test\",\"make\":\"\",\"model\":\"\",\"description\":\"ownerconsignmentunit, viewingstrictlybyappostringmentonly. pristineconditionwithlotsof upgradesdone. viewtobelieve!optiontopurchasewithout coe. flexible loan solutions! call/whatsapp our sales consultant now to arrange for a viewing before it's gone!\",\"manufactured\":2012,\"original_reg_date\":\"\",\"reg_date\":12,\"type_of_vehicle\":\"suv\",\"category\":\"\",\"transmission\":\"\",\"curb_weight\":0,\"power\":0,\"fuel_type\":\"\",\"engine_cap\":0,\"no_of_owners\":1,\"depreciation\":0,\"coe\":0,\"road_tax\":0,\"dereg_value\":0,\"mileage\":0,\"omv\":0,\"arf\":0,\"opc_scheme\":\"\",\"lifespan\":\"\",\"eco_category\":\"\",\"features\":\"smooth inline 6 3.0l turbo n55 engine, high specification unit. view specs of the bmw x6\",\"accessories\":\"20'' staggered m rims, carbon steering wheel, 10'' andriod headunit, hamann wide bodykit, kw coilover, bms tuned.\",\"indicative_price\":0}')": file does not exist
