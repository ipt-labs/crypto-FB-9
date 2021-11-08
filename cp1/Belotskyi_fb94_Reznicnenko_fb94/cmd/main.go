package main

import (
	"fmt"
	"io/ioutil"
	"regexp"

	//"io/ioutil"
	"log"
	"os"
	"sort"
	"strings"
	"unicode/utf8"
)

var alphabet = []string{"а", "б","в", "г", "д", "е", "ж","з", "a", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ы", "ь", "э", "ю", "я"}

//func for checking errors
func check(err error){
	if err != nil{
		log.Fatal(err)

	}
}

//func that replace letter in text, deleting spaces and returns array of text letters
func replaceLettersSpaces(path string) (string, string){

	fileBytes, err := ioutil.ReadFile(path)
	check(err)
	sliceData := strings.Split(string(fileBytes), "\n")

	//fmt.Println(sliceData)

	var re = regexp.MustCompile(`ё`)
	tempText := re.ReplaceAllString(sliceData[0], `е`)

	re = regexp.MustCompile(`ъ`)
	withSpaces := re.ReplaceAllString(string(tempText), `ь`)

	f1, err := os.OpenFile("../docs/TextWithSpaces.txt", os.O_RDWR|os.O_CREATE, 0666)
	check(err)

	f1TruncateErr := f1.Truncate(0)
	check(f1TruncateErr)

	_, err = f1.WriteString(withSpaces)
	check(err)

	spaces := regexp.MustCompile(` `)
	withoutSpaces := spaces.ReplaceAllString(string(withSpaces), ``)

	f2, f2Err := os.OpenFile("../docs/TextWithoutSpaces.txt", os.O_RDWR|os.O_CREATE, 0666)
	check(f2Err)

	f2TruncateErr := f2.Truncate(0)
	check(f2TruncateErr)

	_, err3 := f2.WriteString(withoutSpaces)
	check(err3)

	return withSpaces, withoutSpaces

}

//func that counts each letter in text
func lettersCount(text string) map[string]int{

	lettersCount := map[string]int{
		"а": 0, "б": 0, "в": 0, "г": 0, "д": 0, "е": 0, "ж": 0, "з": 0, "и": 0, "й": 0, "к": 0, "л": 0, "м": 0, "н": 0, "о": 0, "п": 0, "р": 0, "с": 0, "т": 0, "у": 0, "ф": 0, "х": 0, "ц": 0, "ч": 0, "ш": 0, "щ": 0, "ы": 0, "ь": 0, "э": 0, "ю": 0, "я": 0,
	}

	alphabet := []string{"а", "б","в", "г", "д", "е", "ж","з", "a", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ы", "ь", "э", "ю", "я"}

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
func letterFrequency(text string) map[string]float64 {

	lettersFrequency := map[string]float64{
		"а": 0, "б": 0, "в": 0, "г": 0, "д": 0, "е": 0, "ж": 0, "з": 0, "и": 0, "й": 0, "к": 0, "л": 0, "м": 0, "н": 0, "о": 0, "п": 0, "р": 0, "с": 0, "т": 0, "у": 0, "ф": 0, "х": 0, "ц": 0, "ч": 0, "ш": 0, "щ": 0, "ы": 0, "ь": 0, "э": 0, "ю": 0, "я": 0,
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

	sortedFrequency := make(map[string]float64)

	sort.Slice(sortArr, func(i, j int) bool {
		return sortArr[i].Value > sortArr[j].Value
	})


	for i:=0; i<len(sortArr);i++{
		tempKey := sortArr[i].Key
		tempVal := sortArr[i].Value

		fmt.Println(tempKey, ": ", tempVal)

		sortedFrequency[sortArr[i].Key] = sortArr[i].Value
	}

	file, err := os.Create("../docs/lettersFrequency")
	check(err)
	defer func(file *os.File) {
		err := file.Close()
		check(err)
	}(file)

	//for _, kv := range sortArr {
	//	//sortedFrequency[kv.Key] = kv.Value
	//	//fmt.Printf("%s: %v\n", kv.Key, kv.Value)
	//}


	fmt.Println(sortedFrequency)


	return sortedFrequency
}

func createCountBgrammsMatrix(text string) []string {

	tempArray := strings.Split(text, "")

	if len(tempArray) % 2 == 0 {
		tempArray = append(tempArray, "ю")

	}

	var crossedBigrmas []string
	var unCrossedBigrmas []string

	for i := 0; i < len(tempArray) - 1; i++{
		crossedBigrmas = append(crossedBigrmas, strings.ToLower(tempArray[i]) + strings.ToLower(tempArray[i+1]))
	}

	for i := 0; i < len(tempArray) - 2; i++{
		unCrossedBigrmas = append(unCrossedBigrmas, strings.ToLower(tempArray[i]) + strings.ToLower(tempArray[i+2]))
	}


	crossBgrammsCount := map[string]int{}
	UncrossBgrammsCount := map[string]int{}

	for i:=0; i < len(crossedBigrmas); i++{
		if _, ok := crossBgrammsCount[crossedBigrmas[i]]; ok{
			crossBgrammsCount[crossedBigrmas[i]]++
		} else {
			crossBgrammsCount[crossedBigrmas[i]] = 1
		}
	}

	for i:=0; i < len(unCrossedBigrmas); i++{
		if _, ok := UncrossBgrammsCount[unCrossedBigrmas[i]]; ok{
			UncrossBgrammsCount[unCrossedBigrmas[i]]++
		} else {
			UncrossBgrammsCount[unCrossedBigrmas[i]] = 1
		}
	}

	CrossF, err := os.OpenFile("../docs/crossedBgrams.txt", os.O_RDWR|os.O_CREATE, 0666)
	check(err)



	UncrossF, err := os.OpenFile("../docs/UnCrossedBgrams.txt", os.O_RDWR|os.O_CREATE, 0666)
	check(err)


	truncateErr := CrossF.Truncate(0)
	check(truncateErr)

	truncateErr = UncrossF.Truncate(0)
	check(truncateErr)



	for key, value := range crossBgrammsCount{
		_, err := CrossF.Write([]byte(string(key) + ": " + string(rune(value)) + "\n"))
		check(err)
	}


	for key, value := range UncrossBgrammsCount{
			_, err := UncrossF.Write([]byte(string(key) + ": " + string(rune(value)) + "\n"))
			check(err)
		}


	return crossedBigrmas
}

func main(){

	_, withOutSpaces :=  replaceLettersSpaces("../docs/text.txt")

	createCountBgrammsMatrix(withOutSpaces)

	letterFrequency(withOutSpaces)

}