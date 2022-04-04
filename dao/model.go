package dao

type Car struct {
	ListingID       int    `db:"listing_id" json:"listingID,omitempty"`
	Title           string `db:"title" json:"title,omitempty"`
	Make            string `db:"make" json:"make,omitempty"`
	Model           string `db:"model" json:"model,omitempty"`
	Description     string `db:"description" json:"description,omitempty"`
	Manufactured    string `db:"manufactured" json:"manufactured,omitempty"`
	OriginalRegDate string `db:"original_reg_date" json:"originalRegDate,omitempty"`
	RegDate         string `db:"reg_date" json:"regDate,omitempty"`
	TypeOfVehicle   string `db:"type_of_vehicle" json:"typeOfVehicle,omitempty"`
	Category        string `db:"category" json:"category,omitempty"`
	Transmission    string `db:"transmission" json:"transmission,omitempty"`
	CurbWeight      int    `db:"curb_weight" json:"curbWeight,omitempty"`
	Power           int    `db:"power" json:"power,omitempty"`
	FuelType        string `db:"fuel_type" json:"fuelType,omitempty"`
	EngineCap       int    `db:"engine_cap" json:"engineCap,omitempty"`
	NoOfOwners      int    `db:"no_of_owners" json:"noOfOwners,omitempty"`
	Depreciation    int    `db:"depreciation" json:"depreciation,omitempty"`
	Coe             int    `db:"coe" json:"coe,omitempty"`
	RoadTax         int    `db:"road_tax" json:"roadTax,omitempty"`
	DeregValue      int    `db:"dereg_value" json:"deregValue,omitempty"`
	Mileage         int    `db:"mileage" json:"mileage,omitempty"`
	Omv             int    `db:"omv" json:"omv,omitempty"`
	Arf             int    `db:"arf" json:"arf,omitempty"`
	OpcScheme       string `db:"opc_scheme" json:"opcScheme,omitempty"`
	Lifespan        string `db:"lifespan" json:"lifespan,omitempty"`
	EcoCategory     string `db:"eco_category" json:"ecoCategory,omitempty"`
	Features        string `db:"features" json:"features,omitempty"`
	Accessories     string `db:"accessories" json:"accessories,omitempty"`
	IndicativePrice int    `db:"indicative_price" json:"indicativePrice,omitempty"`
	Price           int64  `db:"price" json:"price,omitempty"`
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
