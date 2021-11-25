package main

import (
	"io/ioutil"
	"log"
	"math"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

var alphabet = []string{"а", "б", "в", "г", "д", "е", "ж", "з", "a", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ы", "ь", "э", "ю", "я"}
var textLen int

func check(err error) {
	if err != nil {
		log.Fatal(err)

	}
}

func openReportFile() (f *os.File) {
	f, err := os.OpenFile("..docs/report.txt", os.O_RDWR|os.O_CREATE, 0666)
	check(err)
	defer func(f *os.File) {
		err := f.Close()
		if err != nil {

		}
	}(f)

	return f
}

func replaceLetters() (string, string) {
	textFile, err := ioutil.ReadFile("../docs/text.txt")
	check(err)

	clearText := string(textFile)

	regexp.MustCompile("\n").ReplaceAllString(clearText, ``)
	regexp.MustCompile(`ё`).ReplaceAllString(clearText, `е`)
	regexp.MustCompile(`ъ`).ReplaceAllString(clearText, `ь`)

	noSpace := regexp.MustCompile(` `).ReplaceAllString(clearText, ``)

	textLen = len(noSpace)

	return clearText, noSpace

}

//struct for sorting letters frequency

type Pair struct {
	Key   string
	Value float64
}

type PairList []Pair

func (p PairList) Len() int           { return len(p) }
func (p PairList) Swap(i, j int)      { p[i], p[j] = p[j], p[i] }
func (p PairList) Less(i, j int) bool { return p[i].Value < p[j].Value }

//counting letters count and frequency
func lettersCountFreq(text string) (map[string]int, []string) {

	lettersCount := map[string]int{}
	lettersFreq := map[string]float64{}

	textArray := strings.Split(text, "")

	for i, _ := range textArray {
		for j, _ := range alphabet {
			if alphabet[j] == strings.ToLower(textArray[i]) {
				lettersCount[strings.ToLower(textArray[i])]++
			}
		}
	}

	var lettersInText int

	for _, val := range lettersCount {
		lettersInText += val
	}

	for key, val := range lettersCount {
		lettersFreq[key] = float64(val) / float64(lettersInText)
	}

	p := make(PairList, len(lettersFreq))
	sortedLettersFreq := make([]string, len(lettersFreq))

	i := 0
	for k, v := range lettersFreq {
		p[i] = Pair{k, v}
		i++
	}
	sort.Sort(sort.Reverse(p))

	for _, k := range p {
		stringToArray := k.Key + ": " + strconv.FormatFloat(k.Value, 'f', 6, 64)
		sortedLettersFreq = append(sortedLettersFreq, stringToArray)
	}

	return lettersCount, sortedLettersFreq
}

func bgrammsCount(text string) (map[string]float64, map[string]float64) {

	crossedBgrammCount := map[string]float64{}
	unCrossedBgrammCount := map[string]float64{}

	textArray := strings.Split(text, "")

	for i := 0; i < len(textArray)-1; i++ {
		if textArray[i] == " " {
			i++
		} else {
			crossedBgrammCount[strings.ToLower(textArray[i])+strings.ToLower(textArray[i+1])]++
		}

	}

	for i := 0; i < len(textArray)-2; i += 2 {
		unCrossedBgrammCount[strings.ToLower(textArray[i])+strings.ToLower(textArray[i+1])]++
	}

	return crossedBgrammCount, unCrossedBgrammCount

}

func bgrammsFreq(cross map[string]int, unCross map[string]int) (map[string]float64, map[string]float64){

	crossFreq := map[string]float64{}
	unCrossFreq := map[string]float64{}

	for key, val := range cross{
		crossFreq[key] = float64(val) / float64(textLen - 1)
	}

	for key, val := range unCross{
		unCrossFreq[key] = float64(val) / 2
	}

	return crossFreq, unCrossFreq
}

func entropy(freq map[string]float64) float64{

	var entropy float64 = 0
	//fmt.Println(len(freq))

	for _, val := range freq{
		entropy += -val * math.Log2(val)
	}

	return entropy

}

func main() {
	text, _ := replaceLetters()
	test1, test2 := bgrammsCount(text)
	entropy(test1)
	entropy(test2)

	//fmt.Println(text)

}
