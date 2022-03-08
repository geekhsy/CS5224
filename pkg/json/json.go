package json

import (
	jsoniter "github.com/json-iterator/go"
	"io"
)

var json = jsoniter.ConfigCompatibleWithStandardLibrary

func ToString(v interface{}) string {
	s, _ := json.MarshalToString(v)
	return s
}

func Marshal(v interface{}) ([]byte, error) {
	return json.Marshal(v)
}
func MarshalIndent(v interface{}, prefix, indent string) ([]byte, error) {
	return json.MarshalIndent(v, prefix, indent)
}
func UnmarshalFromString(str string, v interface{}) error {
	return json.UnmarshalFromString(str, v)
}
func Unmarshal(data []byte, v interface{}) error {
	return json.Unmarshal(data, v)
}
func Get(data []byte, path ...interface{}) jsoniter.Any {
	return json.Get(data, path)
}
func NewEncoder(writer io.Writer) *jsoniter.Encoder {
	return json.NewEncoder(writer)
}
func NewDecoder(reader io.Reader) *jsoniter.Decoder {
	return json.NewDecoder(reader)
}
func Valid(data []byte) bool {
	return json.Valid(data)
}
