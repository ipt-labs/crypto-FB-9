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

	fileWithSpaces, err2 := os.OpenFile("../docs/TextWithSpaces.txt", os.O_RDWR|os.O_APPEND, 0660)

	check(err2)

	_, err3 := fileWithSpaces.WriteString(noDoubleSpace)
	check(err3)

	noSpaces := strings.Replace(noDoubleSpace, " ", "", -1)

	fileWithoutSpaces, err4 := os.OpenFile("../docs/TextWithoutSpaces.txt", os.O_RDWR|os.O_APPEND, 0660)
	check(err4)

	_, err5 := fileWithoutSpaces.WriteString(noSpaces)
	check(err5)

	//fmt.Println(noDoubleSpace)

}