package dao

import (
	"CS5224/pkg/log"
	"fmt"

	_ "github.com/go-sql-driver/mysql"
	"github.com/jmoiron/sqlx"
)

const (
	username = "admin"
	password = "admin666"
	dbHost   = "database-2.ckzihnf4uip0.us-east-1.rds.amazonaws.com"
	dbPort   = 3306
	dbName   = "carguru"
)

var (
	rds RDS
)

type RDS struct {
	db *sqlx.DB
}

func InitDB() {
	dbEndpoint := fmt.Sprintf("%s:%s@tcp(%s:%d)/%s", username, password, dbHost, dbPort, dbName)
	log.Logger.Infof(dbEndpoint)
	db, err := sqlx.Open("mysql", dbEndpoint)
	if err != nil {
		log.Logger.Errorf("init db error: %+v", err)
		panic(err)
	}
	rds.db = db
}

func GetCarByID(id int) Car {
	car := Car{}
	query := fmt.Sprintf("select * from car where listing_id=%d", id)
	err := rds.db.Get(&car, query)
	if err != nil {
		log.Logger.Info("Query failed : %s, err: %v", query, err)
	}
	return formatCar(car)
}

func SearchCar(params *CarParams) ([]Car, error) {
	cars := make([]Car, 0)
	query := "select * from car where 1=1"
	if len(params.Title) > 0 {
		query += fmt.Sprintf(" and title like \"%%%v%%\"", params.Title)
	}
	if params.ManufacturedMax > 0 {
		query += fmt.Sprintf(" and manufactured < %d", params.ManufacturedMax)
	}
	if params.ManufacturedMin > 0 {
		query += fmt.Sprintf(" and manufactured > %d", params.ManufacturedMin)
	}
	if len(params.TypeOfVehicle) > 0 {
		query += fmt.Sprintf(" and type_of_vehicle=\"%v\"", params.TypeOfVehicle)
	}
	if len(params.Transmission) > 0 {
		query += fmt.Sprintf(" and transmission=\"%v\"", params.Transmission)
	}
	if params.PriceMax > 0 {
		query += fmt.Sprintf(" and price < %d", params.PriceMax)
	}
	if params.PriceMin > 0 {
		query += fmt.Sprintf(" and manufactured > %d", params.PriceMin)
	}
	if len(params.OrderBy) > 0 {
		query += fmt.Sprintf(" order by %v", params.OrderBy)
	}
	// query += " limit 1;"
	if err := rds.db.Select(&cars, query); err != nil {
		log.Logger.Errorf("Query failed : %s, err: %v", query, err)
		return nil, err
	}
	return formatCars(cars), nil
}

func formatCar(target Car) Car {
	target.Title = formatString(target.Title)
	target.Description = formatString(target.Description)
	target.Category = formatString(target.Category)
	target.Features = formatString(target.Features)
	target.Accessories = formatString(target.Accessories)
	return target
}

func formatCars(target []Car) []Car {
	res := make([]Car, 0)
	for _, car := range target {
		res = append(res, formatCar(car))
	}
	return res
}

func formatString(s string) string {
	if len(s) > 0 && s[0] == '"' {
		s = s[1:]
	}
	if len(s) > 0 && s[len(s)-1] == '"' {
		s = s[:len(s)-1]
	}
	return s
}
