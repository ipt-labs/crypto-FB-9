package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"regexp"
	"sort"
	"strings"
	"unicode/utf8"
)


var alphabet = []string{
"а",
"б",
"в",
"г",
"д",
"е",
"ж",
"з",
"a",
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


//func for checking errors
func check(err error){
	if err != nil{
		log.Fatal(err)
	}
}

//func that replace letter in text, deleting spaces and returns array of text letters
func replaceLettersSpaces(path string) (string, string){
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

	return text2, withoutSpaces

}

//func that counts each letter in text
func lettersCount(text string) map[string]int{

	lettersCount := map[string]int{

		"а": 0,
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

//structure for sorting array
type kv struct{
	Key string
	Value float64
}

//func that count frequency and sorting frequency from high to low
//and return sorted map(dictionary) frequency of letters
func frequency(text string) map[string]float64 {

	lettersFrequency := map[string]float64{

		"а": 0,
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

	lettersCount(text)

	letters := lettersCount(text)

	count := utf8.RuneCountInString(text)

	for i, _ := range lettersFrequency{
		lettersFrequency[i] = float64(letters[i]) / float64(count)
	}


	var sortArr []kv
	for k, v := range lettersFrequency{
		sortArr = append(sortArr, kv{k, v})
	}

	sort.Slice(sortArr, func(i, j int) bool {
		return sortArr[i].Value > sortArr[j].Value
	})

	sortedFrequency := map[string]float64{}

	for _, kv := range sortArr {
		//fmt.Printf("%s: %v\n", kv.Key, kv.Value)
		sortedFrequency[kv.Key] = kv.Value
	}

	return sortedFrequency

}

func createBgrammsMatrix(text string) []string {

	tempArray := strings.Split(text, "")

	if len(tempArray) % 2 == 0 {
		tempArray = append(tempArray, "ю")
	}

	var lettersArray []string
	for i := 0; i <= len(tempArray) - 2; i++{
		lettersArray = append(lettersArray, strings.ToLower(tempArray[i]) + strings.ToLower(tempArray[i+1]))
	}
	return lettersArray

}

func main(){

	_,withoutSpace := replaceLettersSpaces("../docs/text.txt")

	//count := utf8.RuneCountInString(withOutSpaces)
	//fmt.Println(count)
	//
	//fmt.Println(lettersCount(WithSpaces))

	//fmt.Print(frequency(WithSpaces),"\n\n")
	//fmt.Print(frequency(withOutSpaces))
	arr := createBgrammsMatrix(withoutSpace)

	fmt.Println(arr[len(arr)-1])
}