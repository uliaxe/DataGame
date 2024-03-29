// server who print vgsales.json

package main	

import (
	"net/http"
	"io/ioutil"
	"fmt"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		data, err := ioutil.ReadFile("vgsales.json")
		if err != nil {
			fmt.Fprintf(w, "Error: %v", err)
			return
		}
		fmt.Fprintf(w, "%s", data)
	})
	http.ListenAndServe(":8080", nil)
}

