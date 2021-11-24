package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"regexp"
	"strconv"

	"log"
	"os"
	"sort"
	"strings"
	"unicode/utf8"
)

var alphabet = []string{"а", "б", "в", "г", "д", "е", "ж", "з", "a", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ы", "ь", "э", "ю", "я"}

var textPath string = "../docs/text.txt"

//func for checking errors
func check(err error) {
	if err != nil {
		log.Fatal(err)

	}
}

//func that replace letter in text, deleting spaces and returns array of text letters
func replaceLettersSpaces(path string) (string, string) {



	fileBytes, err := ioutil.ReadFile(path)
	check(err)
	sliceData := strings.Split(string(fileBytes), "\n")

	newLine := regexp.MustCompile("\n")
	withoutNewLine := newLine.ReplaceAllString(sliceData[0], ``)

	re := regexp.MustCompile(`ё`)
	tempText := re.ReplaceAllString(withoutNewLine, `е`)

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

	//fmt.Println(withSpaces, "\n")
	//fmt.Println(withoutSpaces, "\n")

	return withSpaces, withoutSpaces

}

//func that counts each letter in text
func lettersCount(text string) map[string]int {

	lettersCount := map[string]int{
		"а": 0, "б": 0, "в": 0, "г": 0, "д": 0, "е": 0, "ж": 0, "з": 0, "и": 0, "й": 0, "к": 0, "л": 0, "м": 0, "н": 0, "о": 0, "п": 0, "р": 0, "с": 0, "т": 0, "у": 0, "ф": 0, "х": 0, "ц": 0, "ч": 0, "ш": 0, "щ": 0, "ы": 0, "ь": 0, "э": 0, "ю": 0, "я": 0,
	}

	lettersArray := strings.Split(text, "")

	for i, _ := range lettersArray {
		for j, _ := range alphabet {
			if alphabet[j] == strings.ToLower(lettersArray[i]) {
				lettersCount[strings.ToLower(lettersArray[i])]++
				continue
			}
		}
	}

	return lettersCount
}

//structure for sorting array
type kv struct {
	Key   string
	Value float64
}

//func that count frequency and sorting frequency from high to low
//and return sorted map(dictionary) frequency of letters
func letterFrequency(text string) {

	lettersFrequency := map[string]float64{
		"а": 0, "б": 0, "в": 0, "г": 0, "д": 0, "е": 0, "ж": 0, "з": 0, "и": 0, "й": 0, "к": 0, "л": 0, "м": 0, "н": 0, "о": 0, "п": 0, "р": 0, "с": 0, "т": 0, "у": 0, "ф": 0, "х": 0, "ц": 0, "ч": 0, "ш": 0, "щ": 0, "ы": 0, "ь": 0, "э": 0, "ю": 0, "я": 0,
	}

	lettersCount(text)

	letters := lettersCount(text)

	count := utf8.RuneCountInString(text)
	//fmt.Println(count)

	for i, _ := range lettersFrequency {
		lettersFrequency[i] = float64(letters[i]) / float64(count)
	}

	var sortArr []kv
	for k, v := range lettersFrequency {
		sortArr = append(sortArr, kv{k, v})
	}

	sort.Slice(sortArr, func(i, j int) bool {
		return sortArr[i].Value > sortArr[j].Value
	})

	file, err := os.Create("../docs/lettersFrequency.txt")
	check(err)
	defer func(file *os.File) {
		err := file.Close()
		check(err)
	}(file)

	var frequencyToFile string
	var entropy float64


	for i := 0; i < len(sortArr); i++ {
		tempKey := sortArr[i].Key

		entropy += -sortArr[i].Value * math.Log(sortArr[i].Value)

		tempVal := strconv.FormatFloat(sortArr[i].Value, 'E', -1, 64)

		frequencyToFile = tempKey + ": " + tempVal + "\n"

		_, err := file.WriteString(frequencyToFile)
		check(err)

	}

	_, errEnt := file.WriteString("\nLetters Entropy: " +strconv.FormatFloat(entropy, 'f', 6, 64))
	check(errEnt)

}

func createCountBgrammsMatrix(text string) []string {

	tempArray := strings.Split(text, "")

	if len(tempArray)%2 != 0 {

		tempArray = append(tempArray, "ю")
	}

	var crossedBigrmas []string
	var unCrossedBigrmas []string

	for i := 0; i < len(tempArray)-1; i++ {
		crossedBigrmas = append(crossedBigrmas, strings.ToLower(tempArray[i])+strings.ToLower(tempArray[i+1]))
	}

	for i := 0; i < len(tempArray)-2; i++ {
		unCrossedBigrmas = append(unCrossedBigrmas, strings.ToLower(tempArray[i])+strings.ToLower(tempArray[i+2]))
	}

	crossBgrammsCount := map[string]int{}
	UncrossBgrammsCount := map[string]int{}

	for i := 0; i < len(crossedBigrmas); i++ {
		if _, ok := crossBgrammsCount[crossedBigrmas[i]]; ok {
			crossBgrammsCount[crossedBigrmas[i]]++
		} else {
			crossBgrammsCount[crossedBigrmas[i]] = 1
		}
	}

	for i := 0; i < len(unCrossedBigrmas); i++ {
		if _, ok := UncrossBgrammsCount[unCrossedBigrmas[i]]; ok {
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

	for key, value := range crossBgrammsCount {

		strVal := strconv.Itoa(value)

		_, err := CrossF.WriteString(key + ": " + strVal + "\n")
		check(err)

	}

	for key, value := range UncrossBgrammsCount {

		strVal := strconv.Itoa(value)

		_, err := UncrossF.WriteString(key + ": " + strVal + "\n")
		check(err)
	}

	CrossFreqF, err := os.OpenFile("../docs/CrossedBgramsFreq.txt", os.O_RDWR|os.O_CREATE, 0666)
	check(err)
	defer CrossFreqF.Close()

	UncrossFreqF, err := os.OpenFile("../docs/UnCrossedBgramsFreq.txt", os.O_RDWR|os.O_CREATE, 0666)
	check(err)
	defer UncrossFreqF.Close()

	lenText := len(text)
	floatValText := float64(lenText)

	var entCrossed float64
	var entUnCrossed float64

	CrossBgramFreq := map[string]float64{}

	for key, value := range crossBgrammsCount {

		entCrossed += -float64(value) * math.Log2(float64(value))

		var floatVal float64 = float64(value) / (floatValText - 1)

		CrossBgramFreq[key] = floatVal

		strVal := strconv.FormatFloat(floatVal, 'f', 6, 64)

		_, err := CrossFreqF.WriteString(key + ": " + strVal + "\n")
		check(err)
	}

	_, err = CrossFreqF.WriteString("\nEntropy: " + strconv.FormatFloat(entCrossed, 'f', 6, 64) + "\n")
	check(err)

	UncrBgramArr := []float64{}

	for key, value := range UncrossBgrammsCount {

		var floatVal float64 = float64(value) / 2

		strVal := strconv.FormatFloat(floatVal, 'f', 6, 64)

		UncrBgramArr = append(UncrBgramArr, floatVal)

		_, err := UncrossFreqF.WriteString(key + ": " + strVal + "\n")
		check(err)
	}

	for i:=0; i < len(UncrBgramArr); i++ {
		entUnCrossed += -UncrBgramArr[i] * math.Log(UncrBgramArr[i])
	}

	fmt.Println(UncrBgramArr)
	fmt.Println(len(UncrBgramArr))

	_, err = UncrossFreqF.WriteString("\nEntropy: " + strconv.FormatFloat(entUnCrossed, 'f', 6, 64) + "\n")
	check(err)

	return crossedBigrmas
}

func main() {

	_, withOutSpace := replaceLettersSpaces(textPath)

	lettersCount(withOutSpace)

	letterFrequency(withOutSpace)

	createCountBgrammsMatrix(withOutSpace)

}
