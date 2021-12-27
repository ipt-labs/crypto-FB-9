use std::cmp::Ordering;
use std::collections::{BTreeMap, HashMap};
use std::fs;

use itertools::Itertools;
use once_cell::sync::OnceCell;
use regex::Regex;

fn egcd(a: isize, b: isize) -> (isize, isize, isize) {
    if a == 0 {
        (b, 0, 1)
    } else {
        let (g, y, x) = egcd(b.rem_euclid(a), a);
        (g, x - (b / a) * y, y)
    }
}

fn mod_inv(a: isize, n: isize) -> Option<isize> {
    let (g, x, _) = egcd(a, n);
    if g == 1 {
        Some(x.rem_euclid(n))
    } else {
        None
    }
}

fn linear(a: isize, b: isize, n: isize) -> Option<Vec<isize>> {
    let a = a.rem_euclid(n);
    let b = b.rem_euclid(n);
    let (g, x, _) = egcd(a, n);
    if g != 1 {
        if b.rem_euclid(g) != 0 {
            None
        } else {
            let ans = linear(a / g, b / g, n / g).unwrap();
            Some(
                (0..g)
                    .map(|i| ans.iter().map(move |x| (x + (g - i) * n / g).rem_euclid(n)))
                    .flatten()
                    .collect::<Vec<isize>>(),
            )
        }
    } else {
        Some(vec![(x * b).rem_euclid(n)])
    }
}

pub fn count_bigram_frequency(text: &str) -> HashMap<String, f32> {
    let chunks = text.chars().chunks(2);
    let iter = chunks
        .into_iter()
        .map(|item| item.collect::<String>())
        .filter(|n| n.chars().count() == 2);
    let mut frequency = BTreeMap::new();
    for item in iter {
        *frequency.entry(item).or_insert(0f32) += 1f32;
    }

    let len: f32 = frequency.values().sum();
    for (_, v) in frequency.iter_mut() {
        *v = *v / len;
    }
    frequency
        .into_iter()
        .sorted_by(|(_, a), (_, b)| b.partial_cmp(a).unwrap_or(Ordering::Equal))
        .take(5)
        .collect::<HashMap<_, _>>()
}

static ALPHABET: OnceCell<Alphabet> = OnceCell::new();

pub struct Alphabet(Vec<char>);

impl Alphabet {
    pub fn global() -> &'static Alphabet {
        ALPHABET.get_or_init(|| {
            let mut chars = ('а'..='я').filter(|c| c != &'ъ').collect::<Vec<_>>();
            chars.swap(26, 27);
            Alphabet(chars)
        })
    }

    pub fn get_index(&self, ch: &char) -> usize {
        self.0.iter().position(|c| c == ch).unwrap()
    }
    pub fn len(&self) -> usize {
        self.0.len()
    }
    pub fn get_char(&self, index: usize) -> &char {
        self.0.get(index).unwrap()
    }
}

fn bi_number(bi: &str) -> isize {
    let chars = bi.chars().collect::<Vec<_>>();
    let alphabet = Alphabet::global();
    (alphabet.get_index(chars.get(0).unwrap()) * alphabet.len()
        + alphabet.get_index(chars.get(1).unwrap())) as isize
}

fn decode(a: isize, b: isize, text: &str) -> Option<String> {
    let impossible_bi = vec![
        "аь", "еь", "иь", "оь", "уь", "юь", "яь", "эь", "ыь", "жы", "шы", "фй", "дй", "хщ", "яы",
        "ьь", "яь", "бй", "эы", "эь",
    ];
    let alphabet = Alphabet::global();
    let alphabet_len = alphabet.len() as isize;

    let (_, x, _) = egcd(a, alphabet_len.pow(2));
    let vec = text
        .chars()
        .clone()
        .chunks(2)
        .into_iter()
        .map(|item| item.collect::<String>())
        .map(|n| {
            let decoded_bi = ((bi_number(n.as_str()) - b) * x).rem_euclid(alphabet_len.pow(2));
            let second_index = decoded_bi.rem_euclid(alphabet_len);
            let first_index = ((decoded_bi - second_index) / alphabet_len) as usize;
            format!(
                "{}{}",
                alphabet.get_char(first_index),
                alphabet.get_char(second_index as usize)
            )
        })
        .collect::<Vec<_>>();
    if vec.iter().any(|bi| impossible_bi.contains(&bi.as_str())) {
        None
    } else {
        Some(vec.join(""))
    }
}

fn main() {
    assert_eq!(mod_inv(3, 26), Some(9));
    assert_eq!(linear(1287, 447, 516), Some(vec![109, 453, 281]));
    let text = fs::read_to_string("03.txt").unwrap();
    let text = Regex::new(r"\s+").unwrap().replace_all(&text, "");

    let alphabet = Alphabet::global();

    let map = count_bigram_frequency(&text);

    let most_bi = vec![
        "ст".to_string(),
        "но".to_string(),
        "то".to_string(),
        "на".to_string(),
        "ен".to_string(),
    ];
    let vec = vec![
        most_bi,
        map.keys().map(|s| s.to_string()).collect::<Vec<_>>(),
    ];
    println!(
        "{:?}",
        map.keys().map(|s| s.to_string()).collect::<Vec<_>>()
    );
    let vec = vec
        .into_iter()
        .multi_cartesian_product()
        .collect::<Vec<_>>();
    let keys = vec
        .clone()
        .into_iter()
        .cartesian_product(vec.into_iter())
        .filter(|(v1, v2)| {
            let y0 = v1.get(0).unwrap();
            let y1 = v1.get(1).unwrap();

            let x0 = v2.get(0).unwrap();
            let x1 = v2.get(1).unwrap();
            y0 != x0 && y1 != x0 && y0 != x1 && y1 != x1
        })
        .collect::<Vec<_>>();
    println!("keys len: {:?}", keys.len());

    let n = alphabet.len().pow(2) as isize;
    'l: for (pair1, pair2) in keys {
        let y1 = bi_number(pair1.get(0).unwrap());
        let x1 = bi_number(pair1.get(1).unwrap());
        let a = y1 - bi_number(pair2.get(0).unwrap());
        let b = x1 - bi_number(pair2.get(1).unwrap());
        if let Some(keys) = linear(a, b, n).map(|a| {
            a.into_iter()
                .map(|a| (a, (x1 - (y1 * a)).rem_euclid(n)))
                .collect::<HashMap<_, _>>()
        }) {
            for (a, b) in keys {
                if let Some(text) = decode(a, b, &text) {
                    println!("a: {}, b: {}", a, b);
                    println!("{}", text);
                    break 'l;
                }
            }
        }
    }
}
