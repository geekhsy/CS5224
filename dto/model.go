package dto

type Car struct {
	ListingID       int    `db:"listing_id"`
	Title           string `db:"title"`
	Make            string `db:"make"`
	Model           string `db:"model"`
	Description     string `db:"description"`
	Manufactured    string `db:"manufactured"`
	OriginalRegDate string `db:"original_reg_date"`
	RegDate         string `db:"reg_date"`
	TypeOfVehicle   string `db:"type_of_vehicle"`
	Category        string `db:"category"`
	Transmission    string `db:"transmission"`
	CurbWeight      int    `db:"curb_weight"`
	Power           int    `db:"power"`
	FuelType        string `db:"fuel_type"`
	EngineCap       int    `db:"engine_cap"`
	NoOfOwners      int    `db:"no_of_owners"`
	Depreciation    int    `db:"depreciation"`
	Coe             int    `db:"coe"`
	RoadTax         int    `db:"road_tax"`
	DeregValue      int    `db:"dereg_value"`
	Mileage         int    `db:"mileage"`
	Omv             int    `db:"omv"`
	Arf             int    `db:"arf"`
	OpcScheme       string `db:"opc_scheme"`
	Lifespan        string `db:"lifespan"`
	EcoCategory     string `db:"eco_category"`
	Features        string `db:"features"`
	Accessories     string `db:"accessories"`
	IndicativePrice int    `db:"indicative_price"`
	Price           int    `db:"price"`
}

type CarParams struct {
	Title           string
	ManufacturedMax int
	ManufacturedMin int
	TypeOfVehicle   string
	Transmission    string
	PriceMax        int
	PriceMin        int
	OrderBy         string
}

type CarResponse struct {
	Cars []Car
}

type User struct {
	Username string
	Password string
}
