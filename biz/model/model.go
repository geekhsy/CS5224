package model

type Car struct {
	Title          string `form:"title" json:"title"`
	Model          string `form:"model" json:"model"`
	Price          int64  `form:"price" json:"price"`
	Mileage        int64  `form:"mileage" json:"mileage"`
	ProductionYear string `form:"production_year" json:"production_year"`
	URL            string `form:"URL" json:"URL"`
}
