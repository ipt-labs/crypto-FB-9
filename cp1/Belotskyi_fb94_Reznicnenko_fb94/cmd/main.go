package main

import (
	"io/ioutil"
	"log"
	"os"
	"regexp"
)

func check(err error){
	if err != nil{
		log.Fatal(err)
	}
}

func replaceLetters(path string) string {
	file, err := ioutil.ReadFile(path)
	check(err)

	var re = regexp.MustCompile(`ё`)
	text1 := re.ReplaceAllString(string(file), `е`)

	re = regexp.MustCompile(`ъ`)
	text2 := re.ReplaceAllString(string(text1), `ь`)

	return text2
}


func main(){

	text := replaceLetters("../docs/text.txt")

	file, err := os.OpenFile("../docs/TextWithSpaces.txt", os.O_RDWR|os.O_APPEND|os.O_CREATE, 0666)
	check(err)

	_, err2 := file.WriteString(text)
	check(err2)
}

