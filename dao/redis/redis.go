package redis

import (
	"fmt"
	"github.com/go-redis/redis"
)

var Client *redis.Client

func InitRedisClient() {
	Client = redis.NewClient(&redis.Options{
		Addr:     "carguru.ow3jum.0001.use1.cache.amazonaws.com:6379",
		Password: "", // no password set
		DB:       0,  // use default DB
	})

	//if _, err := Client.Ping().Result(); err != nil {
	//	panic(err)
	//}
}

func GenCarKey(listID string) string {
	return fmt.Sprintf("add_car_%s_lock", listID)
}
