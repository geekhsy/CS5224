package dao

type Car struct {
	ListingID       int    `db:"listing_id" json:"listing_id,omitempty"`
	Title           string `db:"title" json:"title,omitempty"`
	Make            string `db:"make" json:"make,omitempty"`
	Model           string `db:"model" json:"model,omitempty"`
	Description     string `db:"description" json:"description,omitempty"`
	Manufactured    string `db:"manufactured" json:"manufactured,omitempty"`
	OriginalRegDate string `db:"original_reg_date" json:"original_reg_date,omitempty"`
	RegDate         string `db:"reg_date" json:"reg_date,omitempty"`
	TypeOfVehicle   string `db:"type_of_vehicle" json:"type_of_vehicle,omitempty"`
	Category        string `db:"category" json:"category,omitempty"`
	Transmission    string `db:"transmission" json:"transmission,omitempty"`
	CurbWeight      int    `db:"curb_weight" json:"curb_weight,omitempty"`
	Power           int    `db:"power" json:"power,omitempty"`
	FuelType        string `db:"fuel_type" json:"fuel_type,omitempty"`
	EngineCap       int    `db:"engine_cap" json:"engine_cap,omitempty"`
	NoOfOwners      int    `db:"no_of_owners" json:"no_of_owners,omitempty"`
	Depreciation    int    `db:"depreciation" json:"depreciation,omitempty"`
	Coe             int    `db:"coe" json:"coe,omitempty"`
	RoadTax         int    `db:"road_tax" json:"road_tax,omitempty"`
	DeregValue      int    `db:"dereg_value" json:"dereg_value,omitempty"`
	Mileage         int64  `db:"mileage" json:"mileage,omitempty"`
	Omv             int    `db:"omv" json:"omv,omitempty"`
	Arf             int    `db:"arf" json:"arf,omitempty"`
	OpcScheme       string `db:"opc_scheme" json:"opc_scheme,omitempty"`
	Lifespan        string `db:"lifespan" json:"lifespan,omitempty"`
	EcoCategory     string `db:"eco_category" json:"eco_category,omitempty"`
	Features        string `db:"features" json:"features,omitempty"`
	Accessories     string `db:"accessories" json:"accessories,omitempty"`
	IndicativePrice int    `db:"indicative_price" json:"indicative_price,omitempty"`
	Price           int64  `db:"price" json:"price,omitempty"`
}

type TransmissionTypeEnum string

const (
	TransmissionTypeEnum_Auto   TransmissionTypeEnum = "auto"
	TransmissionTypeEnum_Manual TransmissionTypeEnum = "manual"
)

type OrderByConditionsEnum string

type CarParams struct {
	Title           string
	ManufacturedMax int
	ManufacturedMin int
	TypeOfVehicle   string
	Transmission    TransmissionTypeEnum
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
