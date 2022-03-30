package model

type Car struct {
	Model          string `form:"model" json:"model"`
	Price          int64  `form:"price" json:"price"`
	Brand          string `form:"brand" json:"brand"`
	ProductionYear int64  `from:"production_year" json:"production_year"`
	URL            string `from:"URL" json:"URL"`
}
