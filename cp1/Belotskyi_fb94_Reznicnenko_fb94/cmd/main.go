package main

import (
	"fmt"
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

func replaceLettersSpaces(path string) string{
	file, err := ioutil.ReadFile(path)
	check(err)

	var re = regexp.MustCompile(`ё`)
	text1 := re.ReplaceAllString(string(file), `е`)

	re = regexp.MustCompile(`ъ`)
	text2 := re.ReplaceAllString(string(text1), `ь`)

	f1, err := os.OpenFile("../docs/TextWithSpaces.txt", os.O_RDWR|os.O_CREATE, 0666)
	check(err)
	f1.Truncate(0)

	_, err2 := f1.WriteString(text2)
	check(err2)

	spaces := regexp.MustCompile(` `)
	withoutSpaces := spaces.ReplaceAllString(string(text2), ``)

	f2, err := os.OpenFile("../docs/TextWithoutSpaces.txt", os.O_RDWR|os.O_CREATE, 0666)
	check(err)
	f2.Truncate(0)

	_, err3 := f2.WriteString(withoutSpaces)
	check(err3)

	return withoutSpaces

}

func countLetters(text string) map[string]int{

	lettersCount := map[string]int{
		"a": 0,
		"б": 0,
		"в": 0,
		"г": 0,
		"д": 0,
		"е": 0,
		"ж": 0,
		"з": 0,
		"и": 0,
		"й": 0,
		"к": 0,
		"л": 0,
		"м": 0,
		"н": 0,
		"о": 0,
		"п": 0,
		"р": 0,
		"с": 0,
		"т": 0,
		"у": 0,
		"ф": 0,
		"х": 0,
		"ц": 0,
		"ч": 0,
		"ш": 0,
		"щ": 0,
		"ы": 0,
		"ь": 0,
		"э": 0,
		"ю": 0,
		"я": 0,
	}
	alphabet := []string{
		"a",
		"б",
		"в",
		"г",
		"д",
		"е",
		"ж",
		"з",
		"и",
		"й",
		"к",
		"л",
		"м",
		"н",
		"о",
		"п",
		"р",
		"с",
		"т",
		"у",
		"ф",
		"х",
		"ц",
		"ч",
		"ш",
		"щ",
		"ы",
		"ь",
		"э",
		"ю",
		"я",
	}
	lettersArray := strings.Split(text, "")

	for i, _ := range lettersArray{
		for j, _ := range alphabet {
			if alphabet[j] == strings.ToLower(lettersArray[i])  {
				lettersCount[strings.ToLower(lettersArray[i])]++
				continue
			}
		}
	}
	return lettersCount
}

func main(){

	text := replaceLettersSpaces("../docs/text.txt")

	//count := utf8.RuneCountInString(text)
	//fmt.Println(count)

	fmt.Println(countLetters(text))

}