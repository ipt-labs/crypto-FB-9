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

func replaceLettersSpaces(path string){
	file, err := ioutil.ReadFile(path)
	check(err)

	var re = regexp.MustCompile(`ё`)
	text1 := re.ReplaceAllString(string(file), `е`)

	re = regexp.MustCompile(`ъ`)
	text2 := re.ReplaceAllString(string(text1), `ь`)

	f1, err := os.OpenFile("../docs/TextWithSpaces.txt", os.O_RDWR|os.O_APPEND|os.O_CREATE, 0666)
	check(err)

	_, err2 := f1.WriteString(text1)
	check(err2)

	spaces := regexp.MustCompile(` `)
	withoutSpaces := spaces.ReplaceAllString(string(text2), ``)

	f2, err := os.OpenFile("../docs/TextWithoutSpaces.txt", os.O_RDWR|os.O_APPEND|os.O_CREATE, 0666)
	check(err)

	_, err3 := f2.WriteString(withoutSpaces)
	check(err3)

}


func main(){

	replaceLettersSpaces("../docs/text.txt")

}

