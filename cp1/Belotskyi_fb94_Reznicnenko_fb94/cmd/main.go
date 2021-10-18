package main

import (
	"io/ioutil"
	"log"
	"os"
	"regexp"
	"strings"
)

func check(err error){
	if err != nil{
		log.Fatal(err)
	}
}

func main(){
	file, err := ioutil.ReadFile("../docs/text.txt")
	check(err)

	var re = regexp.MustCompile(`[[:punct:]]`)

	text := re.ReplaceAllString(string(file), "")

	noDashes := strings.Replace(text, "—", "", -1)

	noDoubleSpace := strings.Replace(noDashes, "  ", "", -1)

	fileToWrite, err2 := os.OpenFile("../docs/TextWithSpaces.txt", os.O_RDWR|os.O_APPEND, 0660)
	defer fileToWrite.Close()

	check(err2)

	_, err3 := fileToWrite.WriteString(noDoubleSpace)

	check(err3)

	//fmt.Println(noDoubleSpace)

}