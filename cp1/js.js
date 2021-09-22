let alpha = {
  й: 0,
  ц: 0,
  у: 0,
  к: 0,
  е: 0,
  н: 0,
  г: 0,
  ш: 0,
  щ: 0,
  з: 0,
  х: 0,
  ъ: 0,
  ф: 0,
  ы: 0,
  в: 0,
  а: 0,
  п: 0,
  р: 0,
  о: 0,
  л: 0,
  д: 0,
  ж: 0,
  э: 0,
  я: 0,
  ч: 0,
  с: 0,
  м: 0,
  и: 0,
  т: 0,
  ь: 0,
  б: 0,
  ю: 0,
  " ": 0,
};
let keys = Object.keys(alpha);
document.querySelector("button").addEventListener("click", function () {
  let file = document.getElementById("file").files[0];
  let reader = new FileReader();
  reader.readAsText(file);
  reader.onload = function () {
    //console.log(reader.result);
    letters(textEditor(reader.result, true), alpha, keys, 1);
    letters(textEditor(reader.result, false), alpha, keys, 2);
    bigrams(textEditor(reader.result), true, 3)
    bigrams(textEditor(reader.result), false, 4)
  };
  reader.onerror = function () {
    console.log(reader.error);
  };
});

function textEditor(text, spaces) {
  let editText;
  if (spaces) {
    editText = text.replace(/[!-@]|[\[-`]|[\{-~]|I|—|…/gi, "").toLowerCase();
    //console.log(editText);
  } else {
    editText = text
      .replace(/[ -@]|[\[-`]|[\{-~]|I|—|…/gi, "")
      .trim()
      .toLowerCase();
    //console.log(editText);
  }

  return editText;
}

function appendList(obj, iteration) {
  let ulList = document.createElement("ul");
  ulList.classList.add("letters" + iteration);
  //console.log(ulList.style);
  //ulList.style="display: inline-block"
  for (let key in obj) {
    let liEl = document.createElement("li");
    liEl.textContent = key + ": " + obj[key];
    ulList.append(liEl);
  }
  document.querySelector(".uls").append(ulList);
}

function sortObj(alphabet) {
  let sortable = [];
  for (let letter in alphabet) {
    sortable.push([letter, alphabet[letter]]);
  }

  sortable.sort(function (a, b) {
    return b[1] - a[1];
  });
  let objSorted = {};
  sortable.forEach((item) => {
    objSorted[item[0]] = item[1];
  });
  return objSorted;
}

function redundency(x, y) {
  return 1 - x / Math.log2(y);
}

function letters(text, alphabet, keys, iteration) {
  console.log(alphabet);
  console.log(alpha);
  console.log(iteration);
  for (let letter of text) {
    for (let key of keys) {
      if (key == letter) {
        alphabet[letter]++;
      }
    }
  }
  for (let el of keys) {
    alphabet[el] = alphabet[el] / text.length;
  }
  //console.log(alphabet);
  let varArr = [];
  for (let val of Object.values(alphabet)) {
    if (val > 0) varArr.push(-val * Math.log2(val));
  }
  //console.log(varArr);
  //console.log(alphabet);
  let summ = 0;
  for (let val of varArr) {
    summ += val;
  }
  //console.log(summ, " and sets redundency ", redundency(summ, keys.length));
  appendList(sortObj(alphabet), iteration);
}

function bigrams(text, inters, iteration) {
  let bigram;
  let bigrams = [];
  let bigramsObj = {};
  if (inters) {
    for (let i = 0; i < text.length - 1; i++) {
      bigram = text[i] + text[i + 1];
      bigrams.push(bigram);
    }
    for (let i = 0; i < bigrams.length; i++) {
      if (bigramsObj[bigrams[i]] != undefined) bigramsObj[bigrams[i]]++;
      else bigramsObj[bigrams[i]] = 1;
    }
    //console.log(bigramsObj);
    //bigramsObj=probability(bigramsObj, text.length)
    for (let el in bigramsObj) {
      bigramsObj[el] = bigramsObj[el] / text.length;
    }
    //console.log(bigramsObj);
  } else {
    let newtext = "";
    for (let i = 0; i < text.length; i += 2) {
      newtext += text[i];
    }
    for (let i = 0; i < newtext.length - 1; i++) {
      bigram = text[i] + text[i + 1];
      bigrams.push(bigram);
    }
    for (let i = 0; i < bigrams.length; i++) {
      if (bigramsObj[bigrams[i]] != undefined) bigramsObj[bigrams[i]]++;
      else bigramsObj[bigrams[i]] = 1;
    }
    for (let el in bigramsObj) {
      bigramsObj[el] = bigramsObj[el] / newtext.length / 2;
    }
  }
  let varArr = [];
  let summ = 0;
  for (let val of Object.values(bigramsObj)) {
    varArr.push(-val * Math.log2(val));
  }
  for (let val of varArr) {
    summ += val;
  }
  summ = summ / 2;
  //console.log(summ," and sets redundency ", redundency(summ, Object.values(bigramsObj).length));
  appendList(sortObj(bigramsObj), iteration);
}
