package biz

import (
	"CS5224/biz/handlers"
	"github.com/gin-gonic/gin"
	"net/http"
)

func RegisterRouters(router *gin.Engine) {
	// Query string parameters are parsed using the existing underlying request object.
	// The request responds to an url matching:  /welcome?firstname=Jane&lastname=Doe
	router.GET("/welcome", Welcome)
	router.POST("/get_cars", handlers.GetCars)
	router.POST("/add_cars", handlers.AddCars)
	router.POST("/recommend_cars", handlers.RecommendCars)
	router.POST("/evaluate_car", handlers.EvaluateCar)
}

func Welcome(c *gin.Context) {
	firstname := c.DefaultQuery("firstname", "Guest")
	lastname := c.Query("lastname") // shortcut for c.Request.URL.Query().Get("lastname")
	c.String(http.StatusOK, "Hello %s %s\n You are from: %s", firstname, lastname, c.ClientIP())
}
